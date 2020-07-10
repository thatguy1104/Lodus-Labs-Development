import requests
import json
import sys
import time
import lxml
from tqdm import tqdm
import pyodbc
import datetime
from bs4 import BeautifulSoup

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver = '{ODBC Driver 17 for SQL Server}'


class Bandwidth_48():
    def __init__(self):
        self.link = 'https://store.steampowered.com/stats/content/'
        self.response = requests.get(self.link)
        try:
            self.response.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s with scraping for <steam_48_bandwidth>' % (exc))
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def get_data(self):
        lin = 'https://steamcdn-a.akamaihd.net/steam/publicstats/contentserver_bandwidth_stacked.jsonp?v=07-04-2020-15'
        resp = requests.get(lin).text
        file_sec = json.loads(resp[resp.index("(") + 1: resp.rindex(")")])['legend']

        # CURRENT DATA
        curr_date = datetime.datetime.now()

        data = []
        for i in range(len(file_sec)):
            country_data = file_sec[i]
            name = country_data['name']
            max_ = country_data['max']
            current = country_data['cur']
            data.append((name, max_, current, curr_date))

        return data

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

    def writeBandwidth(self):
        # DATA:
        data = self.get_data()

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'steam_48_bandwidth'):
            # EXECUTE SQL COMMANDS
            cur.execute("DROP TABLE IF EXISTS steam_48_bandwidth;")
            create = """CREATE TABLE steam_48_bandwidth(
                Name            VARCHAR(50),
                Peak            FLOAT,
                Current_         FLOAT,
                Last_Updated    DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""
            cur.execute(create)
            myConnection.commit()
            print("Successully created table <steam_48_bandwidth>")

        # DO NOT WRITE IF LIST IS EMPTY DUE TO TOO MANY REQUESTS
        if not data:
            print("Not written --> too many requests")
        else:
            # RECORD INITIAL TIME OF WRITING
            t0 = time.time()

            # EXECUTE INSERTION INTO DB
            cur.fast_executemany = True
            insertion = "INSERT INTO steam_48_bandwidth(Name, Peak, Current_, Last_Updated) VALUES (?, ?, ?, ?)"
            cur.executemany(insertion, data)

            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to table <steam_48_bandwidth> (db: {0})".format(database))

        myConnection.commit()
        myConnection.close()

        return t1 - t0
