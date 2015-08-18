from pyquery import PyQuery as pq
import json

class Player:
    def __init__(self,name,posns,url):
        self.name = name
        self.posns = posns
        self.url = url

d = pq(url='http://www.pro-football-reference.com/players/A')
player_list = []
for block in d("blockquote > pre"):
    player_links = block.cssselect('a')
    player_data = block.text_content().split('\n')[1:-1]
    if(player_links is None):
        continue
    if(len(player_links) != len(player_data)):
        raise Exception("Lengths must be equal!")
    n = len(player_links)
    for i in range(0,n):
        curr_data = player_data[i].split()

        name = curr_data[0]+" "+curr_data[1]
        posns = curr_data[2].split('-')
        url = player_links[i].get('href')

        player = Player(name,posns,url)
        player_list.append(player)
with open("player_list.txt","w") as file:
    json.dump([p.__dict__ for p in player_list],file);