from bs4 import BeautifulSoup
import requests
import lxml
import json


class GameStats():
    def __init__(self):
        self.link = 'https://steamcharts.com/app/730'

    def recieveData(self):
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, 'lxml')
        
        month = soup.find_all('td', class_='month-cell left italic') + \
            soup.find_all('td', class_='month-cell left')
        avg_players = soup.find_all('td', class_='right num-f italic') + \
            soup.find_all('td', class_='right num-f')
        
        gain = soup.find_all('td', class_='right num-p gainorloss italic loss')
        percent_gain = soup.find_all('td', class_='right gainorloss italic loss') + \
            soup.find_all('td', class_='right gainorloss gain')


        print(gain)
        
        
        peak_players = soup.find_all('td', class_='right num italic') + \
            soup.find_all('td', class_='right num')

        return month, avg_players, gain, percent_gain, peak_players

    def getOneGameData(self):
        month, avg_player, gain, percent_gain, peak_players = self.recieveData()
        all_months = []
        all_players = []
        all_gains = []
        all_percent_gains = []
        all_peak_players = []
        print(len(month), len(avg_player), len(gain), len(percent_gain), len(peak_players))
        
        # for i in range(len(month)):
        #     initial_1 = month[i].text.replace('\t', '')
        #     mid_1 = initial_1.replace('\n', '')
        #     all_months.append(mid_1)

        #     initial_2 = avg_player[i].text.replace('\t', '')
        #     mid_2 = initial_2.replace('\n', '')
        #     all_players.append(mid_2)

        #     initial_3 = gain[i].text.replace('\t', '')
        #     mid_3 = initial_3.replace('\n', '')
        #     all_gains.append(mid_3)

        #     initial_4 = percent_gain[i].text.replace('\t', '')
        #     mid_4 = initial_4.replace('\n', '')
        #     all_percent_gains.append(mid_4)

        #     initial_5 = peak_players[i].text.replace('\t', '')
        #     mid_5 = initial_5.replace('\n', '')
        #     all_peak_players.append(mid_5)
        

        print(all_peak_players)



stats = GameStats()
stats.getOneGameData()
