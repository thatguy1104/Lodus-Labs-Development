from GeneralGameData.steamConcurrent import steamConcurrent
from Network.steamBandwidth import SteamBandwidth

class SteamController():

    def getAllGameStats(self):
        steam_concurrent = steamConcurrent()
        MAX_pages = 480
        steam_concurrent.updateJSON(MAX_pages) # Writes to top100GamesByPlayers.json
        # steam_concurrent.getTopGamesByPlayerCount()

    def getBandwidthPerCountry(self):
        steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
        steam_bandwidth.writeBandwidthSteam()  # Writes to bandwidthSteamData.json

    def runControl(self):
        """ GET ALL GAMES DATA """
        # self.getAllGameStats()
        """ GET ALL DATA PER COUNTRY """
        # self.getBandwidthPerCountry()

control = SteamController()
control.runControl()

