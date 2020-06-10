import psycopg2
import json
import datetime

hostname = 'localhost'
username = 'postgres'
password = 'analytcis_123'
database = 'steam_data'

def readJSON():
    """
    READ ALREADY UPDATED DATA
    """
    data = None
    try:
        with open('top100GamesByPlayers.json') as json_file:
            data = json.load(json_file)
    except:
        data = {}
    return data

def doQuery() :
    """
    WRITE DATA TO DATABASE TABLE: concurrentgames
    """

    # CONNECT TO DATABASE
    myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cur = myConnection.cursor()

    # READ DATA
    data = readJSON()
    time_now = datetime.datetime.now()

    # EXECUTE SQL COMMANDS
    cur.execute("DROP TABLE IF EXISTS concurrentGames;")
    create = """CREATE TABLE concurrentGames(
        Name_               CHAR(200),
        Current_Players     BIGINT,
        Peak_Today          BIGINT,
        Hours_Played        BIGINT,
        Last_Updated        TIME
    );"""
    cur.execute(create)

    for elem in data['Concurrent Steam Data']:
        game_name = elem['Game Name']
        current = elem['Current Players']
        peak = elem['Peak Today']
        hours = elem['Hours Played']
        
        insertion = "INSERT INTO concurrentGames(Name_, Current_Players, Peak_Today, Hours_Played, Last_Updated) VALUES (%s, %s, %s, %s, %s)"
        t = str(time_now.hour) + ":" + str(time_now.minute) + ":" + str(time_now.second)
        values = (game_name, current, peak, hours, t)
        cur.execute(insertion, values)
    
    print("db files loaded")

    myConnection.commit()
    myConnection.close()

doQuery()