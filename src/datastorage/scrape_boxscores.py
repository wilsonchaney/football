from pyquery import PyQuery as pq
import os
import urllib2
from time import sleep,time

import json

'''
This is an experimental file.

I'm going to work on scraping boxscores from pro-football-reference
so I can track team stats from week to week.

This will, hopefully, be used for some predictive modeling
of winners of NFL games.
'''

def download_boxscore_list(year):
    url = "http://www.pro-football-reference.com/years/%d/games.htm" % year

    schedule_page = pq(url)

    boxscore_links = [link.get('href') for link in schedule_page.find('tr > td:nth-child(4) a')]

    # Filter to regular season, because there are only 256 games.
    boxscore_links = boxscore_links[:256]

    with open("data/boxscores/%s_list.dat" % year,"w") as f:
        for link in boxscore_links:
            f.write(link+"\n")
    print "Downloaded box scores for %d" % year

def get_file_name(year,box_score_link):
    """
    :return: the name of the *.dat file where the page source will be stored for this boxscore.
    """
    link_id = box_score_link[box_score_link.rfind('/')+1:box_score_link.rfind('.')]
    return "data/boxscores/%d/%s.dat" % (year,link_id)

def get_json_file_name(year,box_score_link):
    """
    :return: the name of the *.dat file where the page source will be stored for this boxscore.
    """
    link_id = box_score_link[box_score_link.rfind('/')+1:box_score_link.rfind('.')]
    return "data/boxscores/%d_json/%s.json" % (year,link_id)

def download_all_scores_for_year(year):
    if not os.path.exists("data/boxscores/%d" % year):
        os.makedirs("data/boxscores/%d" % year)
    with open ("data/boxscores/%s_list.dat" % year,"r") as f:
        boxscore_links = [line.strip() for line in f.readlines()]
    for link in boxscore_links:
        url = "http://www.pro-football-reference.com/"+link

        fname = get_file_name(year,link)
        if os.path.exists(fname):
            print "Skipping",fname
        else:
            response = urllib2.urlopen(url)
            html = response.read()
            with open(get_file_name(year,link),"w") as f:
                f.write(html)
            print "Downloaded",get_file_name(year,link)

            # An attempt at rate limiting.
            sleep(0.5)

class BoxScore:
    year = None
    week = None

    home_team = None
    away_team = None
    team_stats = {}

    def to_json(self):
        res = {}
        res["year"] = self.year
        res["week"] = self.week
        res["home_team"] = self.home_team
        res["away_team"] = self.away_team
        res["team_stats"] = self.team_stats

        return res



def parse_boxscore(boxscore_path,year):
    with open(boxscore_path) as f:
        page_src = ''.join(f.readlines())
    boxscore_page = pq(page_src)
    team_stats_table = boxscore_page.find("table#team_stats")

    rows = team_stats_table.find('tr')
    team1,team2 = rows[0].getchildren()[1].text,rows[0].getchildren()[2].text

    week = boxscore_page.find("div#page_content table").find("td")[0].text

    # Change "Week N" into an integer N
    week = int(week[week.index(' ')+1:])

    stats = {}

    # Remove header
    rows = rows[1:]
    for row in rows:
        cells = row.getchildren()
        stats[cells[0].text] = (cells[1].text,cells[2].text)

    result = BoxScore()
    result.week = week
    result.home_team = team2
    result.away_team = team1
    result.year = year
    result.team_stats = stats

    return result

def write_all_boxscores_to_json(year):
    if not os.path.exists("data/boxscores/%d_json" % year):
        os.mkdir("data/boxscores/%d_json" % year)
    with open ("data/boxscores/%s_list.dat" % year,"r") as f:
        boxscore_links = [line.strip() for line in f.readlines()]
    for link in boxscore_links:
        boxscore = parse_boxscore(get_file_name(year,link),year)

        with open(get_json_file_name(year,link),"w") as json_file:
            json_file.write(json.dumps(boxscore.to_json()))



# The below code will download the boxscores from the given year and store the team stats from that game in .json format.
'''
year = 2014
download_all_scores_for_year(2014)
write_all_boxscores_to_json(2014)
'''
