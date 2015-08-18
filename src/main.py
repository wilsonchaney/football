from player_list_scraper import get_all_players
import json

players = get_all_players()
with open("player_list.txt","w") as file:
    json.dump([p.__dict__ for p in players],file);