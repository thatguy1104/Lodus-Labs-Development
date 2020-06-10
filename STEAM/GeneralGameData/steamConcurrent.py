from bs4 import BeautifulSoup
import requests
import lxml
import json
import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'analytcis_123'
database = 'steam_data'

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

    def updateJSON(self, pages):
        data = {}
        data['Concurrent Steam Data'] = []
        data['General Data'] = []
        total_current, total_peak = self.getConcurrent()

        # CONNECT TO DATABASE
        myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cur = myConnection.cursor()

        # EXECUTE SQL COMMANDS
        cur.execute("DROP TABLE IF EXISTS concurrentGames;")
        create = """CREATE TABLE concurrentGames(
            Name_               CHAR(200),
            Current_Players     BIGINT,
            Peak_Today          BIGINT,
            Hours_Played        BIGINT,
            Time_Updated        TIME,
            Date_Updated        DATE NOT NULL DEFAULT CURRENT_DATE
        );"""
        cur.execute(create)
        print("Successully created DB Table: concurrentGames")

        for p in range(1, pages):
            print("Writing page {0} / {1} to <concurrentGames> table (db: {2})".format(p, pages, database))
            name, current, peak, hours_played = self.getTopGamesByPlayerCount(p)

            for i in range(len(name)):
                insertion = "INSERT INTO concurrentGames(Name_, Current_Players, Peak_Today, Hours_Played, Time_Updated) VALUES (%s, %s, %s, %s, CURRENT_TIME)"
                values = (name[i], current[i], peak[i], hours_played[i])
                cur.execute(insertion, values)

        print("Successully written to DB Table: concurrentGames")
        myConnection.commit()
        myConnection.close()