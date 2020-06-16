from GOOGLE_PLAYSTORE.gameStats import AllGamesForDev
from GOOGLE_PLAYSTORE.devRanks import DevelopersGames
import time

class PlayController():
    def load_Ranks(self):
        """
        RANKS COMPANIES + GENERAL DATA
            Writes to: 
                table = play_dev_ranks 
                database = project_data
        """
        ranks = DevelopersGames()
        return ranks.writeToDB()

    def load_Apps(self):
        """
        DETAILED APP ANALYTICS
            Writes to:
                table = play_app_ranks
                database = project_data
        """
        apps = AllGamesForDev()
        apps.getAllGameStats()

    def controller(self):
        # START TIME
        t0 = time.time()

        ranks = self.load_Ranks()
        print(ranks)
        # self.load_Apps()
        
        # END TIME
        t1 = time.time()

        # print("\n\nCode Finished In: {0}\n\n".format(t1-t0))