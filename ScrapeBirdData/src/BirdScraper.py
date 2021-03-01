from Scraper import Scraper
import json, os
from Location import Location
import requests
from geohash import Geohash as GH
import mysql
import datetime

gh = GH()

auth = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBVVRIIiwidXNlcl9pZCI6ImY0YWNmYWU2LTNiM2MtNDRlZC05MWYxLTA0NDMzZjEyNWZhNiIsImRldmljZV9pZCI6IjU2MTlCNjhCLTIyMEItNEEwQi04NUQzLTQzMTU3Q0VCMkQ2OCIsImV4cCI6MTU5MzM5NDU4N30.f0gnahVvdj9GkgjXM-XXDHGeHUXAJ6uBK05SxMoCwXY"
cookie = "__cfduid=da3e3fe39e31ab9dc385ec173080443c81561419371"
host = 'api.birdapp.com'
url = f'https://{host}/bird/nearby'

#endpoint = 'gridodatascraper2.csbg5plxwxlz.us-east-2.rds.amazonaws.com'
#connection = mysql.connector.connect(host=endpoint, database='ScooterData', user='yourgrido', password='GridoTushar1691$')

class BirdScraper(Scraper):

    def __init__(self):
        super().__init__()
        #self.seen = set()
        self.scooter_type = 'Bird'
        #self.connection = mysql.connector.connect(host=endpoint, database='ScooterData', user='yourgrido', password='GridoTushar1691$')
        #self.cursor = self.connection.cursor()

    def curlGetBirds(self, loc, radius="100"):
        self.params = {'latitude': loc.lat, 'longitude': loc.long, 'radius': radius}
        self.headers = {'Accept': '*/*', 'App-Version': '4.41.0',
                   'Authorization': f'Bearer {auth}',
                   'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
                   'Device-id': '5619B68B-220B-4A0B-85D3-43157CEB2D68',
                   'Host': host, 'Location': f'{{"latitude": {loc.lat}, "longitude":{loc.long}, "radius":{radius}}}',
                   'cookie': cookie}
        return super().curlGet(url, self.params, self.headers)

    def writeToDB(self, jsonitem, city_name):
        location_hash = gh.encode(float(jsonitem["location"]["latitude"]), float(jsonitem["location"]["longitude"]))
        curr_datetime = datetime.datetime.now()
        curr_time = str(curr_datetime.time().strftime('%H:%M:%S'))
        curr_date = str(curr_datetime.date())
        values = f"'{self.scooter_type}', '{city_name}', '{jsonitem['id']}', {jsonitem['battery_level']}, {jsonitem['estimated_range']}, 'No update data', '{location_hash}', '{curr_time}', '{curr_date}', '{jsonitem['model']}'"
        command = f'INSERT INTO {super().tblname} VALUES ({values});'
        super().cursor.execute(command)

    def writeLine(self, jsonitem, foldername, filename, city_name):
        filepath, option = super().prepareFiles(foldername, filename)
        with open(filepath, option) as file:
            location_hash = gh.encode(float(jsonitem["location"]["latitude"]), float(jsonitem["location"]["longitude"]))
            to_write = ', '.join([self.scooter_type, city_name, jsonitem["id"], str(jsonitem["battery_level"]), str(jsonitem["estimated_range"]), 'No update data', location_hash])+'\n'
            file.write(to_write)

    def getSpecificInfo(self, loc, city_name):
        dataJSON = self.curlGetBirds(loc, '100')
        for elem in dataJSON['birds']:
            if elem['id'] not in self.seen:
                loc.scooter_counts['Bird'] += 1
                self.seen.add(elem['id'])
                #------WRITE TO DB----------
                #TODO self.writeToDB(elem, city_name)
                #------END WRITE TO DB--------
                #self.writeLine(elem, 'IDData', f'{super().getTimeNow(super().millisecond_cutoff-3)}.txt', city_name)


    def getMultipleInfos(self, locations, city_name):
        for loc in locations:
            try:
                self.getSpecificInfo(loc, city_name)
            except (json.decoder.JSONDecodeError, json.JSONDecodeError) as e:
                continue
        super().connection.commit()
