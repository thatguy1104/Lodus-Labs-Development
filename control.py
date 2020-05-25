from Platform.steam import *
from Scrapers.corp1 import *

""" INITIALISE THE JSON FILE (ONLY ONCE UNLESS CHANGES ARE MADE) """
# CORPORATION LIST: NAME, CITY, COUNTRY
# corp = GameCorporations()
# corp.writeCorpNames()


""" STEAM API """
# Get the NAME, DEVELOPER, CURRENT_PLAYERS
steam = SteamList('2C2C2E0FEBFD8D32F9346602D47C83BA')
steam.run()
