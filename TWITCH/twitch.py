import requests, json, sys, time
import twitch_oauth2_access_token_generator
import pyodbc
import sqlalchemy
import pandas as pd
import urllib

INDENT = 2
BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = 'lgb4dq2tni1ce2ib9gzmg0kp571lgz'
CLIENT_SECRET = '3j58umfzeu2mve615u3mkfwogfamy1'
GRANT_TYPE = 'client_credentials'
HEADERS = { 'Client-ID': CLIENT_ID, 
            'Client-Secret': CLIENT_SECRET,
            'Authorization': 'Bearer ' + twitch_oauth2_access_token_generator.get_access_token(CLIENT_ID,CLIENT_SECRET,GRANT_TYPE)}

def get_response(query, payload=None):
    """
    Get response from twitch API call
    """
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS, params=payload)
    return response

def get_top_games():
    """
    Gets games sorted by number of current viewers on Twitch, most popular first.
    Returned in a list of 2-tuples [(game_id, game_name),,,,]
    """
    print(sys._getframe().f_code.co_name + " calling api to receive list of top games...")
    start_time = time.time()
    top_games_list = []
    payload = {'first': 100, 'after': None}
    response = get_response('games/top', payload)
    for game in response.json()["data"]:
        top_games_list.append((int(game["id"]), game["name"]))

    while(response.json()["pagination"]): # whilst there are more pages with data, continue requesting data
        payload['after'] = response.json()["pagination"]["cursor"]
        response = get_response('games/top', payload)
        for game in response.json()["data"]:
            top_games_list.append((int(game["id"]), game["name"]))

    print("Finished receiving list with top games in " + str(time.time()-start_time) + " seconds")
    return top_games_list

def get_view_count_of_games(pagination_nr=None, view_counts={}, stream_data=[]):
    """
    Iteartes through all livestreams and sums the total view count per game, sorted accordingly
    """
    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('streams', payload)
    response_json = response.json()
    #print("In progress with " + sys._getframe().f_code.co_name)

    stream_data += response_json['data']

    # Iteate through streams and add view_count
    for stream in response_json['data']:
        if stream['game_id'] == '':
            continue 
        elif stream['game_id'] in view_counts.keys():
            view_counts[stream['game_id']] += stream['viewer_count']
        else:
            view_counts[stream['game_id']] = stream['viewer_count']

    # Stop the functions once we are looking at streams with 3 viewer
    if 100 in view_counts.values():
        return list(view_counts.items()),stream_data

    if (response.json()["pagination"]):  # If there exists more livestreams go to next page
        payload['after'] = response.json()["pagination"]["cursor"]
        get_view_count_of_games(pagination_nr=response.json()["pagination"]["cursor"], view_counts=view_counts, stream_data=stream_data)
    return list(view_counts.items()),stream_data

def run_get_top_games():
    SERVER = 'serverteest.database.windows.net'
    DATABASE = 'testdatabase'
    USERNAME = 'login12391239'
    PASSWORD = 'HejsanHejsan!1'
    DRIVER= '{ODBC Driver 17 for SQL Server}'

    top_games_list = get_top_games() 

    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+PASSWORD)
    cursor = conn.cursor()
    print("SQL Server connection established")
    cursor.fast_executemany = True
    sql_insert_query = """INSERT INTO games2 (gameid, gamename) 
                                    VALUES (?, ?) """
    start_time = time.time()
    cursor.executemany(sql_insert_query, top_games_list)
    conn.commit()
    print(cursor.rowcount, "Record inserted successfully into table")
    print(str(len(top_games_list)) + " rows in " + str(time.time() - start_time) + "seconds")
    cursor.close()
    conn.close()
    print("SQL Server connection is closed")

def run_get_view_count_of_games():
    SERVER = 'serverteest.database.windows.net'
    DATABASE = 'testdatabase'
    USERNAME = 'login12391239'
    PASSWORD = 'HejsanHejsan!1'
    DRIVER= '{ODBC Driver 17 for SQL Server}'

    top_games_list = get_view_count_of_games()[0]
    top_games_list = list(tuple(map(int, (x,y))) for x,y in top_games_list) # convert ('gameid',viewcount) -> (gameid,viewcount) aka (str,int)->(int,int) 
    top_games_list.sort(key=lambda tup: tup[1], reverse=True) # sort list based on viewcount

    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+PASSWORD)
    cursor = conn.cursor()
    print("SQL Server connection established")
    cursor.fast_executemany = True
    sql_insert_query = """INSERT INTO twitch_view_counts (GameID, ViewCount) 
                                    VALUES (?, ?) """
    start_time = time.time()
    cursor.executemany(sql_insert_query, top_games_list)
    conn.commit()
    print(cursor.rowcount, "Record inserted successfully into table")
    print(str(len(top_games_list)) + " rows in " + str(time.time() - start_time) + "seconds")
    cursor.close()
    conn.close()
    print("SQL Server connection is closed")

#run_get_top_games()
#run_get_view_count_of_games()


def testt():
    streamlist = get_view_count_of_games()[1]
    dataframe = pd.DataFrame.from_dict(streamlist, orient='columns')
    dataframe.drop(columns=['tag_ids','type','title','user_name','thumbnail_url'], inplace = True)
    #curr_time = time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())
    #dataframe['time_logged'] = curr_time
    dataframe = dataframe.rename(columns={'user_id':'userr_id', 'language':'stream_language'})
    print(dataframe)

    SERVER = 'serverteest.database.windows.net'
    DATABASE = 'testdatabase'
    USERNAME = 'login12391239'
    PASSWORD = 'HejsanHejsan!1'
    DRIVER= '{ODBC Driver 17 for SQL Server}'

    params = urllib.parse.quote_plus('DRIVER='+DRIVER+';SERVER='+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+PASSWORD)
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)
    
    print("SQL Server connection established")
    start_time = time.time()

    dataframe.to_sql('streams', con=engine, schema='dbo', if_exists='append',index=False)
    print("Record inserted successfully into table")
    print(str(dataframe.shape[0]) + " rows in " + str(time.time() - start_time) + "seconds")
    print("SQL Server connection is closed")

testt()