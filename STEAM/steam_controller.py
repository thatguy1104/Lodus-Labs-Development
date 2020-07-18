from STEAM.GeneralGameData.steamConcurrent import steamConcurrent
from STEAM.Network.steamBandwidth import SteamBandwidth
from STEAM.ALL_GAMES_ALL_STATS.oneGameData import GameStats
from STEAM.ALL_GAMES_ALL_STATS.record_total_stats import GetAllRecordData
from STEAM.ServiceProvider.provider import Provider
from STEAM.Bandwidth_48.bandwidth_48 import Bandwidth_48
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
        steam_bandwidth = SteamBandwidth(17)  # 16 = is the weird number at the end of the request link
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

    def getProviderData(self):
        """
        PERFORMANCE BY INTERNET SERVICE PROVIDER (ISP)
            Writes to:
                table = steam_provider_data
                database = project_data
        """
        data_ = Provider()
        return data_.writeProvider()

    def get48Bandwidth(self):
        """
        PERFORMANCE BY INTERNET SERVICE PROVIDER (ISP)
            Writes to:
                table = steam_48_bandwidth
                database = project_data
        """
        obj = Bandwidth_48()
        # obj.get_data()
        return obj.writeBandwidth()

    def runControl(self):
        """
        UPDATES ALL STEAM-RELATED DATA
        """

        # START TIME
        t0 = time.time()

        # concurrent = self.getConcurrentStats()
        # bandwidth = self.getBandwidthPerCountry()
        all_games = self.getALLGamesDATA()
        # provider = self.getProviderData()
        # bandwidth_48 = self.get48Bandwidth()

        # file1 = open("WRITING_TIMES.txt", "a")
        # file1.write("Concurrent finished in " + str(concurrent) + "\n")
        # file1.write("Bandwidth finished in " + str(bandwidth) + "\n")
        # file1.write("All games finished in " + str(all_games) + "\n")
        # file1.write("Provide finished in " + str(provider) + "\n")
        # file1.write("Bandwidth_48 finished in " + str(bandwidth_48) + "\n")

        # END TIME
        t1 = time.time()

        return t1 - t0
