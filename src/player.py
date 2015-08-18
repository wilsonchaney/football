from pyquery import PyQuery as pq


# Will use this to store all stats too
class Player:
    def __init__(self,name,posns,url):
        self.name = name
        self.posns = posns
        self.url = url

    def read_page(self):
        self.page = pq('http://www.pro-football-reference.com/'+self.url)

    def populate_passing_data(self):
        passing_table = self.page("div#div_passing")
        headers = [x.get('data-stat') for x in passing_table("th")]
        table_rows = passing_table("tbody > tr")
        self.passing_data = {}
        for row in table_rows:
            cells = row.findall("td")
            row_data = {}
            year = int(cells[0].text_content()[:4])
            for i,cell in enumerate(cells[1:]):
                stat = headers[i]
                row_data[stat] = cell.text_content()
            self.passing_data[year] = row_data
        self.start_year = min(self.passing_data.keys())
        self.end_year = max(self.passing_data.keys())


    def get_passing_stat(self,_year,_statname):
        for year,data in self.passing_data.iteritems():
            # print year,_year
            if year == _year:
                return data[_statname]

    def __str__(self):
        return self.name+" "+'-'.join(self.posns)+" "+self.url