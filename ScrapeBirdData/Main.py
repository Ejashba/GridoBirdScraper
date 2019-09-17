import os
from time import sleep
from BirdScraper import BirdScraper
from LimeScraper import LimeScraper
from VoiScraper import VoiScraper
from Location import Location
import sys
from datetime import datetime
import mysql

standard_format = '%Y-%m-%d %H:%M:%S'

def getTimeNow(format):
    return datetime.now().strftime(format)

scooter_list = ['Bird', 'Lime', 'Voi']

city_name_dict = {
                    'MEX': 'MexicoCity',
                    'PBC': 'Puebla',
                    'ATL': 'Atlanta',
                    'OSL': 'Oslo'
                  }

scooters_scraped_by_city =  {
                        'MEX': ['Bird'],
                        'PBC': ['Bird'],
                        'ATL': ['Lime'],
                        'OSL': ['Voi']
                    }

def getCodeFromFilename(filename):
    """
    takes away .txt extension

    """
    return filename.split('.')[0]

def getListOfLocations(foldername, filename):
    locations = []
    with open(f'{foldername}/{filename}', 'r') as f:
        #legend = f.readline()
        for line in f.readlines():
            if line[0] == '#': #ignore lines that start with hashtags
                continue
            pieces = line.strip('\n').split(', ')
            lat, long, name = pieces[0], pieces[1], pieces[2]
            city_name = getCodeFromFilename(filename)
            locations.append(Location(lat, long, name, city_name, scooters_scraped_by_city[city_name]))
    return locations

bird_scraper = BirdScraper() #should need to add connector variable
lime_scraper = LimeScraper()
voi_scraper = VoiScraper()

scrapers = {'Bird': bird_scraper, 'Lime': lime_scraper, 'Voi': voi_scraper}

def resetScrapers():
    for s in scrapers:
        scrapers[s].seen = set()

intervalMins = 15#int(sys.argv[1]) #15
count = 0

total_scooters = {s: 0 for s in scooter_list}
if __name__ == "__main__":
    pingfoldername = 'PingLocations'
    desired_cities = city_name_dict.keys() #default is ALL cities
    desired_cities = ['MEX', 'PBC'] #add custom desired cities
    try:
        while True:
            #scraping operation
            for city_filename in os.listdir(pingfoldername): #for ATL.txt, MEX.txt, ...
                city_code = getCodeFromFilename(city_filename)
                if city_code not in desired_cities:
                    continue
                print(f'------starting {city_code} at {datetime.now()}------')
                locs = getListOfLocations(pingfoldername, city_filename)
                for scooter_name in scrapers:
                    #print(scrapers[scooter_name].scooter_type, scooters_scraped_by_city[city_code])
                    if scrapers[scooter_name].scooter_type in scooters_scraped_by_city[city_code]:
                        scrapers[scooter_name].getMultipleInfos(locs, city_code)
                    #connection.commit() #commit entering data to DB


                #prints scraping output to console
                print(f'For {city_name_dict[city_code]}:')
                for loc in locs: #for lat, long, Ansley_Park; lat, long, Puebla_Central, etc.
                    toprint = f'\t- {loc.name.replace("_", " ")}: '
                    scooter_counts = []
                    for scooter_type in scooters_scraped_by_city[loc.city]:
                        scooter_counts.append(f'{loc.scooter_counts[scooter_type]} {scooter_type}{"" if loc.scooter_counts[scooter_type] == 1 else "s"}') #e.g. 113 Birds, 49 Limes
                        total_scooters[scooter_type] += int(loc.scooter_counts[scooter_type])
                    toprint += ', '.join(scooter_counts)
                    print(toprint)
                    loc.resetCounts()
                print(total_scooters)
                if total_scooters['Lime'] > 0:
                    print(f'{len(scrapers["Lime"].duplicates)} Lime duplicates in {city_code}')
                    scrapers["Lime"].duplicates = []
                total_scooters = {s: 0 for s in scooter_list}
            resetScrapers()

            #print(f'##########################RANGE DIF: {max(scraper.ranges, key=lambda x: x[0])} - {min(scraper.ranges, key=lambda x: x[0])}############')
            count += 1
            print(f'----------{count} scrape{"" if count == 1 else "s"} completed by {getTimeNow(standard_format)}----------')
            for i in range(intervalMins):
                left = intervalMins - i
                print(f'#######{left} minute{"" if left == 1 else "s"} left till next scrape#######')
                sleep(60)
    except KeyboardInterrupt:
        #connection.close()
        print('\n------connection to DB closed------\n')
