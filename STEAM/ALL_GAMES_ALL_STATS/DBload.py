import psycopg2
import json

hostname = 'localhost'
username = 'postgres'
password = ''
database = 'steam_data'

def readJSON():
    data = None
    try:
        with open('recordsAllGameStats.json') as json_file:
            data = json.load(json_file)
    except:
        data = {}
    return data

def doQuery() :
    myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cur = myConnection.cursor()
    data = readJSON()

    cur.execute("DROP TABLE IF EXISTS all_games_all_data")
    create = """CREATE TABLE all_games_all_data(
        name_       CHAR(100),
        ids         CHAR(100),
        months       text[][],
        avg_players     float[],
        gains           float[],
        percent_gains   text[][],
        peak_players    integer[]
    );"""
    cur.execute(create)

    counter = 0
    for i in data:
        name = data[i][0]['Name']
        id_ = data[i][0]['ID']
        months = data[i][0]['Month'] # LIST OF STRINGS
        avg_players = data[i][0]['Avg. Players'] # LIST OF FLOATS
        gains = data[i][0]['Gains'] # LIST OF FLOATS
        percent_gains = data[i][0]['\\% Gains'] # LIST OF STRINGS
        peak_players = data[i][0]['Peak Players'] # LIST OF STRINGS

        # insertion = """
        #     INSERT INTO all_games_all_data VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6})
        # """.format(name, id_, months, avg_players, gains, percent_gains, peak_players)
        insertion = "INSERT INTO all_games_all_data (name_, ids, months, avg_players, gains, percent_gains, peak_players) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(insertion, (name, id_, months, avg_players, gains, percent_gains, peak_players))

    myConnection.commit()
    myConnection.close()
    # for name in cur.fetchall():
    #     print(name)

doQuery()