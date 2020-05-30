import requests
import json
from bs4 import BeautifulSoup
import lxml

class DevelopersGames():
    def __init__(self):
        self.startLink = 'https://www.androidrank.org/developers/ranking?&start=1'
        self.endLink = 'https://www.androidrank.org/developers/ranking?&start=1341'

    def scrape(self):
        response = requests.get(self.startLink)
        soup = BeautifulSoup(response.text, 'lxml')

        odd = soup.find_all('tr', class_='odd')
        even = soup.find_all('tr', class_='even')
        all_rows =  odd + even
        
        results = []
        for item in all_rows:
            row = item.find_all('td')
            # Get: Rank, Developer, Total ratings, Total installs, Applications, Average rating
            rank = int(row[0].text.replace('.', ''))
            ratings = int(row[2].text.replace(',', ''))
            installs = int(row[3].text.replace(',', ''))
            applications = int(row[4].text)
            avg_rating = float(row[5].text)
            results.append((rank, row[1].text, ratings, installs, applications, avg_rating))
        
        results = sorted(results, key=lambda x: x[0])
        return results
        
    def writeToJSON(self, data_list):
        data = {}

        for i in range(len(data_list)):
            data[data_list[i][1]] = []
            data[data_list[i][1]].append({
                'Rank'              : data_list[i][0],
                'Developer'         : data_list[i][1],
                'Total Ratings'     : data_list[i][2],
                'Total installs'    : data_list[i][3],
                'Applications'      : data_list[i][4],
                'Average rating'    : data_list[i][5]
            })

        with open('results.json', 'w') as outfile:
            json.dump(data, outfile)

obj = DevelopersGames()
results = obj.scrape()
obj.writeToJSON(results)
