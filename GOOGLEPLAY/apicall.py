import requests

url = "https://app-stores.p.rapidapi.com/details"

querystring = {"language": "en", "store": "google",
               "id": "com.snapchat.android"}

headers = {
    'x-rapidapi-host': "app-stores.p.rapidapi.com",
    'x-rapidapi-key': "7bc12ffb0amsh9aaa2f2708ed897p1c5b03jsn7f2a36b5e767"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)