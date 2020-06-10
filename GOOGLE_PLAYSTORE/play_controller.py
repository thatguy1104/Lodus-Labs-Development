from gameStats import AllGamesForDev
from devRanks import DevelopersGames


def load_Ranks():
    """
    
    """
    ranks = DevelopersGames()
    ranks.writeToDB()

def load_Apps():
    """
    
    """
    apps = AllGamesForDev()
    apps.getAllGameStats()


def controller():
