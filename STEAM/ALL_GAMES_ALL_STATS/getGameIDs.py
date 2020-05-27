from bs4 import BeautifulSoup
import requests
import lxml
import json


class GetGameID():
    def __init__(self):
        self.linkGeneral = 'https://store.steampowered.com/stats/'
        self.linkAll = 'https://steamcharts.com/top/p.'
        self.response = requests.get(self.linkGeneral)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.filenameWRITE = 'OneGameData/gameIDs.json'
        self.total_pages = 0

    def getTopGamesByPlayerCount(self, page):
        link = self.linkAll + str(page)
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')

        all_rows = soup.find_all('tr')
        all_game_names = []
        all_game_id = []

        names = soup.find_all('td', class_='game-name left')
        current_p = soup.find_all('td', class_='num')

        for tittle in names:
            game_name = tittle.find('a')

            # Record game IDs for Detailed Scraping by OneGameData
            app_id = tittle.find('a')['href']
            all_game_id.append(app_id)

            # Process the weirdly formatted string output for NAMES
            raw = game_name.text.replace('\t', '')
            final = raw.replace('\n', '')
            all_game_names.append(final)

        return all_game_names, all_game_id

    def updateJSON(self, pages):
        self.total_pages = pages
        data = {}
        data['Game ID + Name'] = []

        for p in range(1, pages):
            print("Writing page ", p)
            name, game_id = self.getTopGamesByPlayerCount(p)
            for i in range(len(name)):
                data['Game ID + Name'].append({
                    'Game Name': name[i],
                    'Game ID': game_id[i]
                })

        with open(self.filenameWRITE, 'w') as outfile:
            json.dump(data, outfile)

