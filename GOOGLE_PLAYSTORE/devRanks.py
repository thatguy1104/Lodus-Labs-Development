import requests
import json
from bs4 import BeautifulSoup
import lxml
import pyodbc
import datetime
import time
import csv
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
            curr_date = datetime.datetime.now()
            results.append((rank, row[1].text, ratings, installs, applications, avg_rating, link, curr_date))
        
        print(results)
        results = sorted(results, key=lambda x: x[0])
        return results
        
    def writeToDB(self):
        start_page = 1
        # end_page = 1341
        end_page = 21

        # SCRAPE ALL DATA FIRST
        data = []
        while start_page != end_page:
            data_list = self.scrape(str(start_page))
            for i in range(len(data_list)):
                data.append(data_list[i])
            start_page += 20

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        cur = myConnection.cursor()

        # EXECUTE SQL COMMANDS
        cur.execute("DROP TABLE IF EXISTS play_dev_ranks;")
        create = """CREATE TABLE play_dev_ranks(
            Rank                INT,
            Developer           VARCHAR(200),
            Total_Ratings       BIGINT DEFAULT 0,
            Total_Installs      BIGINT DEFAULT 0,
            Applications        INT DEFAULT 0,
            Average_Rating      FLOAT DEFAULT 0.0,
            Link                VARCHAR(200),
            Last_Updated        DATETIME
        );"""
        cur.execute(create) 
        print("Successully created DB: Table -> play_dev_ranks DB -> {0}".format(self.database))

        # RECORD INITIAL TIME OF WRITING
        t0 = time.time()

        # INSERT THE VALUES INTO DB TABLE
        cur.fast_executemany = True
        insertion = "INSERT INTO play_dev_ranks(Rank, Developer, Total_Ratings, Total_Installs, Applications, Average_Rating, Link, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cur.executemany(insertion, data)

        # RECORD END TIME OF WRITING
        t1 = time.time()

        print("Successully written to: Table -> play_dev_ranks DB -> {0}".format(self.database))
        myConnection.commit()
        myConnection.close()

        return t1-t0