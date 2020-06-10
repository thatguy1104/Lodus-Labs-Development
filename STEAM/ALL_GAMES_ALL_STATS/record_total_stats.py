# Step 1: update app ids
# Step 2: iterate through OneGameData

from OneGameData.oneGameData import GameStats
import json
import psycopg2

hostname = 'localhost'~
username = 'postgres'
password = 'analytcis_123'
database = 'project_data'

class GetAllRecordData():

    def __init__(self):
        self.writeFILE = 'ALL_GAMES_ALL_STATS/recordsAllGameStats.json'
    
    def readGameIds(self):
        link_to_file = 'ALL_GAMES_ALL_STATS/gameIDs.json'
        ids = []
        names = []
        with open(link_to_file) as json_file:
            data = json.load(json_file)
            for p in data['Game ID + Name']:
                ids.append(p['Game ID'])
                names.append(p['Game Name'])
        return names, ids

    def getOneGameStats(self):
        names, get_all_ids = self.readGameIds()

        data = {}

        for i in range(len(names)):
            data[get_all_ids[i]] = []
            one_game = GameStats(get_all_ids[i])
            all_months, all_players, all_gains, all_percent_gains, all_peak_players = one_game.getOneGameData()

            # Convert list of strings to list of integers
            all_players = [float(i) for i in all_players]
            all_peak_players = [int(i) for i in all_peak_players]

            gains_converted = []
            for item in all_gains:
                try:
                    gains_converted.append(float(item))
                except ValueError as e:
                    gains_converted.append(item)

        with open(self.writeFILE, 'w') as outfile:
            json.dump(data, outfile)

    def record(self):
        self.getOneGameStats()
