import requests
import json
import time
import math

class SteamBandwidth():
    def __init__(self, weird_num):
        self.url = 'https://steamcdn-a.akamaihd.net/steam/publicstats/download_traffic_per_country.jsonp?v=' + \
            time.strftime("%m-%d-%Y") + str(weird_num)
        self.response = requests.get(self.url).text
        self.bandwidthFILENAME = 'bandwidthSteamData.json'

    def setup(self):
        # Remove JSONP function name and braces, conversion to JSON format
        startidx = self.response.find('(')
        endidx = self.response.find(')')
        bandwidthFile = json.loads(self.response[startidx + 1:endidx])

        grand_total = 0

        for name in bandwidthFile:
            if type(bandwidthFile[name]['totalbytes']) == str:
                bandwidthFile[name]['totalbytes'] = int(bandwidthFile[name]['totalbytes'])
            
            # Add to total for traffic percentage per country insight
            grand_total += bandwidthFile[name]['totalbytes']
            if type(bandwidthFile[name]['avgmbps']) == str:
                bandwidthFile[name]['avgmbps'] = int(bandwidthFile[name]['avgmbps'])
        
        # Calculate additional insights
        for name in bandwidthFile:
            bandwidthFile[name]['Percentage of global Steam Traffic'] = []
            percentage = (bandwidthFile[name]['totalbytes'] / grand_total) * 100
            number = round(percentage, 2)
            bandwidthFile[name]['Percentage of global Steam Traffic'] = number

        return bandwidthFile

    def writeBandwidthSteam(self):
        bandwidthFile = self.setup()
        with open(self.bandwidthFILENAME, 'w') as outfile:
            json.dump(bandwidthFile, outfile)
