# Step 1: update app ids
# Step 2: iterate through OneGameData

from OneGameData.oneGameData import GameStats
from bs4 import BeautifulSoup
import requests
import lxml
import json
import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'analytcis_123'
database = 'project_data'

class GetAllRecordData():

    def __init__(self):
        self.writeFILE = 'ALL_GAMES_ALL_STATS/recordsAllGameStats.json'
        self.linkGeneral = 'https://store.steampowered.com/stats/'
        self.linkAll = 'https://steamcharts.com/top/p.'
        self.response = requests.get(self.linkGeneral)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

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

    def readGameIds(self):
        pages = 450
        ids = []
        names = []

        print("Gathering game IDs...")
        for p in range(1, pages):
            print("{0} / {1}".format(p, pages))
            name, game_id = self.getTopGamesByPlayerCount(p)
            for i in range(len(name)):
                ids.append(game_id[i])
                names.append(name[i])
        print("Finished gathering game IDs")
        return names, ids

    def getOneGameStats(self):
        names, get_all_ids = self.readGameIds()

        # CONNECT TO A SERVER DATABASE
        myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cur = myConnection.cursor()

        # RESET THE TABLE
        cur.execute("DROP TABLE IF EXISTS all_games_all_data;")
        create = """CREATE TABLE all_games_all_data(
            Month           text,
            name_           text,
            ids             text,
            avg_players     float,
            gains           float,
            percent_gains   text,
            peak_players    INT,
            Time_Updated    TIME NOT NULL DEFAULT CURRENT_TIME,
            Date_Updated    DATE NOT NULL DEFAULT CURRENT_DATE
        );"""
        cur.execute(create)
        print("Successully created DB Table: all_games_all_data")

        # RECORD DATA
        for i in range(len(names)):
            one_game = GameStats(get_all_ids[i])
            all_months, all_players, all_gains, all_percent_gains, all_peak_players = one_game.getOneGameData()
            if counter < 4:
                print("Writing page {0} / {1} to <all_games_all_data> table (db: {2})".format(i, len(names), database))
                name = names[i]
                id_ = get_all_ids[i]
                months = all_months # LIST OF STRINGS
                avg_players = all_players # LIST OF FLOATS
                gains = all_gains # LIST OF FLOATS
                percent_gains = all_percent_gains # LIST OF STRINGS
                peak_players = all_peak_players # LIST OF STRINGS

                if len(gains) is not 0:
                    gains[len(gains) - 1] = 0

                if len(percent_gains) is not 0:
                    percent_gains[len(percent_gains) - 1] = 0
                
                for j in range(len(months)):
                    cur.execute("INSERT into all_games_all_data(Month, name_, ids, avg_players, gains, percent_gains, peak_players) VALUES (%s, %s, %s, %s, %s, %s, %s)", (months[j], name, id_, avg_players[j], gains[j], percent_gains[j], peak_players[j]))
                
        print("Successully written to DB Table: all_games_all_data")
        myConnection.commit()
        myConnection.close()

    def record(self):
        self.getOneGameStats()