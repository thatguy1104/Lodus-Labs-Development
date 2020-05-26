from Platform.steam import *
from Platform.steamConcurrent import *
from Platform.steamBandwidth import *
from Scrapers.corpNamesList import *

class SteamController():
    def getDevelopersNames(self):
        corp = GameCorporations()
        corp.writeCorpNames()

    def getAllgames(self):
        steam_general = SteamList('2C2C2E0FEBFD8D32F9346602D47C83BA')  # Reads steam.csv
        steam_general.writeToJSON()  # Writes to processedSteamData.json

    def getTop100Games(self):
        steam_concurrent = steamConcurrent()
        steam_concurrent.writeToJSON()  # Writes to top100GamesByPlayers.json

    def getBandwidthPerCountry(self):
        steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
        steam_bandwidth.writeBandwidthSteam()  # Writes to bandwidthSteamData.json

    def runControl(self):
        """ GET NAMES OF GAME DEVELOPERS """
        # self.getDevelopersNames()
        """ GET 30K GAME NAMES, IDs, LIVE PLAYER COUNT """
        # self.getAllgames()
        """ GET # OF PLAYERS + PEAK PER GAME (FOR TOP 100 PLAYED GAMES)"""
        # self.getTop100Games()
        """ GET DOWNLOAD DATA PER COUNTRY """
        self.getBandwidthPerCountry()

control = SteamController()
control.runControl()

