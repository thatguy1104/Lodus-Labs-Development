from gameStats import AllGamesForDev
from devRanks import DevelopersGames


def load_Ranks():
    """
    RANKS COMPANIES + GENERAL DATA
        Writes to: 
            table = PLAY_dev_ranks
            databse = project_data
    """
    ranks = DevelopersGames()
    ranks.writeToDB()

def load_Apps():
    """
    DETAILED APP ANALYTICS
    """
    apps = AllGamesForDev()
    apps.getAllGameStats()


def controller():
    # load_Ranks()
    load_Apps()

controller()