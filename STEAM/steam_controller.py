from STEAM.GeneralGameData.steamConcurrent import steamConcurrent
from STEAM.Network.steamBandwidth import SteamBandwidth
from STEAM.ALL_GAMES_ALL_STATS.oneGameData import GameStats
from STEAM.ALL_GAMES_ALL_STATS.record_total_stats import GetAllRecordData
import time

class SteamController():

    def getConcurrentStats(self):
        """
        UPDATABLE: GET BREIF DATA ON ALL 12K GAMES
            Writes to:
                table = steam_concurrentGames
                database = project_data
        """
        steam_concurrent = steamConcurrent()
        MAX_pages = 478
        return steam_concurrent.updateDB(MAX_pages)

    def getBandwidthPerCountry(self):
        """
        UPDATABLE: GET DATA BANDWIDTH PER COUNTRY
            Writes to:
                table = steam_network_data
                database = project_data
        """
        steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
        return steam_bandwidth.writeBandwidthSteam()

    def getALLGamesDATA(self):
        """
        RECORD HISTORY DATA FOR 12K GAMES
            Writes to:
                table = steam_all_games_all_data
                database = project_data
        """
        set_all_data = GetAllRecordData()
        return set_all_data.record()

    def runControl(self):
        """
        UPDATES ALL STEAM-RELATED DATA
        """

        # START TIME
        # t0 = time.time()

        concurrent = self.getConcurrentStats()
        bandwidth = self.getBandwidthPerCountry()
        all_games = self.getALLGamesDATA()
        
        # END TIME
        # t1 = time.time()

        # print("\n\nCode Finished In: {0}\n\n".format(t1-t0))

