import json, os

def findDiameter(filename):
    with open(filename, 'r') as f:
        JSONdata = json.load(f)

    minLat, maxLat = 200, -200
    minLong, maxLong = 200, -200

    for elem in JSONdata['birds']:
        currLoc = elem['location']
        currLat = float(currLoc['latitude'])
        currLong = float(currLoc['longitude'])
        if currLat < minLat:
            minLat = currLat
        if currLat > maxLat:
            maxLat = currLat
        if currLong < minLong:
            minLong = currLong
        if currLong > maxLong:
            maxLong = currLong

    latDiff = abs(maxLat - minLat)
    longDiff = abs(maxLong - minLong)

    latToMetres = 110.574
    longToMetres = 111.32

    print(f'------ ({filename}) Lat: {latDiff*latToMetres}m, Long: {longDiff*longToMetres}km ------')

def findDuplicates(dirpath):
    seen = set()
    duplicateCount = 0
    for filename in os.listdir(dirpath):
        if filename in seen:
            duplicateCount += 1
        else:
            seen.add(filename)
    return duplicateCount

filenames = [
'BirdOutputCurl - Angel_of_Independence.json',
'BirdOutputCurl - Condesa.json',
'BirdOutputCurl - Polanco.json',
'BirdOutputCurl - Puebla.json'
]

if __name__ == '__main__':
    #print(findDuplicates('July 12 nonuniques'))
    for name in filenames:
        findRadius(name)
