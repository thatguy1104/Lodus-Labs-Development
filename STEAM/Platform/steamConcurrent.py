from bs4 import BeautifulSoup
import requests
import lxml
import json

class steamConcurrent():
    def __init__(self):
        self.linkGeneral = 'https://store.steampowered.com/stats/'
        self.linkAll = 'https://steamcharts.com/top/p.1'
        self.response = requests.get(self.linkGeneral)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.filenameWRITE = './DATA(json)/top100GamesByPlayers.json'

    def getConcurrent(self):
        all_current = self.soup.find_all('span', class_ = 'statsTopHi')
        current = all_current[0].text.replace(',', '')
        peak_today = all_current[1].text.replace(',', '')

        return int(current), int(peak_today)

    def getTopGamesByPlayerCount(self):
        response = requests.get(self.linkAll)
        soup = BeautifulSoup(response.text, 'lxml')

        names = soup.find_all('td', class_='game-name left')

        all_game_names = []
        for tittle in names:
            game_name = tittle.find('a')
            raw = game_name.text.replace('\t', '')
            final = raw.replace('\n', '')
            all_game_names.append(final)
        
        print(all_game_names)
        # return name, current, peak, hours_played

    def writeToJSON(self):
        data = {}
        data['Concurrent Steam Data'] = []
        data['General Data'] = []
        total_current, total_peak = self.getConcurrent()
        name, current, peak, hours_played = self.getTopGamesByPlayerCount()

        for i in range(len(name)):
            print("Writing item ", i)
            data['Concurrent Steam Data'].append({
                'Game Name' : name[i].text,
                'Current Players' : current[i].text,
                'Peak Today' : peak[i].text,
                'Hours Played' : hours_played[i].text
            })

        data['General Data'].append({
            'Current Total Players': total_current,
            'Current Total Peak': total_peak
        })

        with open(self.filenameWRITE, 'w') as outfile:
            json.dump(data, outfile)
            
