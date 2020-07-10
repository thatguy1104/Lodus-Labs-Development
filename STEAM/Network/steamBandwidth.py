import requests
import json
import sys
import time
import math
from tqdm import tqdm
import pyodbc
import datetime
import configparser as cfg

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver = '{ODBC Driver 17 for SQL Server}'


class SteamBandwidth():
    def __init__(self, weird_num):
        self.url = 'https://steamcdn-a.akamaihd.net/steam/publicstats/download_traffic_per_country.jsonp?v=' + \
                   time.strftime("%m-%d-%Y") + str(weird_num)
        self.response = requests.get(self.url)
        try:
            self.response.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s with scraping for <steam_network_data>' % (exc))
        self.response = self.response.text
        parser = cfg.ConfigParser()
        parser.read('config.cfg')
        self.server = parser.get('db_credentials', 'server')
        self.database = parser.get('db_credentials', 'database')
        self.username = parser.get('db_credentials', 'username')
        self.password = parser.get('db_credentials', 'password')
        self.driver = parser.get('db_credentials', 'driver')

    def setup(self):
        # Remove JSONP function name and braces, conversion to JSON format
        startidx = self.response.find('(')
        endidx = self.response.find(')')
        bandwidthFile = json.loads(self.response[startidx + 1:endidx])

        grand_total = 0

        for name in bandwidthFile:
            if type(bandwidthFile[name]['totalbytes']) == str:
                bandwidthFile[name]['totalbytes'] = int(bandwidthFile[name]['totalbytes'])

            # Add to total for traffic percentage per country insight
            grand_total += bandwidthFile[name]['totalbytes']
            if type(bandwidthFile[name]['avgmbps']) == str:
                bandwidthFile[name]['avgmbps'] = int(bandwidthFile[name]['avgmbps'])

        # Calculate additional insights
        for name in bandwidthFile:
            bandwidthFile[name]['Percentage of global Steam Traffic'] = []
            percentage = (bandwidthFile[name]['totalbytes'] / grand_total) * 100
            number = round(percentage, 2)
            bandwidthFile[name]['Percentage of global Steam Traffic'] = number

        return bandwidthFile

    def progress(self, count, total, custom_text, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '*' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s %s %s\r' % (bar, percents, '%', custom_text, suffix))
        sys.stdout.flush()

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

    def writeBandwidthSteam(self):
        # DATA:
        bandwidthFile = self.setup()
        data = []

        # CURRENT DATA
        curr_date = datetime.datetime.now()
        counter = 1
        for name in bandwidthFile:
            self.progress(counter, len(bandwidthFile), "scraping for <steam_network_data>")
            totalbytes = bandwidthFile[name]['totalbytes']
            avg_mb = bandwidthFile[name]['avgmbps']
            perc_global_traffic = bandwidthFile[name]['Percentage of global Steam Traffic']
            data.append((name, totalbytes, avg_mb, perc_global_traffic, curr_date))
            counter += 1
        sys.stdout.write('\n')

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect(
            'DRIVER=' + self.driver + ';SERVER=' + self.server + ';PORT=1433;DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'steam_network_data'):
            # EXECUTE SQL COMMANDS
            cur.execute("DROP TABLE IF EXISTS steam_network_data;")
            create = """CREATE TABLE steam_network_data(
                Country                         VARCHAR(100),
                Total_Bytes                     BIGINT,
                Avg_MB_Per_Sec                  NUMERIC,
                Percentage_of_Global_Traffic    FLOAT,
                Last_Updated                    DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""
            cur.execute(create)
            myConnection.commit()
            print("Successully created table <steam_network_data>")

        # DO NOT WRITE IF LIST IS EMPTY DUE TO TOO MANY REQUESTS
        if not data:
            print("Not written --> too many requests")
        else:
            # RECORD INITIAL TIME OF WRITING
            t0 = time.time()

            # EXECUTE INSERTION INTO DB
            cur.fast_executemany = True
            insertion = "INSERT INTO steam_network_data(Country, Total_Bytes, Avg_MB_Per_Sec, Percentage_of_Global_Traffic, Last_Updated) VALUES (?, ?, ?, ?, ?)"
            cur.executemany(insertion, data)

            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to table <steam_network_data> (db: {0})".format(self.database))

        myConnection.commit()
        myConnection.close()

        return t1 - t0
