from GeneralGameData.steamConcurrent import steamConcurrent
from Network.steamBandwidth import SteamBandwidth
from OneGameData.oneGameData import GameStats
from ALL_GAMES_ALL_STATS.record_total_stats import GetAllRecordData

class SteamController():

    def getBriefGameStats(self):
        """
        UPDATABLE: GET BREIF DATA ON ALL 12K GAMES
            - Writes to top100GamesByPlayers.json
        """
        steam_concurrent = steamConcurrent()
        MAX_pages = 480
        steam_concurrent.updateJSON(MAX_pages)

    def getBandwidthPerCountry(self):
        """
        UPDATABLE: GET DATA BANDWIDTH PER COUNTRY
            - Writes to bandwidthSteamData.json
        """
        steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
        steam_bandwidth.writeBandwidthSteam()

    def getALLGamesDATA(self):
        """
        RECORD HISTORY DATA FOR 12K GAMES
            - Writes to recordsAllGameStats.json
        """
        set_all_data = GetAllRecordData()
        set_all_data.record()

    def runControl(self):
        """
        UPDATES ALL STEAM-RELATED DATA
        """
        # self.getBriefGameStats()
        # self.getBandwidthPerCountry()
        self.getALLGamesDATA()

control = SteamController()
control.runControl()

