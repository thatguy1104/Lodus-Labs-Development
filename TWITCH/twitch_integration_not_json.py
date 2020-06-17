import requests, json, sys
import twitch_oauth2_access_token_generator

BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = 'lgb4dq2tni1ce2ib9gzmg0kp571lgz'
CLIENT_SECRET = '3j58umfzeu2mve615u3mkfwogfamy1'
GRANT_TYPE = 'client_credentials'
HEADERS = { 'Client-ID': CLIENT_ID, 
            'Client-Secret': CLIENT_SECRET,
            'Authorization': 'Bearer vum536vbu1eszirljemgpsbx7ymws7'}
INDENT = 2

def get_response(query, payload=None):
    """
    Get response from twitch API call
    """
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS, params=payload)
    return response

# Save JSON data to file | ('filename.json')
def write_json(filename, data_json):
    with open(filename, 'w') as f:
        json.dump(data_json, f, indent=INDENT)

# Appends game data (json format) to a json file
# Replaces cursor key
def append_game_data_json(filename, data_json):
    with open(filename) as json_file:
        filedata = json.load(json_file)
        merged = filedata['data'] + data_json['data']
        filedata['data'] = merged
        filedata['pagination'] = data_json['pagination']
    write_json(filename, filedata)



top_games_list = []

# Gets games sorted by number of current viewers on Twitch, most popular first.
def get_top_games_query(pagination_nr=None, filename = 'top_streamed_games_query.json'):

    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('games/top', payload)

    # Save response to json file
    write_json(filename, response.json()) # Save response to json file

    
    for game in response.json()["data"]:
        top_games_list.append((int(game["id"]), game["name"]))

    while(response.json()["pagination"]):
        # Update cursor (pagination number)
        payload['after'] = response.json()["pagination"]["cursor"]
        response = get_response('games/top', payload)
        response_json = response.json()
        print(".", end=' ')
        append_game_data_json(filename, response_json)
    print("Done")

# Will itearte through all livestreams and acculumate the total view count per game
# 'Filename' usecase to be implemented
def get_view_count_of_games(filename, pagination_nr=None, view_counts={}, testcount=0):
    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('streams', payload)
    response_json = response.json()

    # Iteate through streams and add view_count
    for dict_item in response_json['data']:
        if dict_item['game_id'] in view_counts.keys():
            view_counts[dict_item['game_id']] += dict_item['viewer_count']
        else:
            view_counts[dict_item['game_id']] = dict_item['viewer_count']

    # Stop the functions once we are looking at streams with 1 viewer
    if 1 in view_counts.values():
        return 

    # Save view counts to file
    write_json('view_counts.json', view_counts)

    # If there exists more livestreams go to next page
    if (response.json()["pagination"]):
        payload['after'] = response.json()["pagination"]["cursor"]
        get_view_count_of_games(filename, pagination_nr=response.json()["pagination"]["cursor"], view_counts=view_counts, testcount=testcount)


get_top_games_query()

top_games_list = top_games_list.copy() + top_games_list
top_games_list = top_games_list.copy() + top_games_list
top_games_list = top_games_list.copy() + top_games_list
top_games_list = top_games_list.copy() + top_games_list
top_games_list = top_games_list.copy() + top_games_list
print(len(top_games_list))

import pyodbc 
server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver= '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
cursor = conn.cursor()
cursor.fast_executemany = True
sql_insert_query = """INSERT INTO games2 (gameid, gamename) 
                                VALUES (?, ?) """

cursor.executemany(sql_insert_query, top_games_list)
conn.commit()
print(cursor.rowcount, "Record inserted successfully into Laptop table")

cursor.close()
conn.close()
print("MySQL connection is closed")


#cursor.execute('SELECT * FROM testdatabase.dbo.salespromotions')
# for row in cursor:
#     print(row)

#get_view_count_of_games('test')

#get_top_games_query()

#print(get_access_token(CLIENT_ID, CLIENT_SECRET, GRANT_TYPE))


