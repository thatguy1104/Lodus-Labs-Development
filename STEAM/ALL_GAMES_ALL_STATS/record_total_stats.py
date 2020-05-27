# Step 1: update app ids
# Step 2: iterate through OneGameData

from OneGameData.oneGameData import GameStats
from GetGameIDs.getGameIDs import GetGameID
import json

class GetAllRecordData():

    def __init__(self):
        self.writeFILE = 'recordsALLGameStats.json'
    
    def readGameIds(self):
        link_to_file = 'GetGameIDs/gameIDs.json'
        ids = []
        with open(link_to_file) as json_file:
            data = json.load(json_file)
            for p in data['Game ID + Name']:
                ids.append(p['Game ID'])
        return ids

    def writeToJSON(self, all_months, all_players, all_gains, all_percent_gains, all_peak_players):
        data = {}
        data['people'] = []
        data['people'].append({
            'name': 'Scott',
            'website': 'stackabuse.com',
            'from': 'Nebraska'
        })

        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)



    def getOneGameStats(self):
        get_all_ids = self.readGameIds()

        for i in range(len(get_all_ids)):
            one_game = GameStats(get_all_ids[i])
            all_months, all_players, all_gains, all_percent_gains, all_peak_players = one_game.getOneGameData()
            self.writeToJSON(all_months[i], all_players[i], all_gains[i], all_percent_gains[i], all_peak_players[i])

            for i in range(len(all_months)):
                print(all_months[i], all_players[i], all_gains[i], all_percent_gains[i], all_peak_players[i])

    def record(self):
        self.getOneGameStats()
