import requests
import json
from bs4 import BeautifulSoup
import lxml
import pyodbc
import datetime
import configparser as cfg

def getLoginCredentials():
    parser = cfg.ConfigParser()
    parser.read('config.cfg')

    # server = parser.get('db_credentials', 'server')
    # database = parser.get('db_credentials', 'database')
    # username = parser.get('db_credentials', 'username')
    # password = parser.get('db_credentials', 'password')
    # driver = parser.get('db_credentials', 'driver')
    server = 'serverteest.database.windows.net'
    database = 'testdatabase'
    username = 'login12391239'
    password = 'HejsanHejsan!1'
    driver= '{ODBC Driver 17 for SQL Server}'


    print(server, database, username, password, driver)

    return server, database, username, password, driver

def run():
    server, database, username, password, driver = getLoginCredentials()
    # CONNECT TO DATABASE
    myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
    cur = myConnection.cursor()

    # EXECUTE SQL COMMANDS
    cur.execute("DROP TABLE IF EXISTS trials;")
    create = """CREATE TABLE trials(
        Developer           text,
        Average_Rating      NUMERIC DEFAULT 0.0,
        Last_Updated        DATETIME
    );"""
    cur.execute(create)
    print("Successully created DB: Table -> trials DB -> {0}".format(database))

    curr_date = datetime.datetime.now()

    insertion = "INSERT INTO trials(Developer, Average_Rating, Last_Updated) VALUES (?, ?, ?)"
    data = ('Google Inc.', 10.1, curr_date)
    cur.execute(insertion, data)

    print("Successully written to: Table -> trials DB -> {0}".format(database))
    myConnection.commit()
    myConnection.close()


run()