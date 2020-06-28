from bs4 import BeautifulSoup
import requests
import lxml
import json
import datetime

timestamp = datetime.datetime.now()
current_month = timestamp.strftime("%B")

class OptimisedGameStats():
    def __init__(self, gameID):
        self.GameID = gameID
        self.link = 'https://steamcharts.com/' + gameID

    def recieveData(self):
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, 'lxml')

        # SPECIFY NUMBER OF PREVIOUS MONTHS TO INCLUDE IN THE SCRAPE DATA
        rows_to_record = 2
        columns = 5

        tbody = soup.find('tbody')
        rows = tbody.find_all('tr', limit = rows_to_record)
        two_rows = []
        month = []
        avg_players = []
        gain = []
        percent_gain = []
        peak_players = []
        result = []

        for i in rows:
            td_s = i.find_all('td', limit = columns)
            row_elements = []
            for j in td_s:
                line = j.text.replace('\t', '').replace('\n', '').replace('\n\n', '')
                row_elements.append(line)

            month.append(row_elements[0])
            avg_players.append(float(row_elements[1]))

            try:
                gain.append(float(row_elements[2]))
            except:
                gain.append(0.0)

            percent_gain.append(row_elements[3])
            peak_players.append(int(row_elements[4]))
            result.append(row_elements)

        all_years = []
        all_months = []

        # SEPARATE MONTH AND YEAR STRING
        for i in range(len(month)):
            separate = month[i].split(' ')
            if separate[0][0] == "L":
                all_months.append(current_month)
                all_years.append(datetime.datetime.now().year)
            else:
                all_months.append(separate[0])
                all_years.append(int(separate[1]))

        return all_months, all_years, avg_players, gain, percent_gain, peak_players