import pyodbc

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver= '{ODBC Driver 17 for SQL Server}'

def writeToDB():
    myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
    cur = myConnection.cursor()

    create = """DROP TABLE IF EXISTS static_data;"""
    cur.execute(create)
    script = """
        CREATE TABLE static_data(
            appid               INT,
            name_               text,
            release_date        text
        );
        """
    cur.execute(script)
    print("Successully created DB: Table -> static_data DB -> {0}".format(database))

    dummy_data = ((248820,	"Risk of Rain", "2013-11-08)"),                                                                                                                                                                                                                                                                                 
                 (248860,	"NEO Scavenger", "2014-12-15"),                                                                                                                                                                                                                                                                                               
                 (249050,	"Dungeon of the Endless™", "2014-10-27"),                                                                                                                                                                                                                                                                                       
                 (249130,	"LEGO® Marvel™ Super Heroes", "2013-11-15"),                                                                                                                                                                                                                                                                                               
                 (249190,	"Ancient Space", "2014-09-23"),                                                                                                                                                                                                                                                                               
                 (249230,	"Risen 3 - Titan Lords", "2014-08-13"))
    
    for data in dummy_data:
        insertion = """INSERT INTO static_data(appid, name_, release_date) VALUES(?, ?, ?)"""
        cur.execute(insertion, data)
    
    print("Successfully written to table -> {0}, DB -> {1}".format("static_data", database))

    myConnection.commit()
    myConnection.close()

def readFromDB():
    # CONNECT TO DATABASE
    myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
    cur = myConnection.cursor()
    print("Connected to", database)
    read = """SELECT appid, name_, release_date, time_updated, date_updated FROM static_data;"""
    cur.execute(read)
    result = cur.fetchall()

    for i in range(len(result)):
        print(result[i])

def run():
    writeToDB()
    # readFromDB()

run()