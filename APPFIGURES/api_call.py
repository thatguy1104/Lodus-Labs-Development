import requests
import json

key = '5f535edf1194429095216a6d05b3343b'
secret_key = '28e000e4ec6d43018c674f7822346b3b'

url = 'https://api.appfigures.com/v2/data/countries?client_key=5f535edf1194429095216a6d05b3343b'

response = requests.get(url, auth=('zcabukh@ucl.ac.uk', 'hakalbert0')).json()

with open('results.json', 'w') as outfile:
    json.dump(response, outfile, indent=5)


# class AppFigures:
#     def __init__(self):
#         super().__init__()
