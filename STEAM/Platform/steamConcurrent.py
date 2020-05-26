from bs4 import BeautifulSoup
import requests
import lxml
import json

class steamConcurrent():
    def __init__(self):
        self.linkGeneral = 'https://store.steampowered.com/stats/'
        self.linkAll = 'https://steamcharts.com/top/p.'
        self.response = requests.get(self.linkGeneral)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.filenameWRITE = './DATA(json)/top100GamesByPlayers.json'

    def getConcurrent(self):
        all_current = self.soup.find_all('span', class_ = 'statsTopHi')
        current = all_current[0].text.replace(',', '')
        peak_today = all_current[1].text.replace(',', '')

        return int(current), int(peak_today)

    def getTopGamesByPlayerCount(self, page):
        link = self.linkAll + str(page)
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')

        all_rows = soup.find_all('tr')

        all_game_names = []
        current_players = []
        peak_players = []
        hours_played = []

        names = soup.find_all('td', class_='game-name left')
        current_p = soup.find_all('td', class_='num')

        for tittle in names:
            game_name = tittle.find('a')
            # Process the weirdly formatted string output for NAMES
            raw = game_name.text.replace('\t', '')
            final = raw.replace('\n', '')
            all_game_names.append(final)
        
        for player in current_p:
            peaks = soup.find_all('td', class_='num period-col peak-concurrent')
            hours = soup.find_all('td', class_='num period-col player-hours')
            if (player not in peaks) and (player not in hours):
                current_players.append(player.text)

        for i in range(len(peaks)):
            peak_players.append(peaks[i].text)
        for i in range(len(hours)):
            hours_played.append(hours[i].text)
        
        return all_game_names, current_players, peak_players, hours_played

    def writeToJSON(self):
        data = {}
        data['Concurrent Steam Data'] = []
        data['General Data'] = []
        total_current, total_peak = self.getConcurrent()
        name, current, peak, hours_played = self.getTopGamesByPlayerCount(1)

        for i in range(len(name)):
            print("Writing item ", i)
            data['Concurrent Steam Data'].append({
                'Game Name' : name[i],
                'Current Players' : current[i],
                'Peak Today' : peak[i],
                'Hours Played' : hours_played[i]
            })

        data['General Data'].append({
            'Current Total Players': total_current,
            'Current Total Peak': total_peak
        })

        with open(self.filenameWRITE, 'w') as outfile:
            json.dump(data, outfile)
            
