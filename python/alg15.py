from math import sin, cos, sqrt, atan2, radians
from collections import OrderedDict


class Antenna(object):
    locationCode = ''
    lat = 0
    lon = 0
    antennaType = ''

    def __init__(self, locationCode, lat, lon):
        self.locationCode = locationCode
        self.lat = lat
        self.lon = lon
        self.antennaType = ''


antennaTypes = OrderedDict([('T-5', 500),('T-4', 400), ('T-3', 300), ('T-2', 200), ('T-1', 100)])
#antennaTypes = OrderedDict([('T-5', 500), ('T-4', 400), ('T-3', 300), ('T-2', 200)])  # ***** 327
# antennaTypes = OrderedDict([('T-3', 300), ('T-4', 400),  ('T-5', 500), ('T-2', 200), ('T-1', 100)])
# antennaTypes = OrderedDict([('T-4', 400),  ('T-5', 500), ('T-3', 300), ('T-2', 200), ('T-1', 100)])
# antennaTypes = OrderedDict([('T-4', 400),  ('T-5', 500), ('T-3', 300), ('T-2', 200)])
# antennaTypes = OrderedDict([('T-5', 500), ('T-3', 300), ('T-4', 400), ('T-2', 200)]) 316
# antennaTypes = OrderedDict([('T-5', 500), ('T-4', 400), ('T-3', 300)]) 318

antennas = []
covered = []


def makeAntenna(locationCode, lat, lon):
    antenna = Antenna(locationCode, lat, lon)
    return antenna


def readJson():
    import json
    global antennas

    data = json.load(open('antennaLocations.json'))
    for key, value in data.items():
        antennas.append(makeAntenna(key, value['latitude'], value['longitude']))


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


def placeAntennas(type):
    for i in range(0, len(antennas)):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennas[i].antennaType = type
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type

def placeAntennaOne(type):
    print("entered one")
    for i in range(0, len(antennas)):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennaCount = 0
            for x in range(0, len(antennas)):
                if (getDistance(antennas[i].lat, antennas[x].lat, antennas[i].lon, antennas[x].lon) <= 100):
                    antennaCount += 1
                    #print("antennaCount: ", antennaCount)
            if antennaCount >= 9:
               # print("antennaCount PLACED: ", antennaCount)
                antennas[i].antennaType = type #place the antenna
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):  #go through each antenna covered and put them in the covered list
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type
    print("exited one")

def placeAntennaFive(type):
    print("entered five")
    num = 63
    for i in range(num, len(antennas)):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennaCount = 0
            for x in range(0, len(antennas)):
                if (getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon) <= 500):
                    #print(getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon))
                    antennaCount += 1
                    #print(antennaCount)
            if antennaCount >= 12:
                #print("antenna count is: ", antennaCount)
                antennaCount = 0
                antennas[i].antennaType = type #place the antenna
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):  #go through each antenna covered and put them in the covered list
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type

    #=============================================================================================================

    for i in range(0, num):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennaCount = 0
            for x in range(0, len(antennas)):
                if (getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon) <= 500):
                    #print(getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon))
                    antennaCount += 1
                    #print(antennaCount)
            if antennaCount >= 12:
                #print("antenna count is: ", antennaCount)
                antennaCount = 0
                antennas[i].antennaType = type #place the antenna
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):  #go through each antenna covered and put them in the covered list
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type
    print("exited five")

def placeAntennaFour(type):
    print("entered four")
    for i in range(0, len(antennas)):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennaCount = 0
            for x in range(0, len(antennas)):
                if (getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon) <= 400):
                    #print(getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon))
                    antennaCount += 1
                    #print(antennaCount)
            if antennaCount >= 17:
                #print("antenna count is: ", antennaCount)
                antennaCount = 0
                antennas[i].antennaType = type #place the antenna
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):  #go through each antenna covered and put them in the covered list
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type
    print("exited four")

def placeAntennaThree(type):
    print("entered three")
    for i in range(0, len(antennas)):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennaCount = 0
            for x in range(0, len(antennas)):
                if (getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon) <= 300):
                    #print(getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon))
                    antennaCount += 1
                    #print(antennaCount)
            if antennaCount >= 6:
                #print("antenna count is: ", antennaCount)
                antennaCount = 0
                antennas[i].antennaType = type #place the antenna
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):  #go through each antenna covered and put them in the covered list
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type
    print("exited three")

def placeAntennaTwo(type):
    print("entered two")
    for i in range(0, len(antennas)):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennaCount = 0
            for x in range(0, len(antennas)):
                if (getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon) <= 200):
                    #print(getDistance(antennas[i].lat,antennas[x].lat,antennas[i].lon,antennas[x].lon))
                    antennaCount += 1
                    #print(antennaCount)
            if antennaCount >= 8:
                #print("antenna count is: ", antennaCount)
                antennaCount = 0
                antennas[i].antennaType = type #place the antenna
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):  #go through each antenna covered and put them in the covered list
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type
    print("exited two")
def placeAntennasStart(type):
    num = 930
    for i in range(num, len(antennas)):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennas[i].antennaType = type
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type

    for i in range(0, num):  # iterate through each antenna
        if antennas[i] in covered:  # if the antenna is already covered, go to next antenna
            # print(i, antennaTypes[type], 'ALREADY COVERED')
            continue
        else:
            goNext = False
            for k in range(0, len(covered)):  # if placing antenna will overlap
                if (getDistance(antennas[i].lat, covered[k].lat, antennas[i].lon, covered[k].lon) <= antennaTypes[
                    type]):
                    # print(i, antennaTypes[type], 'PLACING A T-5 HERE WILL OVERLAP')
                    goNext = True
                    break
            if goNext == True:
                continue
            antennas[i].antennaType = type
            covered.append(antennas[i])
            # print(i, 'T-5')
            for j in range(0, len(antennas)):
                if antennas[j] not in covered:
                    if (getDistance(antennas[i].lat, antennas[j].lat, antennas[i].lon, antennas[j].lon) <= antennaTypes[
                        type]):
                        covered.append(antennas[j])
                        # antennas[j].antennaType = type


def main():
    readJson()
    # print (getDistance(antennas[0].lat, antennas[1].lat, antennas[0].lon, antennas[1].lon))
    for type in antennaTypes:
        print(antennaTypes[type])
        if(type == "T-5"):
           placeAntennaFive(type)
        elif(type == "T-1"):
            placeAntennaOne(type)
        elif(type == "T-4"):
            placeAntennaFour(type)
        elif(type == "T-3"):
            placeAntennaThree(type)
        elif (type == "T-2"):
            placeAntennaTwo(type)
        else:
            placeAntennas(type)
        # placeAntennasStart(type)
        print('placed all ', type)
    print("AntennaLocationCode,AntennaType")
    for antenna in antennas:
        if (antenna.antennaType != ''):
            print(antenna.locationCode + ',' + antenna.antennaType)


main()