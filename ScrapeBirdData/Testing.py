from LimeScraper import LimeScraper
from Location import Location
import json
import mysql
import unittest

class Tests(unittest.TestCase):

    def testLimeScraper(self):
        """
        Tests keys in the Lime APIs JSON (was getting a KeyError for 'data')

        """
        limescraper = LimeScraper()
        test_loc = Location('33.792173', '-84.424772', 'Bland_Town', 'ATL', ['Lime'])

        JSON = limescraper.curlGetLimes(test_loc, test_loc, test_loc, 50)
        data = JSON['data']['attributes']['bikes']
        print(len(data))
        for d in data:
            print(d['attributes']['last_three'])
    #print(json.dumps(data, indent=4))

    def testMySQLWriteToDB(self):
        """
        Testing writing to the MySQL database
        Figured out how to use 'execute' and 'commit'
        You 

        """
        endpoint = 'gridodatascraper2.csbg5plxwxlz.us-east-2.rds.amazonaws.com'
        connection = mysql.connector.connect(host=endpoint, database='ScooterData', user='yourgrido', password='GridoTushar1691$')
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO ScooterInfo VALUES ('TestScooter3', 'ABC', 'dd372aca-cd93-4e38-a8cc-3d8d4168b0b4', 100, 5000000, 'No update data', 'fe123rf3w', '03:04:05', '2019-01-01');")
            cursor.execute("INSERT INTO ScooterInfo VALUES ('TestScooter4', 'ABC', 'dd372aca-cd93-4e38-a8cc-3d8d4168b0b4', 100, 5000000, 'No update data', 'fe123rf3w', '03:04:05', '2019-01-01');")
            connection.commit()
        except:
            connection.rollback()
        connection.close()



#if __name__ == '__main__':
    #testMySQLWriteToDB()
    #testLimeScraper()
