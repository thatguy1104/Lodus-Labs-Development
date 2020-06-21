import pyodbc
import datetime

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver= '{ODBC Driver 17 for SQL Server}'

def createDB():
    myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
    cur = myConnection.cursor()

    create = """DROP TABLE IF EXISTS trials;"""
    cur.execute(create)
    script = """
        CREATE TABLE trials(
            appid               INT,
            name_               text,
            release_date        text,
            Last_Updated        DATETIME
        );
        """
    cur.execute(script)
    print("Successully created DB: Table -> trials DB -> {0}".format(database))
    myConnection.commit()
    myConnection.close()

def checkTableExists(dbcon, tablename):
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

def writeToDB():
    myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
    cur = myConnection.cursor()

    if not checkTableExists(myConnection, 'trials'):
        createDB()

    curr_date = datetime.datetime.now()
    dummy_data = ((248820,	"Bruh", "2013-11-08", curr_date),                                                                                                                                                                                                                                                                                 
                  (248860,	"NEO Scavenger", "2014-12-15", curr_date),                                                                                                                                                                                                                                                                                               
                  (249051,	"Dungeon of the Endless™", "2014-10-27", curr_date),                                                                                                                                                                                                                                                                                       
                  (249131,	"LEGO® Marvel™ Super Heroes", "2013-11-15", curr_date),                                                                                                                                                                                                                                                                                               
                  (249191,	"Ancient Space", "2014-09-23", curr_date),                                                                                                                                                                                                                                                                               
                  (249231,	"BET okeee", "2014-08-13", curr_date))
    for data in dummy_data:
        cols = ['appid', 'name_', 'release_date', 'Last_Update']
        update = "UPDATE trials SET appid = ?"
        cur.execute(update, data[0])

    #     # insertion = """INSERT INTO trials(appid, name_, release_date, Last_Updated) VALUES(?, ?, ?, ?)"""
    #     # cur.execute(insertion, data)
    
    print("Successfully written to table -> {0}, DB -> {1}".format("trials", database))
    myConnection.commit()
    myConnection.close()

def run():
    # createDB()
    writeToDB()

run()