import requests
import json


clientID = '101976a4b31f8443deb71a89c9bb1a0842643288526cfb61'
url = 'GET https://mixer.com/api/v1/resources'

response = requests.get(url)
print(response.json())