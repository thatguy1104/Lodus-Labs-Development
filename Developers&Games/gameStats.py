import requests
import json
from bs4 import BeautifulSoup
import lxml

class AllGamesForDev():
    def __init__(self):
        self.link = 'https://www.androidrank.org'
        self.writeFILE = 'allStats.json'
        self.readFILE = 'devRanks.json'

    def scrapeOne(self, id):
        response = requests.get(self.link + id)
        soup = BeautifulSoup(response.text, 'lxml')

        odd = soup.find_all('tr', class_='odd')
        even = soup.find_all('tr', class_='even')
        all_rows = odd + even

        results = []
        for item in all_rows:
            row = item.find_all('td')
            rank = int(row[0].text.replace('.', ''))
            tittle = row[1].text.replace('\n', '')
            rating = row[3].text
            intalls = row[4].text
            avg_rating = float(row[5].text)
            growth_30_days = row[6].text
            growth_60_days = row[7].text
            price = row[8].text.replace('\n', '')
            results.append((rank, tittle, rating, intalls, avg_rating, growth_30_days, growth_60_days, price))
        return results

    def getIDs(self):
        ids = []
        with open(self.readFILE) as json_file:
            data = json.load(json_file)
            for p in data:
                ids.append(data[p][0]['Link'])
        return ids

    def getAllGameStats(self):
        data = {}
        ids = self.getIDs()

        for dev in range(len(ids)):
            resultOne = self.scrapeOne(ids[dev])
            print("Writing {0} / {1}".format(dev, len(ids)))
            for i in range(len(resultOne)):
                data[resultOne[i][1]] = []
                data[resultOne[i][1]].append({
                    'Rank'              : resultOne[i][0],
                    'App Name'          : resultOne[i][1],
                    'Total Rating'      : resultOne[i][2],
                    'Installs'          : resultOne[i][3],
                    'Average Rating'    : resultOne[i][4],
                    'Growth: 30 days'   : resultOne[i][5],
                    'Growth: 60 days'   : resultOne[i][6],
                    'Price'             : resultOne[i][7]
                })

        with open(self.writeFILE, 'w') as outfile:
            json.dump(data, outfile)

obj = AllGamesForDev()
obj.getAllGameStats()
