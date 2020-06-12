from gameStats import AllGamesForDev
from devRanks import DevelopersGames
import time

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
    # START TIME
    t0 = time.time()

    load_Ranks()
    load_Apps()
    
    # END TIME
    t1 = time.time()

    print("\n\n Code Finished In: {0}\n\n".format(t1-t0))


controller()