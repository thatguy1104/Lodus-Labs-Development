from csv import reader
import requests
import json
import os
# good sourse: https://store.steampowered.com/stats/

class SteamList():
    def __init__(self, APIkey):
        self.filename = "./DATA(csv)/steam.csv"
        self.baseURL = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/'
        self.APIkey = APIkey

    def getSteamStatsForAGame(self, appID):
        header = {"Client-ID": self.APIkey}
        game_players_url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid=' + appID
        game_players = requests.get(game_players_url, headers=header).json()['response']['player_count']
        return game_players

    def readAPPID(self):
        name = []
        appID = []
        developer = []

        with open(self.filename, newline='') as csvfile:
            csv_reader = reader(csvfile)
            for row in csv_reader:
                name.append(row[1])
                appID.append(row[0])
                developer.append(row[4])
        return name, appID, developer

    def run(self):
        name, appID, developer = self.readAPPID()
        for i in range(10):
            count = self.getSteamStatsForAGame(appID[i])
            print("NAME : {0}, DEV: {1}, COUNT: {2}".format(name[i], developer[i], count))

