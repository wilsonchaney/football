from os.path import isfile
import json

from player_list_scraper import get_all_players
import player
print "datastorage/__init__.py"

# In this file, we'll ensure that the player list is downloaded.


def scrape_player_list(file_name):
    players = get_all_players()
    with open(file_name,"w") as file:
        json.dump([p.__dict__ for p in players],file)

# Reads players into memory - called from main.py
def get_player_list(file_name):
    player_list = []
    with open(file_name,"r") as file:
        text = file.read()
        j = json.loads(text)
        for json_object in j:
            p = player.Player(**json_object)
            player_list.append(p)
    return player_list

def get_player(player_list,player_name,player_pos):
    filtered = [x for x in player_list if player_name in x.name and player_pos in x.posns]
    if len(filtered) == 0:
        print "Could not find",player_name
        return None
    return filtered[0]

# Set to True to re-scrape the list of players.
force_scrape_player_list = False

# Avoid running this twice!
if __name__ == "src.datastorage":
    if force_scrape_player_list or not isfile("datastorage/data/player_list.json"):
        print "Player list is not cached, downloading now"
        scrape_player_list("datastorage/data/player_list.json")
    else:
        print "Player list is cached, skipping download"
