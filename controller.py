from STEAM.ALL_GAMES_ALL_STATS.record_total_stats import GetAllRecordData
from STEAM.GeneralGameData.steamConcurrent import steamConcurrent
from STEAM.Network.steamBandwidth import SteamBandwidth
from STEAM.ALL_GAMES_ALL_STATS.record_total_stats import GetAllRecordData


def updateSTEAM():
    steam_concurrent = steamConcurrent()
    MAX_pages = 480
    steam_concurrent.updateJSON(MAX_pages)
    print("DONE WITH CONCURRENT")

    steam_bandwidth = SteamBandwidth(17)
    steam_bandwidth.writeBandwidthSteam()
    print("DONE WITH BANDWIDTH")

    set_all_data = GetAllRecordData()
    set_all_data.record()
    print("DONE WITH ALL GAMES DATA")

updateSTEAM()
