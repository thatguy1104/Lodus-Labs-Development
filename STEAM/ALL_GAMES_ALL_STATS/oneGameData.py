from bs4 import BeautifulSoup
import requests
import lxml
import json

class GameStats():
    def __init__(self, gameID):
        self.GameID = gameID
        self.link = 'https://steamcharts.com/' + gameID
        self.writeFILE = 'OneGameData/oneGameStats.json'

    def recieveData(self):
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, 'lxml')

        month = soup.find_all('td', class_='month-cell left italic') + \
            soup.find_all('td', class_='month-cell left')
        avg_players = soup.find_all('td', class_='right num-f italic') + \
            soup.find_all('td', class_='right num-f')     
        peak_players = soup.find_all('td', class_='right num italic') + \
            soup.find_all('td', class_='right num')

        gain = []
        percent_gain = []

        # Get line input from the table
        whole_line = []
        one_tr = soup.find_all('tr')
        for r in one_tr:
            line = r.text.replace('\t', '').replace('\n\n', '')
            if line is not '' and line is not '\n':
                whole_line.append(line)

        # Parse out the gain + percent gain column from the row data
        for i in range(1, len(whole_line)):
            one = whole_line[i].split('\n')
            if len(one) == 7:    
                gain.append(one[2])
                percent_gain.append(one[3])
            else:
                gain.append(one[1])
                percent_gain.append(one[2])

        return month, avg_players, gain, percent_gain, peak_players

    def getOneGameData(self):
        month, avg_player, gain, percent_gain, peak_players = self.recieveData()
        all_months = []
        all_players = []
        all_gains = []
        all_percent_gains = []
        all_peak_players = []
        
        for i in range(len(month)):
            initial_1 = month[i].text.replace('\t', '')
            mid_1 = initial_1.replace('\n', '')
            all_months.append(mid_1)

            initial_2 = avg_player[i].text.replace('\t', '')
            mid_2 = initial_2.replace('\n', '')
            all_players.append(mid_2)

            all_gains.append(gain[i])
            
            all_percent_gains.append(percent_gain[i])

            initial_5 = peak_players[i].text.replace('\t', '')
            mid_5 = initial_5.replace('\n', '')
            all_peak_players.append(mid_5)

        return all_months, all_players, all_gains, all_percent_gains, all_peak_players

    # def writeToJSON(self):
    #     all_months, all_players, all_gains, all_percent_gains, all_peak_players = self.getOneGameData()

    #     data = {}
    #     data['One Game Data'] = []

    #     for i in range(len(all_months)):    
    #         print('Writing {0} out of {1}'.format(i, len(all_months)))
    #         data['One Game Data'].append({
    #             'Game ID'       : self.GameID,
    #             'Month'         : all_months,
    #             'Avg. Players'  : all_players,
    #             'Gains'         : all_gains,
    #             '\% Gains'      : all_percent_gains,
    #             'Peak Players'  : all_peak_players
    #         })

    #     with open(self.writeFILE, 'w') as outfile:
    #         json.dump(data, outfile)


