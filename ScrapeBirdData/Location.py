class Location:
    def __init__(self, lat, long, name=''):
        self.lat = lat
        self.long = long
        self.name = name
        self.total = 0

    def resetTotal(self):
        self.total = 0
