import time
import sys
import datetime
import json
import pyodbc
import configparser as cfg
import hashlib

server = 'serverteest.database.windows.net'
database = 'testdatabase'
username = 'login12391239'
password = 'HejsanHejsan!1'
driver = '{ODBC Driver 17 for SQL Server}'

class Integrate():
    def progress(self, count, total, custom_text, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '*' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s %s %s\r' %
                         (bar, percents, '%', custom_text, suffix))
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

    def returnTwitch(self):
        # CONNECT TO A SERVER DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()
        cur.execute("""SELECT gameid, gamename FROM games2""")
        records = cur.fetchall()

        twitch_name_set = set()
        for name in records:
            twitch_name_set.add((name[1], name[0]))
        steam_names = list(twitch_name_set)

        myConnection.close()
        return steam_names

    def returnSteam(self):
        # CONNECT TO A SERVER DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()
        cur.execute("""SELECT name_, ids FROM steam_all_games_all_data""")
        records = cur.fetchall()

        # STEAM
        steam_name_set = set()
        for name in records:
            steam_name_set.add((name[0], name[1]))
        steam_names = list(steam_name_set)

        myConnection.close()
        return steam_names

    # CHANGE PARAMETERS TO LIST OF DICTIONARIES FOR N-NUMBER OF PLATFORMS
    def returnUnion(self, steam_dict, twitch_dict):
        final_set = {}

        for elem in steam_dict:
            if elem in twitch_dict:
                final_set[elem] = []
                final_set[elem].append({
                    'Hash'      : elem,
                    'Game_Name' : twitch_dict[elem][0],
                    'ID_steam'  : steam_dict[elem][1],
                    'ID_twitch' : twitch_dict[elem][1]
                })
            else:
                final_set[elem] = []
                final_set[elem].append({
                    'Hash'      : elem,
                    'Game_Name' : steam_dict[elem][0],
                    'ID_steam'  : steam_dict[elem][1],
                })

        for elem in twitch_dict:
            if elem not in steam_dict:
                final_set[elem] = []
                final_set[elem].append({
                    'Hash'      : elem,
                    'Game_Name' : twitch_dict[elem][0],
                    'ID_twitch' : twitch_dict[elem][1]
                })

        return final_set

    def customHash(self, string_to_be_hashed):
        # FROM: https://www.pythoncentral.io/hashing-strings-with-python/
        hash_object = hashlib.md5(string_to_be_hashed.encode())
        return hash_object.hexdigest()

    def converstion(self):
        steam_names = self.returnSteam()
        twitch_names = self.returnTwitch()

        steam_dict = {}
        twitch_dict = {}

        for tupl_steam in steam_names:
            name_hashed_steam = self.customHash(tupl_steam[0])
            steam_dict[name_hashed_steam] = tupl_steam

        for tupl_twitch in twitch_names:
            name_hashed_twitch = self.customHash(tupl_twitch[0])
            twitch_dict[name_hashed_twitch] = tupl_twitch
        
        final_set = self.returnUnion(steam_dict, twitch_dict)

        # with open('final_set.json', 'w') as outfile:
        #     json.dump(final_set, outfile)

        return final_set

    def pushToDB(self):
        final_set = self.converstion()

        # RECORD DATA
        data = []
        curr_date = datetime.datetime.now()

        counter = 0
        len_ = len(final_set)
        for hash_name in final_set:
            self.progress(counter, len_, "integrating for <look_up_table>")
            game_name = final_set[hash_name][0]['Game_Name']
            if 'ID_steam' in final_set[hash_name][0]:
                id_steam = final_set[hash_name][0]['ID_steam']
            else:
                id_steam = None
            if 'ID_twitch' in final_set[hash_name][0]:
                id_twitch = final_set[hash_name][0]['ID_twitch']
            else:
                id_twitch = None
            
            data.append((hash_name, game_name, id_steam, id_twitch, curr_date))
            counter += 1
        sys.stdout.write('\n')

        # CONNECT TO A SERVER DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'look_up_table'):
            # RESET THE TABLE
            cur.execute("DROP TABLE IF EXISTS look_up_table;")
            create = """CREATE TABLE look_up_table(
                Hash            VARCHAR(250),
                Game_Name       NVARCHAR(250),
                ID_steam        NVARCHAR(200),
                ID_twitch       INT,
                Last_Updated    DATETIME
            );"""
            cur.execute(create)
            myConnection.commit()
            print("Successully created DB Table: look_up_table")

        cur.fast_executemany = True
        # DO NOT WRITE IF LIST IS EMPTY DUE TO TOO MANY REQUESTS
        if not data:
            print("Not written --> too many requests")
        else:
            # RECORD INITIAL TIME OF WRITING
            t0 = time.time()

            insertion = "INSERT into look_up_table(Hash, Game_Name, ID_steam, ID_twitch, Last_Updated) VALUES (?, ?, ?, ?, ?)"
            cur.executemany(insertion, data)

            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to table <look_up_table> (db: {0})".format(database))

        myConnection.commit()
        myConnection.close()

        return t1 - t0

obj = Integrate()
obj.pushToDB()
