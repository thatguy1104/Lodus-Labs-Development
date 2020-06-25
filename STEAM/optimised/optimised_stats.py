from bs4 import BeautifulSoup
import requests
import lxml
import json
import datetime


class OptimisedGameStats():
    def __init__(self, gameID):
        self.GameID = gameID
        self.link = 'https://steamcharts.com/' + gameID
        self.writeFILE = 'OneGameData/oneGameStats.json'

    def recieveData(self):
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, 'lxml')

        tabl = soup.find('table', class_='common-table')
        table_body = tabl.find('tbody')
        rows = table_body.find_all('tr')
        two_rows = []
        month = []
        avg_players = []
        gain = []
        percent_gain = []
        peak_players = []
        result = []

        # SPECIFY NUMBER OF PREVIOUS MONTHS TO INCLUDE IN THE SCRAPE DATA
        rows_to_record = 1

        count_rows = 0
        if len(rows) != 0:
            for i in range(0, len(rows)):
                if count_rows <= rows_to_record:
                    two_rows.append(rows[i])
                    count_rows += 1

        for i in two_rows:
            td_s = i.find_all('td')
            row_elements = []
            for j in td_s:
                line = j.text.replace('\t', '').replace('\n', '').replace('\n\n', '')
                row_elements.append(line)

            month.append(row_elements[0])
            avg_players.append(row_elements[1])

            try:
                gain.append(float(row_elements[2]))
            except:
                gain.append(0.0)

            percent_gain.append(row_elements[3])
            peak_players.append(row_elements[4])
            result.append(row_elements)

        return month, avg_players, gain, percent_gain, peak_players

    def getOneGameData(self):
        month, avg_player, gain, percent_gain, peak_players = self.recieveData()
        all_years = []
        all_months = []

        # SEPARATE MONTH AND YEAR STRING
        for i in range(len(month)):
            separate = month[i].split(' ')
            if separate[0] == "Last":
                ok = datetime.datetime.now()
                current_month = ok.strftime("%B")
                all_months.append(current_month)
                all_years.append(datetime.datetime.now().year)
            else:
                all_months.append(separate[0])
                all_years.append(int(separate[1]))

        return all_months, all_years, avg_player, gain, percent_gain, peak_players
