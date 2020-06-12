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

class AllGamesForDev():
    def __init__(self):
        self.link = 'https://www.androidrank.org'

    def scrapeOne(self, id):
        response = requests.get(self.link + id)
        soup = BeautifulSoup(response.text, 'lxml')

        odd = soup.find_all('tr', class_='odd')
        even = soup.find_all('tr', class_='even')
        all_rows = odd + even

        results = []
        # SCRAPE THROUGH THE WEBSITE DATA TABLE
        for item in all_rows:
            row = item.find_all('td')
            rank = row[0].text.replace('.', '')
            tittle = row[1].text.replace('\n', '')
            rating = row[3].text
            intalls = row[4].text
            avg_rating = float(row[5].text)
            growth_30_days = row[6].text
            growth_60_days = row[7].text
            price = row[8].text.replace('\n', '')
            results.append((rank, tittle, rating, intalls, avg_rating, growth_30_days, growth_60_days, price))
        return results

    def getIDs(self):
        ids = []

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
        cur = myConnection.cursor()

        # READ IDS FROM NEIGHBOURING DB (project_data) & TABLE (play_dev_ranks): 
        read =  """SELECT developer,link FROM play_dev_ranks"""
        cur.execute(read)
        result = cur.fetchall()

        for i in range(len(result)):
            dev = result[i][0]
            id1 = result[i][1].replace(' ', '')
            ids.append((id1, dev))

        myConnection.commit()
        myConnection.close()

        return ids

    def getAllGameStats(self):
        ids = self.getIDs()

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
        cur = myConnection.cursor()

        # EXECUTE SQL COMMANDS
        cur.execute("DROP TABLE IF EXISTS play_app_ranks;")
        create = """CREATE TABLE play_app_ranks(
            Developer           text,
            App_Rank            text,
            App_Name            text,
            Total_Rating        BIGINT,
            Installs            text,
            Average_Rating      FLOAT,
            Growth_30_days     text,
            Growth_60_days     text,
            Price               text,
            Last_Updated        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );"""
        cur.execute(create)
        print("Successully created DB: Table -> play_app_ranks DB -> {0}".format(database))

        # ITERATE THROUGH IDS, SCRAPE DATA, WRITE TO DB
        for dev in range(len(ids)):
            resultOne = self.scrapeOne(ids[dev][0])
            print("Writing {0} / {1} to <{2}> table (db: {3})".format(dev, len(ids), "play_app_ranks", database))
            for i in range(len(resultOne)):
                # dev = ids[dev][1]
                rank = resultOne[i][0],
                app_name = resultOne[i][1],
                rating = int(resultOne[i][2]),
                installs = resultOne[i][3],
                avg = resultOne[i][4],
                thirty = resultOne[i][5],
                sixty = resultOne[i][6],
                price = resultOne[i][7]

                insertion = "INSERT INTO play_app_ranks(Developer, App_Rank, App_Name, Total_Rating, Installs, Average_Rating, Growth_30_days, Growth_60_days, Price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                values = (ids[dev][1], rank, app_name, rating, installs, avg, thirty, sixty, price)
                cur.execute(insertion, values)

        print("Successully written to: Table -> play_app_ranks DB -> {0}".format(database))
        myConnection.commit()
        myConnection.close()