import requests
import json
from bs4 import BeautifulSoup
import lxml

class DevelopersGames():
    def __init__(self):
        self.startLink = 'https://www.androidrank.org/developers/ranking?&start='
        self.writeFILE = 'devRanks.json'

    def scrape(self, page):
        response = requests.get(self.startLink + page)
        soup = BeautifulSoup(response.text, 'lxml')

        odd = soup.find_all('tr', class_='odd')
        even = soup.find_all('tr', class_='even')
        all_rows =  odd + even
        
        results = []
        for item in all_rows:
            row = item.find_all('td')
            link = item.find('a')['href']
            # Get: Rank, Developer, Total ratings, Total installs, Applications, Average rating
            rank = int(row[0].text.replace('.', ''))
            ratings = int(row[2].text.replace(',', ''))
            installs = int(row[3].text.replace(',', ''))
            applications = int(row[4].text)
            avg_rating = float(row[5].text)
            results.append((rank, row[1].text, ratings, installs, applications, avg_rating, link))
        
        results = sorted(results, key=lambda x: x[0])
        return results
        
    def writeToDB(self):
        data = {}
        start_page = 1
        counter = 1
        end_page = 1341

        while start_page != end_page:
            print("Writing {0} / {1} pages".format(start_page, end_page))
            data_list = self.scrape(str(start_page))
            for i in range(len(data_list)):
                data[data_list[i][1]] = []
                data[data_list[i][1]].append({
                    'Rank'              : data_list[i][0],
                    'Developer'         : data_list[i][1],
                    'Link'              : data_list[i][6],
                    'Total Ratings'     : data_list[i][2],
                    'Total installs'    : data_list[i][3],
                    'Applications'      : data_list[i][4],
                    'Average rating'    : data_list[i][5],
                    'List of Games:'    : []
                })
            start_page += 20
            counter += 1

        with open(self.writeFILE, 'w') as outfile:
            json.dump(data, outfile)
