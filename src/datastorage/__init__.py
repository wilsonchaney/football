from os.path import isfile
import json

from player_list_scraper import get_all_players
from src.datastorage.player import Player


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
            player = Player(**json_object)
            player_list.append(player)
    return player_list

# Set to True to re-scrape the list of players.
force_scrape_player_list = False

if force_scrape_player_list or not isfile("datastorage/data/player_list.json"):
    print "Player list is not cached, downloading now"
    scrape_player_list("datastorage/data/player_list.json")
else:
    print "Player list is cached, skipping download"
