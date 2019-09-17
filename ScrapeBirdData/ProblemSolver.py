import json, os
from geohash import Geohash as GH

def getTimeRange(time, radius):
    time_range = []

    pieces = time.split(':')
    #print(pieces)
    seconds = int(pieces[2])

    addendum = 1 if seconds >= 30 else 0
    minutes = int(pieces[1]) + addendum

    addenduh = 0
    if minutes == 60:
        addenduh = 1
        minutes = 0
    hours = int(pieces[0]) + addenduh

    #print(hours, minutes)
    zero_pad_hours = ''
    for i in range(-radius, radius+1):
        currMin = minutes + i
        currHour = hours
        if minutes + i == 60:
            currHour = hours + 1
            currMin = 0
        elif minutes + i > 60:
            currHour = hours + 1
            currMin = minutes + i - 60
        elif minutes + i < 0:
            currMin = 60 + i
            currHour = hours - 1

        if currHour < 0:
            currHour = 23 + hours

        zero_pad_minutes = ''
        if len(str(currMin)) == 1:
            zero_pad_minutes = '0'
        if currHour == 24:
            currHour = 0
        if len(str(currHour)) == 1:
            zero_pad_hours = '0'
        time_range.append(f'{zero_pad_hours}{currHour}:{zero_pad_minutes}{currMin}')
    return time_range

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

def find100s(foldername):
    for filename in os.listdir(foldername):
        #with open(filename)
        pass

def convGeohashes():
    gh = GH()
    converted_file = open('jorge_geohashes_latlong.txt', 'w+')
    with open('jorge_geohashes.txt', 'r') as readfile:
        for line in readfile.readlines():
            hash = line.strip('\n')
            latlong = gh.decode_exactly(hash)
            output = [round(float(latlong[0]), 5), round(float(latlong[1]), 5)]
            converted_file.write(f'{output[0]}, {output[1]}\n')

def concentrations(foldername, dtime, precision):
    """
    finds clusters of scooters based on geohash precision

    """
    cluster_count = {}
    time_range = getTimeRange(dtime, 1)
    for filename in os.listdir(foldername):
        with open(f'{foldername}/{filename}', 'r') as file:
            for line in file.readlines():
                pieces = line.split(', ')
                time = pieces[0].split()[1]
                print(time_range)
                print(time)
                if time[:5] in time_range:
                    if pieces[3] in cluster_count:
                        cluster_count[pieces[3][:precision]] += 1
                    else:
                        cluster_count.update({pieces[3][:precision]: 0})
                    break
    return cluster_count

eg = '2019-08-01 16:43:58, 96, 13430, 9g3qrj7xj3d8'

if __name__ == '__main__':
    print(concentrations('BirdIDData', '16:43:00', 2))
    #print(findDuplicates('July 12 nonuniques'))
    #for name in filenames:
    #    findRadius(name)
    #convGeohashes()
