import lxml
import json
from csv import reader

class GameCorporations:
    def __init__(self):
        self.file = './DATA(csv)/data.csv'

    def getCorporationNames(self):
        names = []
        city = []
        country = []
        all_games = []
        list_inactive = ["Danger Close Games",
                         "Day 1 Studios", "Deadline Games", "Dhruva Interactive", "Digital Reality", "Disney Interactive Studios", "Dynamix",
                         "The Dovetail Group", "EA Black Box", "Eat Sleep Play", "Elemental Games", "Ensemble Studios", "Epicenter Studios",
                         "Epyx", "ESA (formerly Softmax)", "Étranges Libellules", "Eurocom", "Evolution Studios", "Examu", "FASA Studio", 
                         "feelplus", "First Star Software", "Flagship Studios", "Flight-Plan", "Foundation 9 Entertainment", "Fox Digital Entertainment",
                         "FTL Games", "Futuremark", "Gray Matter Interactive", "Gremlin Interactive", "Guerrilla Cambridge", "Hanaho", "Headstrong Games",
                         "Heartbeat", "Hudson Soft", "Human Entertainment", "Human Head Studios", "Imageepoch", "Infocom", "Incognito Entertainment", 
                         "Incredible Technologies", "Innerloop Studios", "Ion Storm", "Ion Storm Austin", "Iron Lore Entertainment", "Irrational Games",
                         "Jaleco", "Javaground", "JV Games", "Kaos Studios", "Kesmai", "Krome Studios", "Krome Studios Melbourne", "Kush Games", 
                         "Kuma Reality Games", "Legend Entertainment", "Lift London", "Lionhead Studios", "Liquid Entertainment", "Locomotive Games", 
                         "Looking Glass Studios", "LucasArts", "Luma Arcade", "Luxoflux", "Magenta Software", "Majesco Entertainment", "Mean Hamster Software",
                         "Metropolis Software", "MicroProse Software", "Midway Games", "Midway Studios – Newcastle", "Milestone", "Mitchell Corporation",
                         "Mythic Entertainment", "Namco Tales Studio", "NDOORS Corporation", "Neko Entertainment", "NetDevil", "Neverland", "Neversoft",
                         "New World Computing", "Nibris", "NovaLogic", "n-Space", "Origin Systems", "Outrage Entertainment", "Oxygen Studios",
                         "Page 44 Studios", "Project Sora", "Papaya Studio", "Parallax Software", "Pandemic Studios", "Penguin Software", 
                         "Phenomic Game Development", "Pi Studios", "Pivotal Games", "Playdom", "Playfish", "PlayFirst", "Press Play", "Q Entertainment",
                         "Quest Corporation", "Radical Entertainment", "Rage Games", "Rainbow Studios", "Realtime Worlds", "RedTribe (Tribalant)", 
                         "Reflexive Entertainment", "Runic Games", "Sand Grain Studios", "Sir-Tech", "Sega AM3", "Sega Sports R&D", "Sensible Software",
                         "SCE Studio Liverpool", "SingleTrac", "Sierra Entertainment", "Silicon Knights", "Silicon Studio", "Simtex", "Slant Six Games",
                         "Snowblind Studios", "Software 2000", "Spellbound Entertainment", "Spike", "Sproing Interactive Media", "Stainless Steel Studios",
                         "Strategic Simulations", "Straylight Studios", "Swingin' Ape Studios", "StormRegion", "Sunstorm Interactive", "T&E Soft",
                         "Team Bondi", "Team Ico", "Tecmo", "Telltale Games", "Terminal Reality", "Tetris Online", "THQ", "Three Rings Design",
                         "TimeGate Studios", "Toaplan", "ToeJam & Earl Productions", "Torpex Games", "Trapdoor", "Transmission Games", "Trion Worlds",
                         "UEP Systems", "Ultimate Play the Game", "United Front Games", "United Game Artists", "Universomo", "Venan Entertainment", 
                         "Vigil Games", "Visceral Games", "Wargaming Seattle", "Westone Bit Entertainment", "Westwood Studios", "Wideload Games",
                         "World Forge", "Zipper Interactive", "Zombie Studios", "ZootFly"]
        
        with open(self.file, newline='') as csvfile:
            csv_reader = reader(csvfile)
            for row in csv_reader:
                if row[0] not in list_inactive:
                    # Get the corporation names, first element of the csv_reader row
                    names.append(row[0])
                    # Get the city
                    city.append(row[1])
                    # Get the country
                    country.append(row[3])
        return names, city, country, all_games

    def writeToJSON(self, names, city, country, games):
        data = {}
        data['company'] = []

        for i in range(1, len(names) - 1):
            data['company'].append({
                'name' : names[i],
                'city' : city[i],
                'country' : country[i],
                'games' : "None yet"
                })

        with open('./DATA(json)/corp_info.json', 'w') as outfile:
             json.dump(data, outfile)

    def writeCorpNames(self):
        names, city, country, games = self.getCorporationNames()
        self.writeToJSON(names, city, country, games)
