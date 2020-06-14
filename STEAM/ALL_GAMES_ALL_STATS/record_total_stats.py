# Step 1: update app ids
# Step 2: iterate through OneGameData

from STEAM.ALL_GAMES_ALL_STATS.oneGameData import GameStats
from bs4 import BeautifulSoup
import requests
import lxml
import json
import pyodbc
import datetime
import configparser as cfg

class GetAllRecordData():

    def __init__(self):
        self.writeFILE = 'ALL_GAMES_ALL_STATS/recordsAllGameStats.json'
        self.linkGeneral = 'https://store.steampowered.com/stats/'
        self.linkAll = 'https://steamcharts.com/top/p.'
        self.response = requests.get(self.linkGeneral)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        parser = cfg.ConfigParser()
        parser.read('config.cfg')
        self.server = parser.get('db_credentials', 'server')
        self.database = parser.get('db_credentials', 'database')
        self.username = parser.get('db_credentials', 'username')
        self.password = parser.get('db_credentials', 'password')
        self.driver = parser.get('db_credentials', 'driver')

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
        pages = 448
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
        myConnection = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        cur = myConnection.cursor()

        # RESET THE TABLE
        cur.execute("DROP TABLE IF EXISTS steam_all_games_all_data;")
        create = """CREATE TABLE steam_all_games_all_data(
            Month           text,
            name_           text,
            ids             text,
            avg_players     float,
            gains           float,
            percent_gains   text,
            peak_players    BIGINT,
            Last_Updated    DATETIME
        );"""
        cur.execute(create)
        print("Successully created DB Table: steam_all_games_all_data")

        # RECORD DATA
        for i in range(len(names)):
            one_game = GameStats(get_all_ids[i])
            all_months, all_players, all_gains, all_percent_gains, all_peak_players = one_game.getOneGameData()
            print("Writing page {0} / {1} to <steam_all_games_all_data> table (db: {2})".format(i, len(names), self.database))
            name = names[i]
            id_ = get_all_ids[i]
            months = all_months # LIST OF STRINGS
            avg_players = all_players # LIST OF FLOATS
            gains = all_gains # LIST OF FLOATS
            percent_gains = all_percent_gains # LIST OF STRINGS
            peak_players = all_peak_players # LIST OF STRINGS
            curr_date = datetime.datetime.now()

            if len(gains) is not 0:
                gains[len(gains) - 1] = 0

            if len(percent_gains) is not 0:
                percent_gains[len(percent_gains) - 1] = '0'
            
            for j in range(len(months)):
                f = float(avg_players[j])
                f2 = float(gains[j])
                inte = int(peak_players[j])
                insertion = "INSERT into steam_all_games_all_data(Month, name_, ids, avg_players, gains, percent_gains, peak_players, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                values = (months[j], name, id_, f, f2, percent_gains[j], inte, curr_date)
                cur.execute(insertion, values)

        print("Successully written to table <steam_all_games_all_data> (db: {0})".format(self.database))
        myConnection.commit()
        myConnection.close()

    def record(self):
        self.getOneGameStats()