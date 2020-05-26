from Platform.steamConcurrent import steamConcurrent
from Platform.steamBandwidth import SteamBandwidth
from Scrapers.corpNamesList import GameCorporations

class SteamController():
    def getDevelopersNames(self):
        corp = GameCorporations()
        corp.writeCorpNames()

    def getAllGameStats(self):
        steam_concurrent = steamConcurrent()
        MAX_pages = 480
        steam_concurrent.updateJSON(MAX_pages) # Writes to top100GamesByPlayers.json
        # steam_concurrent.getTopGamesByPlayerCount()

    def getBandwidthPerCountry(self):
        steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
        steam_bandwidth.writeBandwidthSteam()  # Writes to bandwidthSteamData.json

    def runControl(self):
        """ GET NAMES OF GAME DEVELOPERS """
        # self.getDevelopersNames() # NO NEED TO RUN THIS EITHER
        """ GET ALL GAMES DATA """
        # self.getAllGameStats() 
        """ GET ALL DATA PER COUNTRY """
        # self.getBandwidthPerCountry()

control = SteamController()
control.runControl()

