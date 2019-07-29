from os import system
from time import sleep
from Scraper import Scraper
from Location import Location
import sys

locations = []
with open('locations.txt', 'r') as f:
    legend = f.readline()
    for line in f.readlines():
        if line[0] == '#':
            continue
        pieces = line.strip('\n').split(', ')
        lat, long, name = pieces[0], pieces[1], pieces[2]
        locations.append(Location(lat, long, name))

scraper = Scraper()

intervalMins = int(sys.argv[1]) #15
#scrape_limit = 200
count = 0

if __name__ == "__main__":
    while True:
        
        scraper.getMultipleBirdInfos(locations)
        for loc in locations:
            print(f'----{loc.total} UNIQUE Birds found in {loc.name.replace("_", " ")}----')
            loc.resetTotal()
        scraper.resetSet()
        #print(f'##########################RANGE DIF: {max(scraper.ranges, key=lambda x: x[0])} - {min(scraper.ranges, key=lambda x: x[0])}############')
        scraper.ranges = []
        count += 1
        print(f'----------{count} scrape{"" if count == 1 else "s"} completed by {scraper.getTimeNow(scraper.millisecond_cutoff)}----------')
        for i in range(intervalMins):
            left = intervalMins - i
            print(f'#######{left} minute{"" if left == 1 else "s"} left till next scrape#######')
            sleep(60)
        scrape_limit -= 1
        print(f'--------{scrape_limit} left-------')
