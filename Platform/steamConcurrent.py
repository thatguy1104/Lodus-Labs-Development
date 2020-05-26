from bs4 import BeautifulSoup
import requests
import lxml
import json

class steamConcurrent():
    def __init__(self):
        self.link = 'https://store.steampowered.com/stats/'
        self.response = requests.get(self.link)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.filenameWRITE = './DATA(json)/top100GamesByPlayers.json'

    def getConcurrent(self):
        all_current = self.soup.find_all('span', class_ = 'statsTopHi')
        current = all_current[0].text.replace(',', '')
        peak_today = all_current[1].text.replace(',', '')

        return int(current), int(peak_today)

    def getTopGamesByPlayerCount(self):
        row = self.soup.find_all('tr', class_='player_count_row')

        alldata = self.soup.find_all('span', class_='currentServers')
        current = alldata[::2]
        peak = alldata[1::2]
        name = self.soup.find_all('a', class_='gameLink')

        return current, peak, name

    def writeToJSON(self):
        data = {}
        data['Concurrent Steam Data'] = []
        data['General Data'] = []
        current, peak, name = self.getTopGamesByPlayerCount()
        total_current, total_peak = self.getConcurrent()

        for i in range(len(name)):
            print("Writing item ", i)
            data['Concurrent Steam Data'].append({
                'Game Name' : name[i].text,
                'Current Players' : current[i].text,
                'Peak Today' : peak[i].text
            })

        data['General Data'].append({
            'Current Total Players': total_current,
            'Current Total Peak': total_peak
        })

        with open(self.filenameWRITE, 'w') as outfile:
            json.dump(data, outfile)
            
