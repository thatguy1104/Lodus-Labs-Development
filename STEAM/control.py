from GeneralGameData.steamConcurrent import steamConcurrent
from Network.steamBandwidth import SteamBandwidth
from OneGameData.oneGameData import GameStats

class SteamController():

    def getOneGameData(self):
        stats = GameStats('app/570')
        stats.getOneGameData()

    def getAllGameStats(self):
        """
        UPDATABLE:  
        """
        steam_concurrent = steamConcurrent()
        MAX_pages = 480
        steam_concurrent.updateJSON(MAX_pages) # Writes to top100GamesByPlayers.json
        # steam_concurrent.getTopGamesByPlayerCount()

    def getBandwidthPerCountry(self):
        """
        UPDATABLE: GET DATA BANDWIDTH PER COUNTRY
        """
        steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
        steam_bandwidth.writeBandwidthSteam()  # Writes to bandwidthSteamData.json

    def runControl(self):
        """
        UPDATES ALL STEAM-RELATED DATA
        """
        # self.getOneGameData()
        # self.getAllGameStats()
        # self.getBandwidthPerCountry()

control = SteamController()
control.runControl()

