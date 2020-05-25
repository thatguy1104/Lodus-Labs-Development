import lxml
import json
from csv import reader

class GameCorporations:
    def __init__(self):
        self.file = 'data.csv'

    def getCorporationNames(self):
        names = []
        city = []
        country = []
        with open(self.file, newline='') as csvfile:
            csv_reader = reader(csvfile)
            for row in csv_reader:
                # Get the corporation names, first element of the csv_reader row
                names.append(row[0])
                # Get the city
                city.append(row[1])
                # Get the country
                country.append(row[3])
        return names, city, country

    def writeToJSON(self, names, city, country):
        data = {}
        data['company'] = []

        for i in range(1, len(names) - 1):
            data['company'].append({
                'name' : names[i],
                'city' : city[i],
                'country' : country[i]
                })

        with open('corp_info.json', 'w') as outfile:
             json.dump(data, outfile)

    def run(self):
        names, city, country = self.getCorporationNames()
        self.writeToJSON(names, city, country)

corp = GameCorporations()
corp.run()
