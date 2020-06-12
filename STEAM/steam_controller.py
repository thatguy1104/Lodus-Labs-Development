from GeneralGameData.steamConcurrent import steamConcurrent
from Network.steamBandwidth import SteamBandwidth
from ALL_GAMES_ALL_STATS.oneGameData import GameStats
from ALL_GAMES_ALL_STATS.record_total_stats import GetAllRecordData
import time

class SteamController():

    def getConcurrentStats(self):
        """
        UPDATABLE: GET BREIF DATA ON ALL 12K GAMES
            Writes to:
                table = 
                database = project_data
        """
        steam_concurrent = steamConcurrent()
        MAX_pages = 480
        steam_concurrent.updateJSON(MAX_pages)

    def getBandwidthPerCountry(self):
        """
        UPDATABLE: GET DATA BANDWIDTH PER COUNTRY
            Writes to:
                table = network_data
                database = project_data
        """
        steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
        steam_bandwidth.writeBandwidthSteam()

    def getALLGamesDATA(self):
        """
        RECORD HISTORY DATA FOR 12K GAMES
            Writes to:
                table = all_games_all_data
                database = project_data
        """
        set_all_data = GetAllRecordData()
        set_all_data.record()

    def runControl(self):
        """
        UPDATES ALL STEAM-RELATED DATA
        """

        # START TIME
        t0 = time.time()

        self.getConcurrentStats()
        self.getBandwidthPerCountry()
        self.getALLGamesDATA()

        # END TIME
        t1 = time.time()

        print("\n\n Code Finished In: {0}\n\n".format(t1-t0))

control = SteamController()
control.runControl()

