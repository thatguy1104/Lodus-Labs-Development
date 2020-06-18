import requests, json, sys

def get_access_token(client_id, client_secret, grant_type):
    """
    Returns oauth2 access token
    """
    r = requests.post('https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}'
    .format(client_id, client_secret, grant_type))
    r_json = r.json() # For debugging use: print(json.dumps(r_json, indent=INDENT))
    return(r_json['access_token'])

    