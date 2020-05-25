import requests
import json
import time

class SteamBandwidth():
    def __init__(self, weird_num):
        self.url = 'https://steamcdn-a.akamaihd.net/steam/publicstats/download_traffic_per_country.jsonp?v=' + \
            time.strftime("%m-%d-%Y") + str(weird_num)
        self.response = requests.get(self.url).text
        self.bandwidthFILENAME = './DATA(json)/bandwidthSteamData.json'

    def setup(self):
        startidx = self.response.find('(')
        endidx = self.response.find(')')
        bandwidthFile = json.loads(self.response[startidx + 1:endidx])
        print(bandwidthFile['USA']['totalbytes'])

        for name in bandwidthFile:
            if type(bandwidthFile[name]['totalbytes']) == str:
                bandwidthFile[name]['totalbytes'] = int(bandwidthFile[name]['totalbytes'])
            if type(bandwidthFile[name]['avgmbps']) == str:
                bandwidthFile[name]['avgmbps'] = int(bandwidthFile[name]['avgmbps'])
        return bandwidthFile

    def writeBandwidthSteam(self):
        bandwidthFile = self.setup()
        with open(self.bandwidthFILENAME, 'w') as outfile:
            json.dump(bandwidthFile, outfile)
