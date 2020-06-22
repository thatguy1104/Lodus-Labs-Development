import requests
import json
from bs4 import BeautifulSoup
import lxml
import pyodbc
import datetime
import time
import sys
import configparser as cfg

class AllGamesForDev():
    def __init__(self):
        self.link = 'https://www.androidrank.org'
        parser = cfg.ConfigParser()
        parser.read('config.cfg')
        self.server = parser.get('db_credentials', 'server')
        self.database = parser.get('db_credentials', 'database')
        self.username = parser.get('db_credentials', 'username')
        self.password = parser.get('db_credentials', 'password')
        self.driver = parser.get('db_credentials', 'driver')

    def progress(self, count, total, custom_text, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '*' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s %s %s\r' % (bar, percents, '%', custom_text, suffix))
        sys.stdout.flush()

    def scrapeOne(self, id):
        response = requests.get(self.link + id)
        soup = BeautifulSoup(response.text, 'lxml')

        odd = soup.find_all('tr', class_='odd')
        even = soup.find_all('tr', class_='even')
        all_rows = odd + even

        curr_date = datetime.datetime.now()

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
            results.append([tittle, rank, rating, intalls, avg_rating, growth_30_days, growth_60_days, price, curr_date])
        return results

    def getIDs(self):
        ids = []

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
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

    def getAllGameStats(self):
        ids = self.getIDs()

        # ITERATE THROUGH IDS, SCRAPE DATA
        data = []
        count = 0

        for dev in range(len(ids)):
            self.progress(count, len(ids), "scraping for <play_app_ranks>")
            resultOne = self.scrapeOne(ids[dev][0])
            devel = ids[dev][1]
            for i in range(len(resultOne)):
                resultOne[i].insert(0, devel)
                data.append(tuple(resultOne[i]))
            count += 1  
        sys.stdout.write('\n')

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'trials'):
            # EXECUTE SQL COMMANDS
            cur.execute("DROP TABLE IF EXISTS play_app_ranks;")
            create = """CREATE TABLE play_app_ranks(
                Developer           NVARCHAR(100),
                App_Name            NVARCHAR(100),
                App_Rank            INT,
                Total_Rating        BIGINT,
                Installs            VARCHAR(100),
                Average_Rating      FLOAT,
                Growth_30_days      VARCHAR(100),
                Growth_60_days      VARCHAR(100),
                Price               VARCHAR(50),
                Last_Updated        DATETIME
            );"""
            cur.execute(create)
            print("Successully created DB: Table -> play_app_ranks DB -> {0}".format(self.database))
            myConnection.commit()

        # DIVIDE DATA INTO n CHUNKS
        n = 2000
        final = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n )]

        # DO NOT WRITE IF LIST IS EMPTY DUE TO TOO MANY REQUESTS
        if not data:
            print("Not written --> too many requests")
        else:
            # RECORD INITIAL TIME OF WRITING
            t0 = time.time()

            # ITERATE THROUGH DICT AND INSERT VALUES ROW-BY
            counter = 0
            for elem in final:
                self.progress(counter, len(final), "writing to <play_app_ranks>")
                cur.fast_executemany = True
                insertion = "INSERT INTO play_app_ranks(Developer, App_Name, App_Rank, Total_Rating, Installs, Average_Rating, Growth_30_days, Growth_60_days, Price, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.executemany(insertion, elem)
                counter += 1
            sys.stdout.write('\n')
            
            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to: Table -> play_app_ranks DB -> {0}".format(self.database))
        myConnection.commit()
        myConnection.close()

        return t1-t0