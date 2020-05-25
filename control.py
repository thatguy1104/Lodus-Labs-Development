from Platform.steam import *
from Platform.steamBandwidth import *
from Scrapers.corp1 import *
from Scrapers.finance import *

""" INITIALISE THE JSON FILES (RUN ONLY ONCE, UNLESS CHANGES ARE MADE) """

# CORPORATION LIST: NAME, CITY, COUNTRY
# corp = GameCorporations()
# corp.writeCorpNames()

# Get the NAME, DEVELOPER, CURRENT_PLAYERS
# steam_general = SteamList('2C2C2E0FEBFD8D32F9346602D47C83BA')
# steam_general.writeToJSON()

steam_bandwidth = SteamBandwidth(17) # 16 = is the weird number at the end of the request link
steam_bandwidth.writeBandwidthSteam()


""" CONTROL FLOW CLASSES """


