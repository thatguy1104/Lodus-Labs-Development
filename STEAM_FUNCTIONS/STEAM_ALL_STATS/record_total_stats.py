# Step 1: update app ids
# Step 2: iterate through OneGameData

from bs4 import BeautifulSoup
import requests
import lxml
import json
import pyodbc
import datetime
import time
import sys
import configparser as cfg

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver = '{ODBC Driver 17 for SQL Server}'

class GameStats():
    def __init__(self, gameID):
        self.GameID = gameID
        self.link = 'https://steamcharts.com/' + gameID

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
        all_years = []
        all_months = []
        all_players = []
        all_gains = []
        all_percent_gains = []
        all_peak_players = []

        for i in range(len(month)):
            initial_1 = month[i].text.replace('\t', '')
            mid_1 = initial_1.replace('\n', '')
            separate = mid_1.split(' ')

            if separate[0] == "Last":
                ok = datetime.datetime.now()
                current_month = ok.strftime("%B")
                all_months.append(current_month)
                all_years.append(datetime.datetime.now().year)
            else:
                all_months.append(separate[0])
                all_years.append(int(separate[1]))

            initial_2 = avg_player[i].text.replace('\t', '')
            mid_2 = initial_2.replace('\n', '')
            all_players.append(mid_2)

            all_gains.append(gain[i])

            all_percent_gains.append(percent_gain[i])

            initial_5 = peak_players[i].text.replace('\t', '')
            mid_5 = initial_5.replace('\n', '')
            all_peak_players.append(mid_5)

        return all_months, all_years, all_players, all_gains, all_percent_gains, all_peak_players

class GetAllRecordData():
    def __init__(self):
        self.linkGeneral = 'https://store.steampowered.com/stats/'
        self.linkAll = 'https://steamcharts.com/top/p.'
        self.response = requests.get(self.linkGeneral)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def progress(self, count, total, custom_text, suffix=''):
        bar_len = 40
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '*' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s %s %s\r' % (bar, percents, '%', custom_text, suffix))
        sys.stdout.flush()

    def checkTableExists(self, dbcon, tablename):
        dbcur = dbcon.cursor()
        dbcur.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        if dbcur.fetchone()[0] == 1:
            dbcur.close()
            return True

        dbcur.close()
        return False

    def getTopGamesByPlayerCount(self, page):
        link = self.linkAll + str(page)
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')

        all_game_names = []
        all_game_id = []

        names = soup.find_all('td', class_='game-name left')

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

        for p in range(1, pages):
            self.progress(p, pages, "Gathering game IDs..")
            name, game_id = self.getTopGamesByPlayerCount(p)
            for i in range(len(name)):
                ids.append(game_id[i])
                names.append(name[i])
        print("Finished gathering game IDs")
        return names, ids

    def getOneGameStats(self):
        names, get_all_ids = self.readGameIds()

        # RECORD DATA
        data = []
        curr_date = datetime.datetime.now()

        # len(names)
        for i in range(len(names)):
            self.progress(i, len(names), "scraping for <steam_all_games_all_data>")

            # PREPARE THE IDs
            one_game = GameStats(get_all_ids[i])

            # SCRAPE DATA FOR A GIVEN GAME
            all_months, all_years, all_players, all_gains, all_percent_gains, all_peak_players = one_game.getOneGameData()
            name = names[i]
            id_ = get_all_ids[i]

            if len(all_gains) is not 0:
                all_gains[len(all_gains) - 1] = 0

            if len(all_percent_gains) is not 0:
                all_percent_gains[len(all_percent_gains) - 1] = '0'

            for j in range(len(all_months)):
                f = float(all_players[j])
                f2 = float(all_gains[j])
                inte = int(all_peak_players[j])
                data.append((all_months[j], all_years[j], name, id_, f, f2, all_percent_gains[j], inte, curr_date))
        sys.stdout.write('\n')

        # CONNECT TO A SERVER DATABASE
        myConnection = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'steam_all_games_all_data'):
            # RESET THE TABLE
            cur.execute("DROP TABLE IF EXISTS steam_all_games_all_data;")
            create = """CREATE TABLE steam_all_games_all_data(
                Month           VARCHAR(100),
                Year_           INT,
                name_           NVARCHAR(200),
                ids             VARCHAR(100),
                avg_players     float,
                gains           float,
                percent_gains   VARCHAR(100),
                peak_players    BIGINT,
                Last_Updated    DATETIME
            );"""
            cur.execute(create)
            myConnection.commit()
            print("Successully created DB Table: steam_all_games_all_data")

        # DIVIDE DATA INTO n CHUNKS
        n = 1000
        final = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n)]

        cur.fast_executemany = True
        # DO NOT WRITE IF LIST IS EMPTY DUE TO TOO MANY REQUESTS
        if not data:
            print("Not written --> too many requests")
        else:
            # RECORD INITIAL TIME OF WRITING
            t0 = time.time()

            # ITERATE THROUGH DICT AND INSERT VALUES ROW-BY-ROW
            count = 1
            for elem in final:
                self.progress(count, len(final), "writing to <steam_all_games_all_data>")
                insertion = "INSERT into steam_all_games_all_data(Month, Year_, name_, ids, avg_players, gains, percent_gains, peak_players, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.executemany(insertion, elem)
                count += 1

            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to table <steam_all_games_all_data> (db: {0})".format(database))

        myConnection.commit()
        myConnection.close()

        return t1 - t0

def run():
    obj = GetAllRecordData()
    obj.getOneGameStats()

