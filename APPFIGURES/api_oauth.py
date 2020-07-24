""" Demonstrates using the rauth library to interact with
    the Appfigures API
"""

from rauth import OAuth1Session, OAuth1Service


base_url = "https://api.appfigures.com/v2/data/countries?client_key=5f535edf1194429095216a6d05b3343b"
client_key = "5f535edf1194429095216a6d05b3343b"
client_secret = "28e000e4ec6d43018c674f7822346b3b"


request_token_url = base_url + "/oauth/request_token"
authorize_url = base_url + "/oauth/authorize"
access_token_url = base_url + "/oauth/access_token"

def get_service():
  """ Returns an OAuthService configured for us """
  return OAuth1Service(name="appfigures",
                        consumer_key=client_key,
                        consumer_secret=client_secret,
                        request_token_url=request_token_url,
                        access_token_url=access_token_url,
                        authorize_url=authorize_url,
                        base_url=base_url)


def get_session(access_token=None, access_token_secret=None):
  """If access_token and secret are given, create and return a session.

      If they are not given, go through the authorization process
      interactively and return the new session
  """
  oauth = get_service()

  if access_token:
    session = OAuth1Session(client_key, client_secret,
                            access_token, access_token_secret,
                            service=oauth)
    return session

  params = {"oauth_callback": "oob"}
  headers = {'X-OAuth-Scope': 'public:read,products:read'}
  request_token, request_token_secret = oauth.get_request_token(
                                          params=params,
                                          headers=headers
                                        )

  authorization_url = oauth.get_authorize_url(request_token)
  print("Go here: %s to get your verification token."
          % authorization_url)
  verifier = raw_input("Paste verifier here: ")
  session =  oauth.get_auth_session(request_token, 
                                    request_token_secret,
                                    "POST",
                                    data={"oauth_verifier":verifier})
  return session


if __name__ == "__main__":
  s = get_session()
  print("Access Token: %s\tAccess Secret:%s"
          % (s.access_token, s.access_token_secret))
  resp = s.get(base_url + "/products/mine")
  print([ product['name'] for (id, product) in resp.json().items()])

  # it is VERY important that querystring parameters go in params
  # rather than directly put in the URL. rauth will not sign the request
  # correctly if you did s.get(base_url+"products/mine?store=apple")
  resp = s.get(base_url + "/products/mine", params=dict(store="apple"))
  print([ product['name'] for (id, product) in resp.json().items()])

  resp = s.get(base_url + "/reports/sales/products")
  print("Status code(%s) should be 403 because of scope" %
          resp.status_code)