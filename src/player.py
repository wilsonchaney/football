# Will use this to store all stats too
class Player:
    def __init__(self,name,posns,url):
        self.name = name
        self.posns = posns
        self.url = url
    def __str__(self):
        return self.name+" "+'-'.join(self.posns)+" "+self.url