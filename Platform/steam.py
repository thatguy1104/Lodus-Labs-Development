import json
import os

class SteamList():
    def __init__(self):
        self.filename = "corp_info.json"

    def readCorpInfo(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            for p in data['company']:
                print(p)

steam = SteamList()
steam.readCorpInfo()
