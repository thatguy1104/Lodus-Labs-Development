# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def write_json(file_json, data_json):
    """
    Writes JSON data to a json file
    (filename.json)
    """
    with open(file_json, 'w') as f:
        json.dump(data_json, f, indent=INDENT)

# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def append_game_data_json(file_json, data_json):
    """
    Appends game data (json format) to a json file
    Replaces cursor key
    """
    with open(file_json) as f:
        filedata = json.load(f)

        merged = filedata['data'] + data_json['data']

        filedata['data'] = merged
        filedata['pagination'] = data_json['pagination']

    write_json(file_json, filedata) # save file 

# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def get_top_games_queryOLD(pagination_nr=None, filename = 'get_top_games_query.json'):
    """
    Gets games sorted by number of current viewers on Twitch, most popular first.
    'filename' determines name of file where data is saved
    'pagination_nr' determines what page to start calling data from
    """

    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('games/top', payload)

    # Save response to json file
    write_json(filename, response.json()) # Save response to json file

    while(response.json()["pagination"]):
        payload['after'] = response.json()["pagination"]["cursor"]
        response = get_response('games/top', payload)
        response_json = response.json()
    print("Done")

# NOT USED EXPECT FOR TESTING PURPOSES (SAVING DATA IN JSON FILE)
def get_view_count_of_gamesOLD(filename, pagination_nr=None, view_counts={}, testcount=0):
    payload = {'first': 100, 'after': pagination_nr}
    response = get_response('streams', payload)
    response_json = response.json()

    # Iteate through streams and add view_count
    for dict_item in response_json['data']:
        if dict_item['game_id'] in view_counts.keys():
            view_counts[dict_item['game_id']] += dict_item['viewer_count']
        else:
            view_counts[dict_item['game_id']] = dict_item['viewer_count']

    # Stop the functions once we are looking at streams with 1 viewer
    if 1 in view_counts.values():
        return 

    # Save view counts to file
    write_json('view_counts.json', view_counts)

    # If there exists more livestreams go to next page
    if (response.json()["pagination"]):
        payload['after'] = response.json()["pagination"]["cursor"]
        get_view_count_of_games(filename, pagination_nr=response.json()["pagination"]["cursor"], view_counts=view_counts, testcount=testcount)