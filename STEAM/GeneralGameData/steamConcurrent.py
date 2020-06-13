from bs4 import BeautifulSoup
import requests
import lxml
import json
import pyodbc
import datetime

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver= '{ODBC Driver 17 for SQL Server}'

class steamConcurrent():
    def __init__(self):
        self.linkGeneral = 'https://store.steampowered.com/stats/'
        self.linkAll = 'https://steamcharts.com/top/p.'
        self.response = requests.get(self.linkGeneral)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

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

        for i in range(len(names)):
            peak_players.append(peaks[i].text)
        for i in range(len(names)):
            hours_played.append(hours[i].text)
        
        return all_game_names, current_players, peak_players, hours_played

    def updateDB(self, pages):
        data = {}
        data['Concurrent Steam Data'] = []
        data['General Data'] = []
        total_current, total_peak = self.getConcurrent()

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
        cur = myConnection.cursor()

        # EXECUTE SQL COMMANDS
        cur.execute("DROP TABLE IF EXISTS steam_concurrentGames;")
        create = """CREATE TABLE steam_concurrentGames(
            Name_               text,
            Current_Players     BIGINT,
            Peak_Today          BIGINT,
            Hours_Played        BIGINT,
            Last_Updated        DATETIME
        );"""
        cur.execute(create)
        print("Successully created DB Table: steam_concurrentGames")

        for p in range(1, pages):
            print("Writing page {0} / {1} to <steam_concurrentGames> table (db: {2})".format(p, pages, database))
            name, current, peak, hours_played = self.getTopGamesByPlayerCount(p)
            curr_date = datetime.datetime.now()

            for i in range(len(name)):
                insertion = "INSERT INTO steam_concurrentGames(Name_, Current_Players, Peak_Today, Hours_Played, Last_Updated) VALUES (?, ?, ?, ?, ?)"
                values = (name[i], current[i], peak[i], hours_played[i], curr_date)
                cur.execute(insertion, values)

        print("Successully written to table <steam_concurrentGames> (db: {0})".format(database))
        myConnection.commit()
        myConnection.close()