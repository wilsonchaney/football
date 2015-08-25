from pyquery import PyQuery as pq
import json
from util import try_parse
from os import path

# Will use this to store all stats too
class Player:
    def __init__(self,name,posns,url):
        self.name = name
        self.posns = posns
        self.url = url

    def read_page(self):

        if path.isfile(self.get_cache_path()):
            with open(self.get_cache_path()) as cache_file:
                self.passing_data = json.loads(cache_file.read())
                for key in self.passing_data:
                    for stat in self.passing_data[key]:
                        self.passing_data[key][stat] = try_parse(self.passing_data[key][stat])

        else:
            self.page = pq('http://www.pro-football-reference.com/'+self.url)

            # Populate passing data
            passing_table = self.page("div#div_passing")
            headers = [x.get('data-stat') for x in passing_table("th")]
            table_rows = passing_table("tbody > tr")
            self.passing_data = {}
            for row in table_rows:
                cells = row.findall("td")
                row_data = {}
                year = cells[0].text_content()[:4]
                for i,cell in enumerate(cells[1:]):
                    stat = headers[i+1]
                    row_data[stat] = try_parse(cell.text_content())
                self.passing_data[year] = row_data

            career_row = passing_table("tfoot > tr")
            if type(career_row) is pq:
                career_row = career_row[0]

            cells = career_row.findall("td")
            row_data = {}
            for i,cell in enumerate(cells[1:]):
                stat = headers[i+1]
                row_data[stat] = try_parse(cell.text_content())
            self.passing_data["career"] = row_data
            self.cache()

    def get_years(self):
        return [x for x in self.passing_data.keys() if x != "career"]

    def get_passing_stat(self,_year,_statname):
        for year,data in self.passing_data.iteritems():
            # print year,_year
            if year == str(_year):
                return data[_statname]

    def __str__(self):
        return self.name+" "+'-'.join(self.posns)+" "+self.url

    def get_cache_path(self):
        id = self.url
        return "scraping/data/players/"+id[id.rfind("/")+1:id.rfind(".")]+".json"

    def cache(self):

        with open(self.get_cache_path(),"w") as file:
            json.dump(self.passing_data,file)
