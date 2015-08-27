from string import ascii_uppercase

from pyquery import PyQuery as pq

from src.datastorage.player import Player


def get_players_beginning_with(letter):
    d = pq(url='http://www.pro-football-reference.com/players/'+letter)
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
            curr_data = player_data[i].split() # len = 4 if two names, 5 if three (e.g. Norm Van Brocklin)

            name = " ".join(curr_data[0:-2])
            posns = curr_data[-2].split('-')
            url = player_links[i].get('href')

            player = Player(name,posns,url)
            player_list.append(player)
    return player_list

def get_all_players():
    result = []
    for letter in ascii_uppercase:
        result.extend(get_players_beginning_with(letter))
        print "Scraped players beginning with",letter
    return result
