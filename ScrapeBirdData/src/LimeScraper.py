from Scraper import Scraper
import json, os
import datetime
from Location import Location
import requests
from geohash import Geohash as GH
import pygeohash as pgh
#import urllib
#from flask import jsonify
from mysql import connector
#import boto3  #------UNCOMMENT------
import time

from geohash import Geohash as GH
gh = GH()

auth = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3Rva2VuIjoiVk1RQkZUV0o1WUtESyIsImxvZ2luX2NvdW50IjoxMX0.mAg5d2N8Xjrw2X55FQ4kOTiY2w0VndT7ttICedc6PgQ"
cookie = "_limebike-web_session=ZWVwYW9CcUtObkVjUWtVMWlxL01XT0k1R2liaC96a01QNEpHVnM5VmhjeUw4elFPS1o4aUVLemJnV0pLUGZWUUU0WmZSaDdYYmVuYjRIQ1dJKzNJVGJFY1NTd1pOU0NEcjkvVGdLNFlqbTlRM3lJbFFCZ25rS21YU3g4Ry9FOXdhQWxmWHYzZUk5dlFYRGR5VStVcWZiR2kzc0RLbFNyRENERkVraUlKeDVRdFU4ZVBCY0N2ZXJlQUtHQWFGL3IySmZFZndtQ0Z2YXhJSmgyOUl1KzBUNVVkSTRvMFJ4bU5zUU1MWHh3elUyTnFxSWZWMlJsM1RVRnlMT05CbmIydlVTTWtIekozVXFsTUMyazlzSmJDeTNZRS9FME5CRGk5L2tFdlZOcU8vcVltbVU5Skc0b1daZGdxWktXMGZCMWxHTldYQThBU3dYVWVkRHpRMThQRXNpVkNtNERBNVVrVzRZWCtlQzY1TXJrS2lhMDI3S3JPOC9XeGJjZ3pScG4vamJvaHhWdXlGeW4xUXY0R094YUl6ZS9JMncrUG1VMk1YdVV6VzE1QXo2ZHhYQkZsVVpYWHlOK29wdWE1alFMNS0tSVVWUHQ4TVRZN0xRWW11OU9zQjJsUT09--578597c6c34ac604992c4dc40d6c2f82f2dd5132"
url = 'https://web-production.lime.bike/api/rider/v1/views/map'

class LimeScraper(Scraper):

    def __init__(self):
        #self.seen = set()
        super().__init__()
        self.scooter_type = 'Lime'
        self.duplicates = []
        self.ping_count = 0

    def curlGetLimes(self, usrloc, swloc, neloc, zoom):
        headers = {'authorization': f'Bearer {auth}', 'cookie': cookie}
        params = {'ne_lat': neloc.lat, 'ne_lng': neloc.long, 'sw_lat': swloc.lat, 'sw_lng': swloc.long, 'user_latitude': usrloc.lat, 'user_longitude': usrloc.long, 'zoom': zoom}
        return super().curlGet(url, self.params, self.headers)
        #response = requests.get(url, params=params, headers=headers)
        #return response.json()

    def writeLine(self, jsonitem, foldername, filename, city_name):
        filepath, option = super().prepareFiles(foldername, filename)
        with open(filepath, option) as file:
            item_attributes = jsonitem['attributes']
            location_hash = gh.encode(float(item_attributes["latitude"]), float(item_attributes["longitude"]))
            file.write(', '.join([self.scooter_type, city_name, item_attributes["last_three"], item_attributes["battery_level"], str(item_attributes["meter_range"]), item_attributes["last_activity_at"], location_hash])+'\n')

    def writeToDB(self, jsonitem, city_name):
        item_attributes = jsonitem['attributes']
        location_hash = gh.encode(float(item_attributes["latitude"]), float(item_attributes["longitude"]))
        curr_datetime = datetime.datetime.now()
        curr_time = str(curr_datetime.time().strftime('%H:%M:%S'))
        curr_date = str(curr_datetime.date())
        values = f"'{self.scooter_type}', '{city_name}', '{item_attributes['last_three']}', {item_attributes['battery_level']}, {item_attributes['meter_range']}, '{item_attributes['last_activity_at']}', '{location_hash}', '{curr_time}', '{curr_date}', '{item_attributes['type_name']}'" #TODOOOOOOO
        command = f'INSERT INTO {super().tblname} VALUES ({values});'
        #print(command)
        super().cursor.execute(command)

    #IMPORTANT: Lime API as of Summer 2019 does not allow repeated HTTP requests within unknown amount of time,
    #Pinging every 3 seconds seemed to strike the best balance between request returning responses
    def getSpecificInfo(self, loc, city_name, zoom=16):
        dataJSON = self.curlGetLimes(loc, loc, loc, zoom) #TESTING zoom as int vs str
        #dynamodb = boto3.client('dynamodb') #-----UNCOMMENT------
        #dynamodb = boto3.resource('dynamodb')
        try: #see if JSON returned a response
            eg = dataJSON['data']
        except (KeyError, TypeError) as e:
            #print(f'\n\n-------missed---------\n{dataJSON}\n\n')
            print(f'ping #{self.ping_count} at {loc.name} rejected')
            time.sleep(3) #try sleep(3)
            return None
        print(self.ping_count)
        for elem in dataJSON['data']['attributes']['bikes']:
            #print(self.ping_count)
            #print(elem)
            last_three = elem['attributes']['last_three']
            if last_three not in self.seen:
                loc.scooter_counts['Lime'] += 1
                self.seen.add(last_three)
                #------WRITE TO DB----------
                self.writeToDB(elem, city_name)
                #------END WRITE TO DB--------
                #self.writeLine(elem, 'IDData', f'{super().getTimeNow(super().millisecond_cutoff-3)}.txt', city_name)
            elif last_three in self.seen:
                self.duplicates.append(last_three)
        #-----UNCOMMENT-------
            #dynamodb.put_item(TableName='LimeIdData', Item={'scooterId':{'S':elem['id']},'timestamp':{'S':self.getTimeNow(self.millisecond_cutoff)}, 'batteryLevel':{'N':str(elem['battery_level'])}})
        return dataJSON

    def getMultipleInfos(self, locations, city_name):
        start = time.time()
        errmsg = "{'error_message': 'Too many attempts. Please wait and try again later.'}"
        i = 0
        for loc in locations:
            locJSON = self.getSpecificInfo(loc, city_name, 50)
            if not locJSON:
                locations.append(loc)
            print(f'{len(locations) - i} left')
            self.ping_count += 1
            i += 1
        super().connection.commit()
        print(time.time() - start)
                #self.getSpecificInfo(loc, city_name, 50) #TESTING zoom param
            #except (json.decoder.JSONDecodeError, json.JSONDecodeError) as e:
