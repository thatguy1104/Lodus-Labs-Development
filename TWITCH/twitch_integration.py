import requests, json, sys

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
    return

# Appends game data (json format) to a json file
# Replaces cursor key
def append_game_data_json(filename, data_json):
    with open(filename) as json_file:
        filedata = json.load(json_file)
        merged = filedata['data'] + data_json['data']
        filedata['data'] = merged
        filedata['pagination'] = data_json['pagination']
    write_json(filename, filedata)
    return


# Gets games sorted by number of current viewers on Twitch, most popular first.
def get_top_games_query(pagination_nr=None, filename = 'top_streamed_games_query.json'):
    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('games/top', payload)

    # Save response to json file
    write_json(filename, response.json())

    # If there exists more game pages continue iterating 
    while(response.json()["pagination"]):
        # Update cursor (pagination number)
        payload['after'] = response.json()["pagination"]["cursor"]
        response = get_response('games/top', payload)
        response_json = response.json()
        print("Appending page")
        append_game_data_json(filename, response_json)
    print("Done")
    return
    
get_top_games_query()

# Returns oauth2 access token
def get_access_token(client_id, client_secret, grant_type):
    r = requests.post('https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}'
    .format(client_id, client_secret, grant_type))
    r_json = r.json()
    #print(json.dumps(r_json, indent=INDENT))
    #print(r_json['access_token'])
    return(r_json['access_token'])

#print(get_access_token(CLIENT_ID, CLIENT_SECRET, GRANT_TYPE))


