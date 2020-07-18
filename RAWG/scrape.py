import json
import requests
import os, sys
import pyodbc
from datetime import datetime
import time
import pandas as pd

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver = '{ODBC Driver 17 for SQL Server}'

class RAWG_Scrape():
    def __init__(self):
        self.link = 'https://api.rawg.io/api/games?page=1'

    def checkTableExists(self, dbcon, tablename):
        dbcur = dbcon.cursor()
        dbcur.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        if dbcur.fetchone()[0] == 1:
            dbcur.close()
            return True

        dbcur.close()
        return False

    def progress(self, count, total, custom_text, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '*' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s %s %s\r' % (bar, percents, '%', custom_text, suffix))
        sys.stdout.flush()

    def getCretors(self):
        response = requests.get(self.link, headers={'User-Agent': 'Lodus Labs'}).json()
        curr_date = datetime.now()
        data = []
        count = 0
        
        # while response['next']:
        for i in range(5):
            # 20922
            self.progress(count, 5, '<rawgGamesList>')
            next_link = response['next']

            # UPDATE RESPONSE: SET TO NEXT PAGE
            response = requests.get(next_link, headers={'User-Agent': 'Lodus Labs'}).json()

            results = response['results']
            for game in results:
                name = game['name']
                slug = game['slug']

                # GET DATE, CONVERT TO DATETIME OBJECT
                if game['released']:
                    release = game['released']
                    date_object = datetime.strptime(release, '%Y-%m-%d').date()
                else:
                    date_object = None

                if game['metacritic']:
                    metaccritic = game['metacritic']
                else:
                    metaccritic = None
                
                if game['playtime']:
                    avg_game_playtime = game['playtime']
                else:
                    avg_game_playtime = None

                if game['rating']:
                    rating = game['rating']
                else:
                    rating = None

                tba = 1
                data.append((name, slug, date_object, metaccritic, avg_game_playtime, tba, rating, curr_date))
            count += 1

        return data

    def writeToDB(self):
        # DATA:
        data = self.getCretors()

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'rawgGamesList'):
            # EXECUTE SQL COMMANDS
            cur.execute("DROP TABLE IF EXISTS rawgGamesList;")
            create = """CREATE TABLE rawgGamesList(
                gameName        NVARCHAR(200),
                gameSlug        NVARCHAR(200),
                releaseData     DATETIME,
                metacritic      INT,
                avgGamePlaytime INT,
                tba             BIT,
                Rating          FLOAT,
                Last_Updated    DATETIME
            );"""
            cur.execute(create)
            myConnection.commit()
            print("Successully created table <rawgGamesList>")

        # DIVIDE DATA INTO n CHUNKS
        n = 1000
        final = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n)]
        # cur.fast_executemany = True

        # DO NOT WRITE IF LIST IS EMPTY DUE TO TOO MANY REQUESTS
        if not data:
            print("Not written --> too many requests")
        else:
            # RECORD INITIAL TIME OF WRITING
            t0 = time.time()

            # ITERATE THROUGH DICT AND INSERT VALUES ROW-BY-ROW
            count = 1
            for elem in final:
                print(elem)
                self.progress(count, len(final), "writing to <rawgGamesList>")
                insertion = "INSERT INTO rawgGamesList(gameName, gameSlug, releaseData, metacritic, avgGamePlaytime, tba, Rating, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(insertion, elem)
                count += 1

            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to table <rawgGamesList> (db: {0})".format(database))

        myConnection.commit()
        myConnection.close()

        return t1 - t0

obj = RAWG_Scrape()
time = obj.writeToDB()
print(time)