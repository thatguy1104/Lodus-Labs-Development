# Step 1: update app ids
# Step 2: iterate through OneGameData

from STEAM.ALL_GAMES_ALL_STATS.oneGameData import GameStats
from bs4 import BeautifulSoup
import requests
import lxml
import json
import pyodbc
import datetime
import time
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

        # RECORD DATA
        data = {}
        for i in range(len(names)):
            print("Scraping for <play_dev_ranks> {0} / {1}".format(i, len(names)))
            # PREPARE THE IDs
            one_game = GameStats(get_all_ids[i])
            # SCRAPE DATA FOR A GIVEN GAME
            all_months, all_players, all_gains, all_percent_gains, all_peak_players = one_game.getOneGameData()
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
                data[name] = [months[j], name, id_, f, f2, percent_gains[j], inte, curr_date]

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

        # RECORD INITIAL TIME OF WRITING
        t0 = time.time()

        # ITERATE THROUGH DICT AND INSERT VALUES ROW-BY-ROW
        counter = 0
        for elem in data:
            print("Writing page {0} / {1} to <steam_all_games_all_data> table (db: {2})".format(counter, len(data), self.database))
            insertion = "INSERT into steam_all_games_all_data(Month, name_, ids, avg_players, gains, percent_gains, peak_players, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            values = data[elem]
            cur.execute(insertion, values)
            counter += 1

        # RECORD END TIME OF WRITING
        t1 = time.time()

        print("Successully written to table <steam_all_games_all_data> (db: {0})".format(self.database))
        myConnection.commit()
        myConnection.close()

        return t1-t0

    def record(self):
        return self.getOneGameStats()