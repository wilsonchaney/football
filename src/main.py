from visuals import ScatterGen
from clusters import PlayerClusters

from scraping import get_player_list

def get_player(player_list,player_name,player_pos):
    filtered = [x for x in player_list if player_name in x.name and player_pos in x.posns]
    if len(filtered) == 0:
        print "Could not find",player_name
        return None
    return filtered[0]

# Some unfinished clustering business
'''
players = get_player_list("scraping/data/player_list.json")
with open("players.dat","r") as names_file:
    names = [name.strip() for name in names_file.readlines()]
players = [get_player(players,x,"QB") for x in names]
plt = ScatterGen()
for p in players:
    print "Reading",p.name
    p.read_page()
clusters = PlayerClusters(3,["pass_int_perc","pass_yds_per_att"])
clusters.cluster_QBs(players,True)
print "Done"
'''
