from player_list_scraper import get_all_players
from player import Player
import json

# Should really only need to be run one time - DLs player data from site
def scrape_player_list(file_name):
    players = get_all_players()
    with open(file_name,"w") as file:
        json.dump([p.__dict__ for p in players],file)

# Reads players into memory
def get_player_list(file_name):
    player_list = []
    with open(file_name,"r") as file:
        text = file.read()
        j = json.loads(text)
        for json_object in j:
            player = Player(**json_object)
            player_list.append(player)
    return player_list
