from bs4 import BeautifulSoup
import requests
import lxml
import json
import pyodbc
import datetime
import time
import configparser as cfg

class steamConcurrent():
    def __init__(self):
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

    # FUNCTION IS NOT USED
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
        # total_current, total_peak = self.getConcurrent()  <-- NOT USED ANYWHERE, BUT KEEP FOR NOW

        # SCRAPE THE DATA FIRST
        data = []
        curr_date = datetime.datetime.now()
        for p in range(1, pages):
            print("Scraping for steam_concurrentGames {} / {}".format(p, pages))
            name, current, peak, hours_played = self.getTopGamesByPlayerCount(p)
            for i in range(len(name)):
                data.append((name[i], current[i], peak[i], hours_played[i], curr_date))

        # CONNECT TO DATABASE
        myConnection = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
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

        # RECORD INITIAL TIME OF WRITING
        t0 = time.time()

        # EXECUTE INSERTION INTO DB
        cur.fast_executemany = True
        insertion = "INSERT INTO steam_concurrentGames(Name_, Current_Players, Peak_Today, Hours_Played, Last_Updated) VALUES (?, ?, ?, ?, ?)"
        cur.executemany(insertion, data)

        # RECORD END TIME OF WRITING
        t1 = time.time()

        print("Successully written to table <steam_concurrentGames> (db: {0})".format(self.database))
        myConnection.commit()
        myConnection.close()

        return t1-t0