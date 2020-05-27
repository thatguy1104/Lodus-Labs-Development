import requests, json, sys

BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = 'lgb4dq2tni1ce2ib9gzmg0kp571lgz'
CLIENT_SECRET = '3j58umfzeu2mve615u3mkfwogfamy1'
GRANT_TYPE = 'client_credentials'
HEADERS = { 'Client-ID': CLIENT_ID, 
            'Client-Secret': CLIENT_SECRET,
            'Authorization': 'Bearer t5gsvxikp6cnmfqmde9e0lncus8ejs'}
INDENT = 2


def get_response(query):
    """
    Get response from twitch API call
    """
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS)
    return response

def print_response(response):
    """
    Print reponse with JSON for debugging
    """
    response_json = response.json()
    print_response = json.dumps(response_json, indent=INDENT)
    print(print_response)

def get_user_streams_query(user_login):
    """
    Pass in a twitch username and get user's current live stream info
    """
    return 'streams?user_login={0}'.format(user_login)

def get_user_query(user_login):
    """
    Get user info by passing in twitch username
    """
    return 'streams?login={0}'.format(user_login)

def get_user_videos_query(user_id):
    """
    Get videos on user's page, returns first 50
    """
    return 'videos?user_login={0}&first=50'.format(user_id)

def get_games_query():
  return 'games/top'

def get_oath2_verification():
    test = 0
    return test

#user_login = 'ninja'
#query = get_user_streams_query(user_login)
#response = get_response(query)
#print(response.url)
#print_response(response)

x = requests.get('https://api.twitch.tv/helix/games/top', headers=HEADERS)
#print_response(x)
y = x.json()

data = y
with open('test.json', 'w') as f:
    json.dump(y, f, indent=INDENT)
print(y["data"][0]["name"])

#r = requests.post('https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}'.format(CLIENT_ID, CLIENT_SECRET, GRANT_TYPE))
#r_json = r.json()
#print(json.dumps(r_json, indent=INDENT))