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


class Provider():
    def __init__(self):
        self.ProviderLink = 'https://steamcdn-a.akamaihd.net/steam/publicstats/top_asns_per_country.jsonp?v=' + time.strftime("%m-%d-%Y") + str(10)
        self.response = requests.get(self.ProviderLink)
        try:
            self.response.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s with scraping for <steam_provider_data>' % (exc))
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.CountryCodeLink = 'https://steamstore-a.akamaihd.net/public/data/world-countries.jsonp'
        self.response_countries = requests.get(self.CountryCodeLink)
        try:
            self.response_countries.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s with scraping for <steam_provider_data>' % (exc))
    
    def progress(self, count, total, custom_text, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '*' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s %s %s\r' %
                         (bar, percents, '%', custom_text, suffix))
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

    def getData(self):
        # PERFORMANCE BY INTERNET SERVICE PROVIDER (ISP)
        self.response_countries = self.response_countries.text
        self.response = self.response.text

        # PARSE OUT THE DATA FORMATS: JSONP --> JSON
        provider_data = json.loads(self.response[self.response.index("(") + 1: self.response.rindex(")")])
        country_code_data = json.loads(self.response_countries[self.response_countries.index("(") + 1: self.response_countries.rindex(")")])

        # COUNTRY NAME AND ITS CODE ABBREVIATION
        # features = country_code_data['features']
        features_data = {}
        # features_data['CountryCodes'] = []
        # for i in range(len(features)):
        #     codes = country_code_data['features'][i]['properties']['name']
        #     id_ = country_code_data['features'][i]['id']

        # with open('STEAM/ServiceProvider/provider_data.json', 'w') as outfile:
        #     json.dump(provider_data, outfile)
        # with open('STEAM/ServiceProvider/country_codes.json', 'w') as outfile:
        #     json.dump(features_data, outfile)

        return provider_data, features_data

    def writeProvider(self):
        # DATA:
        provider, codes = self.getData()
        data = []
        curr_date = datetime.datetime.now()

        for country in provider:
            for i in range(len(provider[country])):
                asname = provider[country][i]['asname']
                totalbytes = int(provider[country][i]['totalbytes'])
                avgmbps = provider[country][i]['avgmbps']
                data.append((country, asname, totalbytes, avgmbps, curr_date))

        # CURRENT DATA
        curr_date = datetime.datetime.now()

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'steam_provider_data'):
            # EXECUTE SQL COMMANDS
            cur.execute("DROP TABLE IF EXISTS steam_provider_data;")
            create = """CREATE TABLE steam_provider_data(
                Country_Code    VARCHAR(50),
                asname          VARCHAR(50),
                totalbytes      BIGINT,
                avgmbps         FLOAT,
                Last_Updated    DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""
            cur.execute(create)
            myConnection.commit()
            print("Successully created table <steam_provider_data>")

        # DO NOT WRITE IF LIST IS EMPTY DUE TO TOO MANY REQUESTS
        if not data:
            print("Not written --> too many requests")
        else:
            # RECORD INITIAL TIME OF WRITING
            t0 = time.time()

            # EXECUTE INSERTION INTO DB
            cur.fast_executemany = True
            insertion = "INSERT INTO steam_provider_data(Country_Code, asname, totalbytes, avgmbps, Last_Updated) VALUES (?, ?, ?, ?, ?)"
            cur.executemany(insertion, data)

            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to table <steam_provider_data> (db: {0})".format(database))

        myConnection.commit()
        myConnection.close()

        return t1 - t0
