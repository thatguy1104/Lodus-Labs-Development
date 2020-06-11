from gameStats import AllGamesForDev
from devRanks import DevelopersGames

def load_Ranks():
    """
    RANKS COMPANIES + GENERAL DATA
        Writes to: 
            table = play_dev_ranks
            database = project_data
    """
    ranks = DevelopersGames()
    ranks.writeToDB()

def load_Apps():
    """
    DETAILED APP ANALYTICS
        Writes to:
            table = play_app_ranks
            database = project_data
    """
    apps = AllGamesForDev()
    apps.getAllGameStats()

def controller():
    load_Ranks()
    load_Apps()

controller()