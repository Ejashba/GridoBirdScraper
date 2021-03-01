class Location:
    def __init__(self, lat, long, name, city, scooter_names):
        self.lat = lat
        self.long = long
        self.name = name
        self.city = city
        self.scooter_counts = {s: 0 for s in scooter_names}

    def resetCounts(self):
        for s in self.scooter_counts:
            self.scooter_counts[s] = 0
