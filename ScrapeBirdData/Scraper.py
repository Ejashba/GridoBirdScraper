import json, os
from datetime import datetime
from Location import Location
import requests
from geohash import Geohash as GH
#from flask import jsonify
import mysql.connector

class Scraper:

    standard_format = '%Y-%m-%d %H:%M:%S'
    colnames = ['ScooterCompany', 'City', 'ID', 'BatteryLevel', 'EstimatedRange', 'LastUpdated', 'Geohash', 'TimeUploaded', 'DateUploaded', 'ScooterModel']
    tblname = 'ScooterInfo'

    endpoint = 'gridodatascraper2.csbg5plxwxlz.us-east-2.rds.amazonaws.com'
    connection = mysql.connector.connect(host=endpoint, database='ScooterData', user='yourgrido', password='GridoTushar1691$')
    cursor = connection.cursor()

    def getTimeNow(self, format):
        return datetime.now().strftime(format)

    def prepareFiles(self, foldername, filename):
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        filepath = f'{foldername}/{filename}'
        option = 'a'
        if not os.path.exists(filepath):
            option = 'w+'
        return filepath, option

    def curlGet(self, url, params, headers):
        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def writeToDB(self, host, user, passwd):
        return
        #db = mysql.connector.connect(host=, user=, passwd=)
