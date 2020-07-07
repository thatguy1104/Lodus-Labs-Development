import json
import pyodbc
import configparser as cfg


class Integrate():
    def __init__(self):
        parser = cfg.ConfigParser()
        parser.read('config.cfg')
        self.server = parser.get('db_credentials', 'server')
        self.database = parser.get('db_credentials', 'database')
        self.username = parser.get('db_credentials', 'username')
        self.password = parser.get('db_credentials', 'password')
        self.driver = parser.get('db_credentials', 'driver')

    def connect(self):
        # CONNECT TO A SERVER DATABASE
        myConnection = pyodbc.connect('DRIVER=' + self.driver + ';SERVER=' + self.server + ';PORT=1433;DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        cur = myConnection.cursor()
        cur.execute("""
            SELECT name_
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format("steam_all_games_all_data"))
        records = cur.fetchall()
        print(records)




obj = Integrate()
obj.connect()
