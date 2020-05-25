import requests
import json
import time
import math

class SteamBandwidth():
    def __init__(self, weird_num):
        self.url = 'https://steamcdn-a.akamaihd.net/steam/publicstats/download_traffic_per_country.jsonp?v=' + \
            time.strftime("%m-%d-%Y") + str(weird_num)
        self.response = requests.get(self.url).text
        self.bandwidthFILENAME = './DATA(json)/bandwidthSteamData.json'

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        for count in ['Bytes', 'KB', 'MB', 'GB']:
            if size_bytes > -1024.0 and size_bytes < 1024.0:
                print ("%3.1f%s" % (size_bytes, count))
            size_bytes /= 1024.0
        print("%3.1f%s" % (size_bytes, 'TB'))

    def setup(self):
        startidx = self.response.find('(')
        endidx = self.response.find(')')
        bandwidthFile = json.loads(self.response[startidx + 1:endidx])

        for name in bandwidthFile:
            total = 0
            if type(bandwidthFile[name]['totalbytes']) == str:
                bandwidthFile[name]['totalbytes'] = int(bandwidthFile[name]['totalbytes'])
                scale = bandwidthFile[name]['totalbytes']
                # grand_total += bandwidthFile[name]['totalbytes']
            if type(bandwidthFile[name]['avgmbps']) == str:
                bandwidthFile[name]['avgmbps'] = int(bandwidthFile[name]['avgmbps'])
        return bandwidthFile

    def writeBandwidthSteam(self):
        grand_total = 12000
        self.convert_size(grand_total)
        # bandwidthFile = self.setup()
        # with open(self.bandwidthFILENAME, 'w') as outfile:
        #     json.dump(bandwidthFile, outfile)
