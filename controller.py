from GOOGLE_PLAYSTORE.play_controller import PlayController
from STEAM.steam_controller import SteamController

def updatePlay():
    play = PlayController()
    return play.controller()

def updateSteam():
    control = SteamController()
    return control.runControl()

play_store_time = updatePlay()
# steam_time = updateSteam()

print("Play Store finished in " + str(play_store_time))
# print("Steam finished in " + str(steam_time))