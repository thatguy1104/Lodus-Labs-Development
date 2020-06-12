from GOOGLE_PLAYSTORE.play_controller import PlayController
from STEAM.steam_controller import SteamController

def updatePlay():
    play = PlayController()
    play.controller()

def updateSteam():
    control = SteamController()
    control.runControl()

updatePlay()
updateSteam()
