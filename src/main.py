from math import atan,pi

import matplotlib.pyplot as plt

from clusters import PlayerClusters
from datastorage import get_player_list
from datastorage.player import PassingPlayer

def get_player(player_list,player_name,player_pos):
    filtered = [x for x in player_list if player_name in x.name and player_pos in x.posns]
    if len(filtered) == 0:
        print "Could not find",player_name
        return None
    return filtered[0]

# Some unfinished clustering business
def try_k_vals(players):
    x_vals = []
    y_vals = []
    data = []
    for k in range(3,10):
        clusters = PlayerClusters(k,["pass_int_perc","pass_yds_per_att"])
        clusters.cluster_QBs(players,False)
        print k,clusters.variance
        x_vals.append(k)
        y_vals.append(clusters.variance)
        data.append([k,clusters.variance])
    plt.scatter(x_vals,y_vals)
    determine_correct_k(data)
    plt.show()

# Returns angle between *head-to-tail* segments with the given slopes
def get_angle(slope1,slope2):
    return 180-atan((slope1-slope2)/(1+slope1*slope2))*(180/pi)


# Checks for "elbow"
def determine_correct_k(data):
    slopes = [data[i][1]-data[i-1][1] for i in range(1,len(data))]
    angles = [get_angle(slopes[i],slopes[i-1]) for i in range(1,len(slopes))]

    val, idx = min((val, idx+1) for (idx, val) in enumerate(angles))

    print "Calculated k value:",data[idx][0]

players = get_player_list("datastorage/data/player_list.json")
with open("players.dat","r") as names_file:
    names = [name.strip() for name in names_file.readlines()]
players = [PassingPlayer(get_player(players,x,"QB")) for x in names]
for p in players:
    print "Reading",p.name
    p.read_page()
try_k_vals(players)
print "Done"

