import json

with open('top_streamed_games_query.json') as json_file:
    streamed_data = json.load(json_file)
    the_data = streamed_data['data'] 
    for p in the_data:
        game_name = p['name']
        game_id = p['id']
        hash_game_name = hash(game_name)
        if game_name == "Dota 2":
            print("("+game_name+", "+str(hash_game_name)+", "+game_id+")")
        
