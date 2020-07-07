import json
import pyodbc
import configparser as cfg

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver = '{ODBC Driver 17 for SQL Server}'

class Integrate():
    def __init__(self):
        ok = 4

    def returnNameSet(self):
        # CONNECT TO A SERVER DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()
        cur.execute("""SELECT name_ FROM steam_all_games_all_data""")
        records = cur.fetchall()

        name_set = set()
        for name in records:
            name_set.add(str(name[0]))
        
        return name_set

obj = Integrate()
obj.returnNameSet()
