import requests
import json
from bs4 import BeautifulSoup
import lxml
import pyodbc
import datetime
import configparser as cfg

class DevelopersGames():
    def __init__(self):
        self.startLink = 'https://www.androidrank.org/developers/ranking?&start='
        parser = cfg.ConfigParser()
        parser.read('config.cfg')
        self.server = parser.get('db_credentials', 'server')
        self.database = parser.get('db_credentials', 'database')
        self.username = parser.get('db_credentials', 'username')
        self.password = parser.get('db_credentials', 'password')
        self.driver = parser.get('db_credentials', 'driver')

    def scrape(self, page):
        response = requests.get(self.startLink + page)
        soup = BeautifulSoup(response.text, 'lxml')

        odd = soup.find_all('tr', class_='odd')
        even = soup.find_all('tr', class_='even')
        all_rows =  odd + even
        
        results = []
        for item in all_rows:
            row = item.find_all('td')
            link = item.find('a')['href']
            # Get: Rank, Developer, Total ratings, Total installs, Applications, Average rating
            rank = int(row[0].text.replace('.', ''))
            ratings = int(row[2].text.replace(',', ''))
            installs = int(row[3].text.replace(',', ''))
            applications = int(row[4].text)
            avg_rating = float(row[5].text)
            results.append((rank, row[1].text, ratings, installs, applications, avg_rating, link))
        
        results = sorted(results, key=lambda x: x[0])
        return results
        
    def writeToDB(self):
        data = {}
        start_page = 1
        end_page = 1341

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        cur = myConnection.cursor()

        # EXECUTE SQL COMMANDS
        cur.execute("DROP TABLE IF EXISTS play_dev_ranks;")
        create = """CREATE TABLE play_dev_ranks(
            Rank                INT,
            Developer           text,
            Link                text,
            Total_Ratings       BIGINT DEFAULT 0,
            Total_Installs      BIGINT DEFAULT 0,
            Applications        INT DEFAULT 0,
            Average_Rating      NUMERIC DEFAULT 0.0,
            Last_Updated        DATETIME
        );"""
        cur.execute(create)
        print("Successully created DB: Table -> play_dev_ranks DB -> {0}".format(self.database))

        while start_page != end_page:
            print("Writing {0} / {1} to <play_dev_ranks> table (db: {2})".format(start_page, end_page, self.database))
            data_list = self.scrape(str(start_page))
            for i in range(len(data_list)):
                rank = data_list[i][0]
                dev = data_list[i][1].replace('\t', '')
                link = data_list[i][6]
                rat = data_list[i][2]
                installs = data_list[i][3]
                apps = data_list[i][4]
                avg = data_list[i][5]
                curr_date = datetime.datetime.now()
                insertion = "INSERT INTO play_dev_ranks(Rank, Developer, Link, Total_Ratings, Total_Installs, Applications, Average_Rating, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                values = (rank, dev, link, rat, installs, apps, avg, curr_date)
                cur.execute(insertion, values)
            start_page += 20
        
        print("Successully written to: Table -> play_dev_ranks DB -> {0}".format(self.database))
        myConnection.commit()
        myConnection.close()