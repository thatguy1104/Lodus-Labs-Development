import requests, json, sys
import twitch_oauth2_access_token_generator
from . import credentials

INDENT = 2
BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = 'lgb4dq2tni1ce2ib9gzmg0kp571lgz'
CLIENT_SECRET = '3j58umfzeu2mve615u3mkfwogfamy1'
GRANT_TYPE = 'client_credentials'
HEADERS = { 'Client-ID': CLIENT_ID, 
            'Client-Secret': CLIENT_SECRET,
            'Authorization': 'Bearer ' + get_access_token(CLIENT_ID,CLIENT_SECRET,GRANT_TYPE)}

def get_access_token(client_id, client_secret, grant_type):
    """
    Returns oauth2 access token
    """
    r = requests.post('https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}'
    .format(client_id, client_secret, grant_type))
    r_json = r.json() # For debugging use: print(json.dumps(r_json, indent=INDENT))
    return(r_json['access_token'])

def get_response(query, payload=None):
    """
    Get response from twitch API call
    """
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS, params=payload)
    return response

def get_top_games_query():
    """
    Gets games sorted by number of current viewers on Twitch, most popular first.
    Returned in a list of 2-tuples [(game_id, game_name),,,,]
    """
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

    print("Done with top games list")
    return top_games_list

def get_view_count_of_games(pagination_nr=None, view_counts={}):
    """
    Iteartes through all livestreams and sums the total view count per game
    """
    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('streams', payload)
    response_json = response.json()

    # Iteate through streams and add view_count
    for dict_item in response_json['data']:
        if dict_item['game_id'] in view_counts.keys():
            view_counts[dict_item['game_id']] += dict_item['viewer_count']
        else:
            view_counts[dict_item['game_id']] = dict_item['viewer_count']

    # Stop the functions once we are looking at streams with 3 viewer
    if 3 in view_counts.values():
        return list(view_counts.items())

    if (response.json()["pagination"]):  # If there exists more livestreams go to next page
        payload['after'] = response.json()["pagination"]["cursor"]
        get_view_count_of_games(pagination_nr=response.json()["pagination"]["cursor"], view_counts=view_counts)
    return list(view_counts.items())

def run():
    run_function = True

print(HEADERS)

# import pyodbc 
# server = 'serverteest.database.windows.net'
# database = 'testdatabase'
# username = 'login12391239'
# password = 'HejsanHejsan!1'
# driver= '{ODBC Driver 17 for SQL Server}'

# conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
# cursor = conn.cursor()
# cursor.fast_executemany = True
# sql_insert_query = """INSERT INTO games2 (gameid, gamename) 
#                                 VALUES (?, ?) """

# cursor.executemany(sql_insert_query, top_games_list)
# conn.commit()
# print(cursor.rowcount, "Record inserted successfully into Laptop table")

# cursor.close()
# conn.close()
# print("MySQL connection is closed")


#cursor.execute('SELECT * FROM testdatabase.dbo.salespromotions')
# for row in cursor:
#     print(row)

#get_view_count_of_games('test')

#get_top_games_query()

#print(get_access_token(CLIENT_ID, CLIENT_SECRET, GRANT_TYPE))


# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def write_json(file_json, data_json):
    """
    Writes JSON data to a json file
    (filename.json)
    """
    with open(file_json, 'w') as f:
        json.dump(data_json, f, indent=INDENT)

# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def append_game_data_json(file_json, data_json):
    """
    Appends game data (json format) to a json file
    Replaces cursor key
    """
    with open(file_json) as f:
        filedata = json.load(f)

        merged = filedata['data'] + data_json['data']

        filedata['data'] = merged
        filedata['pagination'] = data_json['pagination']

    write_json(file_json, filedata) # save file 

# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def get_top_games_queryOLD(pagination_nr=None, filename = 'get_top_games_query.json'):
    """
    Gets games sorted by number of current viewers on Twitch, most popular first.
    'filename' determines name of file where data is saved
    'pagination_nr' determines what page to start calling data from
    """

    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('games/top', payload)

    # Save response to json file
    write_json(filename, response.json()) # Save response to json file

    while(response.json()["pagination"]):
        payload['after'] = response.json()["pagination"]["cursor"]
        response = get_response('games/top', payload)
        response_json = response.json()
    print("Done")

# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def get_view_count_of_gamesOLD(filename, pagination_nr=None, view_counts={}, testcount=0):
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