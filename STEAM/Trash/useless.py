from csv import reader
import requests
import json
import os

class SteamList():
    def __init__(self, APIkey):
        # Relative file paths
        self.filenameREAD = "./DATA(csv)/steam.csv"
        self.filenameWRITE = "./DATA(json)/processedSteamData.json"
        self.baseURL = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/'
        self.APIkey = APIkey

    def getSteamStatsForAGame(self, appID):
        # Only gets the live_player count for a particular game (of appID)
        header = {"Client-ID": self.APIkey}
        game_players_url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid=' + appID
        game_players = requests.get(game_players_url, headers=header).json()['response']['player_count']
        return game_players

    def readAPPID(self):
        name = []
        appID = []
        developer = []
        live_players = []
        pos_rating = []
        neg_rating = []
        average_play_time = []
        length = 0

        # READ the data, isolate necessary information
        with open(self.filenameREAD, newline='') as csvfile:
            csv_reader = reader(csvfile)
            for row in csv_reader:
                name.append(row[1])
                appID.append(row[0])
                developer.append(row[4])
                pos_rating.append(row[12])
                neg_rating.append(row[13])
                average_play_time.append(row[14])
        return name, appID, developer, pos_rating, neg_rating, average_play_time

    def writeToJSON(self):
        data = {}
        data['games'] = []
        name, appID, developer, pos_rating, neg_rating, average_play_time = self.readAPPID()

        for i in range(1, len(name) - 1):
            print("Writing item ", i)
            count = self.getSteamStatsForAGame(appID[i])
            data['games'].append({
                'appID'             : appID[i],
                'name'              : name[i],
                'developer'         : developer[i],
                'live_players'      : count,
                'positive_ratings'  : pos_rating[i],
                'negative_ratings'  : neg_rating[i],
                'average_play_time' : average_play_time[i]
            })

        with open(self.filenameWRITE, 'w') as outfile:
            json.dump(data, outfile)

    def displaySteamData(self, count):
        name, appID, developer, pos_rating, neg_rating, average_play_time = self.readAPPID()
        if count <= len(name):
            for i in range(1, count + 1):
                count = self.getSteamStatsForAGame(appID[i])
                print("NAME: {0}, DEV: {1}, COUNT: {2}, POS: {3}, NEG: {4}, AVG: {5}".format(
                    name[i], developer[i], count, pos_rating[i], neg_rating[i], average_play_time[i]))
        else:
            raise Exception("Number of games exceeds maximum")

