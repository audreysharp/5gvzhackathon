from math import sin, cos, sqrt, atan2, radians
from collections import OrderedDict
import sys
from collections import defaultdict

class Antenna(object):
    locationCode = ''
    lat = 0
    lon = 0
    antennaHere = False
    antennaType = ''
    antennaID = -1

    def __init__(self, locationCode, lat, lon):
        self.locationCode = locationCode
        self.lat = lat
        self.lon = lon
        self.antennaHere = False
        self.antennaType = ''
        self.antennaID = -1

class House(object):
    lat = 0
    lon = 0

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

# antennaTypes = OrderedDict([('T-5', 500), ('T-4', 400), ('T-3', 300), ('T-2', 200), ('T-1', 100)])
# antennaTypes = OrderedDict([('T-5', 500), ('T-4', 400), ('T-3', 300), ('T-2', 200)]) # ***** 327
# antennaTypes = OrderedDict([('T-3', 300), ('T-4', 400),  ('T-5', 500), ('T-2', 200), ('T-1', 100)])
# antennaTypes = OrderedDict([('T-4', 400),  ('T-5', 500), ('T-3', 300), ('T-2', 200), ('T-1', 100)])
# antennaTypes = OrderedDict([('T-4', 400),  ('T-5', 500), ('T-3', 300), ('T-2', 200)])
# antennaTypes = OrderedDict([('T-5', 500), ('T-3', 300), ('T-4', 400), ('T-2', 200)]) 316
antennaTypes = OrderedDict([('T-5', 500)]) # 318

antennas  = []
houses = []
covered = []

def makeAntenna(locationCode, lat, lon):
    antenna = Antenna(locationCode, lat, lon)
    return antenna

def makeHouse(lat, lon):
    house = House(lat, lon)
    return house

def readJson():
    import json
    global antennas
    global houses

    data = json.load(open('antennaLocations.json'))
    for key, value in data.items():
        antennas.append(makeAntenna(key, value['latitude'], value['longitude']))

    data2 = json.load(open('houseList.json'))
    for key in data2:
        houses.append(makeHouse(key[0], key[1]))

def getDistance(lat1, lat2, lon1, lon2):
    EARTH_RADIUS = 6373.0
    KM_TO_FEET = 3280.84

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = EARTH_RADIUS * c
    feetDistance = distance * KM_TO_FEET

    return feetDistance

def testOverlap(r, x1, x2, y1, y2):
    if (((x1-x2)**2 + (y1-y2)**2) >= 0) and (((x1-x2)**2 + (y1-y2)**2) <= (r+r)**2):
        print('OVERLAP!!!!!!')
        return True

def placeAntennas(type, antennaID):
    global covered
    for i in range(0, len(antennas)): #iterate through each antenna
        if antennas[i] in covered: # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)): # if placing antenna will overlap
                # if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[type]):
                if (testOverlap(antennaTypes[type], antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon)):
                        # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennas[i].antennaType = type
            antennas[i].antennaHere = True
            antennaID += 1
            antennas[i].antennaID = antennaID
            covered.append(antennas[i])
            for j in range(0, len(antennas)):
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[type]):
                        '''if (testOverlap(antennaTypes[type], antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon)):
                            print('AHHHHHHHHHHHHH')
                        else:'''
                        covered.append(antennas[j])
                        antennas[j].antennaID = antennaID
                        antennas[j].antennaType = type

def placeAntennasHouses(type, antennaID):
    global covered
    for i in range(0, len(houses)): #iterate through each antenna
        if houses[i] in covered: # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)): # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennas[i].antennaType = type
            antennaID += 1
            antennas[i].antennaHere = True
            antennas[i].antennaID = antennaID
            covered.append(houses[i])

            for j in range(0, len(houses)):
                if houses[j] not in covered:
                    if (getDistance(antennas[i].lat, houses[j].lat, antennas[i].lon, houses[j].lon) <= antennaTypes[type]):
                        covered.append(houses[j])
                        antennas[j].antennaID = antennaID
                        antennas[j].antennaType = type

def placeAntennasStart(startNum, type, antennaID):
    global covered
    num = startNum
    for i in range(num, len(antennas)): #iterate through each antenna
        if antennas[i] in covered: # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)): # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennas[i].antennaType = type
            antennaID += 1
            antennas[i].antennaHere = True
            antennas[i].antennaID = antennaID
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[type]):
                        covered.append(antennas[j])
                        antennas[j].antennaID = antennaID
                        antennas[j].antennaType = type

    for i in range(0, num): #iterate through each antenna
        if antennas[i] in covered: # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)): # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennas[i].antennaType = type
            antennaID += 1
            antennas[i].antennaID = antennaID
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[type]):
                        covered.append(antennas[j])
                        antennas[j].antennaID = antennaID
                        # antennas[j].antennaType = type
    # print(antennaID)

def getPlacedLocations(type):
    placedAntennas = defaultdict()
    for antenna in antennas:
        if antenna.antennaType == type:
            # print(antenna.locationCode, antenna.antennaType, antenna.antennaID)
            placedAntennas.setdefault(antenna.antennaID, []).append(antenna.locationCode)

    print(type)
    for key, loc in placedAntennas.items():
        print (key, loc)

def countCovered():
    print('COVERED SIZE', len(covered))

def optimizeAntennas():
    '''for antenna in antennas:
        if antenna.antennaID == 0:
            print (antenna.locationCode, antenna.antennaID)'''
    testID = 1
    placed5Antennas = getPlacedLocations('T-5')
    placed4Antennas = getPlacedLocations('T-4')
    placed3Antennas = getPlacedLocations('T-3')
    placed2Antennas = getPlacedLocations('T-2')
    placed1Antennas = getPlacedLocations('T-1')

    '''for i in range(0, 100):
        for type in antennaTypes:
            for antenna in antennas:
                if antenna.antennaType == type and antenna.antennaID == testID:
                    pass
        testID += 1'''

def makeCsv():
    import csv
    import datetime
    csvName = datetime.datetime.now().strftime("%H_%M_%S%Y-%m-%d")
    with open('./csvs/' + csvName + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow(['AntennaLocationCode', 'AntennaType'])
        for antenna in antennas:
            if (antenna.antennaHere):
                writer.writerow([antenna.locationCode, antenna.antennaType])

def main():
    readJson()
    # print (getDistance(antennas[0].lat, antennas[1].lat, antennas[0].lon, antennas[1].lon))
    for type in antennaTypes:
        print ('type', antennaTypes[type])
        placeAntennas(type, 0)
        # placeAntennasStart(603, type, 0)
        # placeAntennasHouses(type, 0)
        print('placed all ', type)
    optimizeAntennas()
    # for antenna in antennas:
    #     if (antenna.antennaType != ''):
    #         print(antenna.locationCode, antenna.antennaType, antenna.antennaID)
    '''for antenna in antennas:
        if antenna.antennaID == -1:
            print(antenna.locationCode, antenna.antennaType, antenna.antennaID)'''
    makeCsv()
    print('csv outputted')
    countCovered()

main()