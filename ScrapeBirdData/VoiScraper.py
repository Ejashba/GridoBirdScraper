import json, os
import datetime
from Location import Location
import requests
from geohash import Geohash as GH
import pygeohash as pgh
#import urllib
#from flask import jsonify
from mysql import connector
from Scraper import Scraper


gh = GH()

class VoiScraper(Scraper):
    def __init__(self):
        self.seen = set()
        self.scooter_type = 'Voi'

    def writeLine(self, jsonitem, foldername, filename, city_name):
        filepath, option = super().prepareFiles(foldername, filename)
        with open(filepath, option) as file:
            location_hash = gh.encode(float(jsonitem["location"][0]), float(jsonitem["location"][1]))
            file.write(', '.join([self.scooter_type, city_name, jsonitem["id"], str(jsonitem["battery"]), 'No range data', jsonitem['updated'], location_hash])+'\n')

    def writeToDB(self, jsonitem, city_name):
        location_hash = gh.encode(float(jsonitem["location"][0]), float(jsonitem["location"][1]))
        curr_datetime = datetime.datetime.now()
        curr_time = str(curr_datetime.time().strftime('%H:%M:%S'))
        curr_date = str(curr_datetime.date())
        no_range_data_placeholder = -1
        values = f"'{self.scooter_type}', '{city_name}', '{jsonitem['id']}', {jsonitem['battery']}, {no_range_data_placeholder}, '{jsonitem['updated']}', '{location_hash}', '{curr_time}', '{curr_date}', '{jsonitem['type']}'"
        command = f'INSERT INTO {super().tblname} VALUES ({values});'
        super().cursor.execute(command)

    def curlGetVois(self, loc):
        url = 'https://api.voiapp.io/v1/vehicle/status/ready'
        params = {'lat': loc.lat, 'lng': loc.long}
        response = requests.get(url, params=params)
        return response.json()

    def getSpecificInfo(self, loc, city_name):
        dataJSON = self.curlGetVois(loc)
        for elem in dataJSON:
            if elem['id'] not in self.seen:
                loc.scooter_counts['Voi'] += 1
                self.seen.add(elem['id'])
                #------WRITE TO DB----------
                self.writeToDB(elem, city_name)
                #------END WRITE TO DB--------
                #self.writeLine(elem, 'IDData', f'{super().getTimeNow(super().millisecond_cutoff-3)}.txt', city_name)

    def getMultipleInfos(self, locations, city_name):
        for loc in locations:
            try:
                self.getSpecificInfo(loc, city_name)
            except (json.decoder.JSONDecodeError, json.JSONDecodeError) as e:
                continue
        super().connection.commit()
