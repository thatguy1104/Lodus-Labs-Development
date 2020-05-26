import requests, json, sys

BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = 'lgb4dq2tni1ce2ib9gzmg0kp571lgz'
CLIENT_SECRET = '3j58umfzeu2mve615u3mkfwogfamy1'
HEADERS = { 'Client-ID': CLIENT_ID, 
            'Client-Secret': CLIENT_SECRET,
            'Token-Type': "bearer"}
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

user_login = 'ninja'
query = get_user_streams_query(user_login)
response = get_response(query)
print_response(response)

GET https://id.twitch.tv/oauth2/authorize
    ?client_id=<your client ID>
    &redirect_uri=<your registered redirect URI>
    &response_type=<type>
    &scope=<space-separated list of scopes> 