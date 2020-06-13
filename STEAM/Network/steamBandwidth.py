import requests
import json
import time
import math
import pyodbc
import datetime

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver= '{ODBC Driver 17 for SQL Server}'

class SteamBandwidth():
    def __init__(self, weird_num):
        self.url = 'https://steamcdn-a.akamaihd.net/steam/publicstats/download_traffic_per_country.jsonp?v=' + \
            time.strftime("%m-%d-%Y") + str(weird_num)
        self.response = requests.get(self.url).text

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

    def writeBandwidthSteam(self):
        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
        cur = myConnection.cursor()

        # EXECUTE SQL COMMANDS
        cur.execute("DROP TABLE IF EXISTS steam_network_data;")
        create = """CREATE TABLE steam_network_data(
            Country                         CHAR(200),
            Total_Bytes                     BIGINT,
            Avg_MB_Per_Sec                  NUMERIC,
            Percentage_of_Global_Traffic    NUMERIC,
            Last_Updated                    DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        cur.execute(create)
        print("Successully created DB Table: steam_network_data")

        # DATA:
        bandwidthFile = self.setup()

        for name in bandwidthFile:
            country = name
            totalbytes = bandwidthFile[name]['totalbytes']
            avg_mb = bandwidthFile[name]['avgmbps']
            perc_global_traffic = bandwidthFile[name]['Percentage of global Steam Traffic']
            curr_date = datetime.datetime.now()

            insertion = "INSERT INTO steam_network_data(Country, Total_Bytes, Avg_MB_Per_Sec, Percentage_of_Global_Traffic, Last_Updated) VALUES (?, ?, ?, ?, ?)"
            values = (country, totalbytes, avg_mb, perc_global_traffic, curr_date)
            cur.execute(insertion, values)

        print("\nSuccessully written to table  <steam_network_data> (db: {0})".format(database))
        myConnection.commit()
        myConnection.close()