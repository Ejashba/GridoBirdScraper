import json, os
from datetime import datetime
from Location import Location
import requests
import urllib
from flask import jsonify
#import boto3  #------UNCOMMENT------

class Scraper:
    def __init__(self):
        self.millisecond_cutoff = 19
        self.seen = set() # set of IDs
        self.birdAuth = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBVVRIIiwidXNlcl9pZCI6ImY0YWNmYWU2LTNiM2MtNDRlZC05MWYxLTA0NDMzZjEyNWZhNiIsImRldmljZV9pZCI6IjU2MTlCNjhCLTIyMEItNEEwQi04NUQzLTQzMTU3Q0VCMkQ2OCIsImV4cCI6MTU5MzM5NDU4N30.f0gnahVvdj9GkgjXM-XXDHGeHUXAJ6uBK05SxMoCwXY"
        self.birdCookie = "__cfduid=da3e3fe39e31ab9dc385ec173080443c81561419371"
        self.ranges = []

    def resetSet(self):
        self.seen = set()

    def getTimeNow(self, cutoff):
        return str(datetime.now())[:cutoff]

    def curlGetBirds(self, loc, radius):
        host = 'api.birdapp.com'
        params = {'latitude': loc.lat, 'longitude': loc.long, 'radius': radius}
        headers = {'Accept': '*/*', 'App-Version': '4.41.0',
                   'Authorization': f'Bearer {self.birdAuth}',
                   'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
                   'Device-id': '5619B68B-220B-4A0B-85D3-43157CEB2D68',
                   'Host': host, 'Location': f'{{"latitude": {loc.lat}, "longitude":{loc.long}, "radius":{radius}}}',
                   'cookie': self.birdCookie}
        response = requests.get(f'https://{host}/bird/nearby', params=params, headers=headers)
        return response.json()

    def getJSON(self, output_filename):
        with open(f'{output_filename}.json', 'r') as f:
            JSON = json.load(f)
        return JSON

    def getSpecificBirdInfo(self, loc, overflow=-1):
        birdDataJSON = self.curlGetBirds(loc, '100')

        #dynamodb = boto3.client('dynamodb') #-----UNCOMMENT------

        for elem in birdDataJSON['birds']:
            if overflow == 0:
                break
            overflow -= 1
            if elem['id'] not in self.seen:
                loc.total += 1
                self.seen.add(elem['id'])
                
        # ------WRITES FILES--------
                filename = f'Bird {elem["id"]}.txt'
                foldername = 'BirdIDData'
                if not os.path.exists(foldername):
                    os.makedirs(foldername)
                filepath = f'{foldername}/{filename}'
                option = 'a'
                if not os.path.exists(filepath):
                    option = 'w+'
                file = open(filepath, option)
                file.write(f'{self.getTimeNow(self.millisecond_cutoff)}, {str(elem["battery_level"])}, {str(elem["estimated_range"])}\n')
                file.close()
                self.ranges.append([elem["estimated_range"], elem["battery_level"]])
                #print(self.ranges)
        #---------END WRITING FILES---------

        #-----UNCOMMENT-------
            #dynamodb.put_item(TableName='BirdIdData', Item={'scooterId':{'S':elem['id']},'timestamp':{'S':self.getTimeNow(self.millisecond_cutoff)}, 'batteryLevel':{'N':str(elem['battery_level'])}})

    def getMultipleBirdInfos(self, locations):
        for loc in locations:
            try:
                self.getSpecificBirdInfo(loc)
            except (json.decoder.JSONDecodeError, json.JSONDecodeError) as e:
                continue
