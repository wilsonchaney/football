from player_list_scraper import get_all_players
import json

# Should really only need to be run one time - DLs player data from site
def scrape_player_list(file_name):
    players = get_all_players()
    with open("player_list.txt","w") as file:
        json.dump([p.__dict__ for p in players],file)
