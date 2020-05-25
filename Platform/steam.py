import requests
import json
import os

class SteamList():
    def __init__(self, APIkey):
        self.filename = "corp_info.json"
        self.baseURL = ' http://api.steampowered.com/ISteamUserStats/GetGlobalStatsForGame/v0001/?'
        self.parameter = {'appid': APIkey, 'name[0]': 'Minecraft'}

    def readCorpInfo(self):
        companies = []
        with open(self.filename) as json_file:
            data = json.load(json_file)
            for p in data['company']:
                companies.append(p)
        return companies
    
    def getSteamStats(self, companies):
        game_name = "Valve"
        response = requests.get(self.baseURL, params=self.parameter)
        print(response)

    def run(self):
        companies = self.readCorpInfo()
        self.getSteamStats(companies)

steam = SteamList('2C2C2E0FEBFD8D32F9346602D47C83BA')
steam.run()
