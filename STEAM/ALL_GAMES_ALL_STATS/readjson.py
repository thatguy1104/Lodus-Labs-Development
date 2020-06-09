import json


with open('recordsAllGameStats.json') as json_file:
    data = json.load(json_file)

    for i in data:
        name = data[i][0]['Name']
        id_ = data[i][0]['ID']
        months = data[i][0]['Month']  # LIST OF STRINGS
        avg_players = data[i][0]['Avg. Players']  # LIST OF FLOATS
        gains = data[i][0]['Gains']  # LIST OF FLOATS
        percent_gains = data[i][0]['\\% Gains']  # LIST OF STRINGS
        peak_players = data[i][0]['Peak Players']  # LIST OF STRINGS


        if len(gains) is not 0:
            gains[len(gains) - 1] = 0

        if len(percent_gains) is not 0:
            percent_gains[len(percent_gains) - 1] = 0
