import psycopg2
import json

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

    # EXECUTE SQL COMMANDS
    cur.execute("DROP TABLE IF EXISTS concurrentGames;")
    create = """CREATE TABLE concurrentGames(
        Name_               CHAR(200),
        Current_Players     BIGINT,
        Peak_Today          BIGINT,
        Hours_Played        BIGINT,
        Time_Updated        TIME NOT NULL DEFAULT CURRENT_TIME,
        Date_Updated DATE NOT NULL DEFAULT CURRENT_DATE
    );"""
    cur.execute(create)

    for elem in data['Concurrent Steam Data']:
        game_name = elem['Game Name']
        current = elem['Current Players']
        peak = elem['Peak Today']
        hours = elem['Hours Played']
        
        insertion = "INSERT INTO concurrentGames(Name_, Current_Players, Peak_Today, Hours_Played) VALUES (%s, %s, %s, %s)"
        values = (game_name, current, peak, hours)
        cur.execute(insertion, values)
    
    print("db files loaded")

    myConnection.commit()
    myConnection.close()

doQuery()