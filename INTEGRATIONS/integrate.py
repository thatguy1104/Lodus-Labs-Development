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
    def __init__(self):
        ok = 4

    def returnNameSet(self):
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

        # TWITCH
        twitch_names = []
        with open('top_streamed_games_query.json') as json_file:
            streamed_data = json.load(json_file)
            the_data = streamed_data['data']
            for p in the_data:
                game_name = p['name']
                game_id = p['id']
                twitch_names.append((game_name, game_id))

        myConnection.close()
        return steam_names, twitch_names

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
                    'Hash': elem,
                    'Game_Name': twitch_dict[elem][0],
                    'ID_steam': steam_dict[elem][1],
                })

        for elem in twitch_dict:
            if elem not in steam_dict:
                final_set[elem] = []
                final_set[elem].append({
                    'Hash': elem,
                    'Game_Name': twitch_dict[elem][0],
                    'ID_twitch': twitch_dict[elem][1]
                })

        return final_set

    def customHash(self, string_to_be_hashed):
        # FROM: https://www.pythoncentral.io/hashing-strings-with-python/
        hash_object = hashlib.md5(string_to_be_hashed.encode())
        return hash_object.hexdigest()

    def converstion(self):
        # key: hash, value: (name, ids)
        steam_names, twitch_names = self.returnNameSet()

        steam_dict = {}
        twitch_dict = {}

        for tupl_steam in steam_names:
            name_hashed_steam = self.customHash(tupl_steam[0])
            steam_dict[name_hashed_steam] = tupl_steam

        for tupl_twitch in twitch_names:
            name_hashed_twitch = self.customHash(tupl_twitch[0])
            # twitch_dict.add((name_hashed_twitch, tupl_twitch[0], tupl_twitch[1]))
            twitch_dict[name_hashed_twitch] = tupl_twitch
        
        final_set = self.returnUnion(steam_dict, twitch_dict)

        # with open('results1.json', 'w') as outfile:
        #     json.dump(dict1, outfile)
        # with open('results2.json', 'w') as outfile:
        #     json.dump(dict2, outfile)
        with open('final_set.json', 'w') as outfile:
            json.dump(final_set, outfile)
        # f = open('final_set.txt', 'w')
        # for i in final_set:
        #     f.write(str(i[0]) + ", " + str(i[1]) + ", " +  str(i[2]) + '\n')

    def pushToDB(self):
        name_set = self.returnNameSet()

        # RECORD DATA
        data = []
        curr_date = datetime.datetime.now()

        # len(names)
        for i in range(len(name_set)):
            self.progress(i, len(name_set),"integrating for <look_up_table>")

        sys.stdout.write('\n')

        # CONNECT TO A SERVER DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = myConnection.cursor()

        if not self.checkTableExists(myConnection, 'look_up_table'):
            # RESET THE TABLE
            cur.execute("DROP TABLE IF EXISTS look_up_table;")
            create = """CREATE TABLE look_up_table(
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
            print("Successully created DB Table: look_up_table")

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
                self.progress(count, len(final), "writing to <look_up_table>")
                insertion = "INSERT into look_up_table(Month, Year_, name_, ids, avg_players, gains, percent_gains, peak_players, Last_Updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.executemany(insertion, elem)
                count += 1

            # RECORD END TIME OF WRITING
            t1 = time.time()

            print("Successully written to table <look_up_table> (db: {0})".format(database))

        myConnection.commit()
        myConnection.close()

        return t1 - t0

obj = Integrate()
# obj.returnNameSet()
obj.converstion()
