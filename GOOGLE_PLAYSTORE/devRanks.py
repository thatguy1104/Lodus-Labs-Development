import requests
import json
from bs4 import BeautifulSoup
import lxml
import pyodbc

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver= '{ODBC Driver 17 for SQL Server}'

class DevelopersGames():
    def __init__(self):
        self.startLink = 'https://www.androidrank.org/developers/ranking?&start='

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
        myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
        cur = myConnection.cursor()

        # EXECUTE SQL COMMANDS
        cur.execute("DROP TABLE IF EXISTS PLAY_dev_ranks;")
        create = """CREATE TABLE PLAY_dev_ranks(
            Rank                INT,
            Developer           text,
            Link                text,
            Total_Ratings       BIGINT DEFAULT 0,
            Total_Installs      BIGINT DEFAULT 0,
            Applications        INT DEFAULT 0,
            Average_Rating      NUMERIC DEFAULT 0.0,
            Last_Updated        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );"""
        cur.execute(create)
        print("Successully created DB: Table -> PLAY_dev_ranks DB -> {0}".format(database))

        while start_page != end_page:
            print("Writing {0} / {1} to <play_dev_ranks> table (db: {2})".format(start_page, end_page, database))
            data_list = self.scrape(str(start_page))
            for i in range(len(data_list)):
                rank = data_list[i][0]
                dev = data_list[i][1].replace('\t', '')
                link = data_list[i][6]
                rat = data_list[i][2]
                installs = data_list[i][3]
                apps = data_list[i][4]
                avg = data_list[i][5]
                
                insertion = "INSERT INTO PLAY_dev_ranks(Rank, Developer, Link, Total_Ratings, Total_Installs, Applications, Average_Rating) VALUES (?, ?, ?, ?, ?, ?, ?)"
                values = (rank, dev, link, rat, installs, apps, avg)
                cur.execute(insertion, values)
            start_page += 20
        
        print("Successully written to: Table -> play_dev_ranks DB -> {0}".format(database))
        myConnection.commit()
        myConnection.close()