import random
from station import Station
from road import Road
from encodeStation import *
from const import *
def generateMap(stationNum,width,height,marginW,marginH):
    loX, hiX = marginW*4//3, width - marginW*4//3
    loY, hiY = marginH*2//3, height - marginH*7//5
    rows = int((stationNum*(hiY-loY)/(hiX-loX))**0.5)
    cols = int(rows*(hiX - loX)/(hiY - loY))
    while rows*cols < stationNum:
        cols += 1
    exc = rows*cols - stationNum
    stations = [[0]*cols for row in range(rows)]
    #randomly pick some cells that have no station and mark them
    for i in range(exc):
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        while stations[row][col] == None:
            row = random.randint(0,rows-1)
            col = random.randint(0,cols-1)
        stations[row][col] = None
    sizeX = (hiX - loX)/cols
    sizeY = (hiY - loY)/rows
    #randomly locate stations for each cell
    #stations = set()
    count = 0
    for row in range(rows):
        for col in range(cols):
            if stations[row][col] != None:
                y = random.randint(loY + int(row*sizeY), loY + int((row+1)*sizeY))
                x = random.randint(loX + int(col*sizeX), loX + int((col+1)*sizeX))
                stations[row][col] = Station(x,y,count,row,col)
                count += 1
                #stations.add(board[row][col])
    roads = set()
    minConnect(stations, roads)
    denseConnect(stations, roads)
    return (stations, roads)
#from maze solving
def minConnect(stations, roads):
    rows = len(stations)
    cols = len(stations[0])
    while not Connected(stations):
        row, col = random.randint(0,rows-1),random.randint(0,cols-1)
        if stations[row][col] == None: continue
        start = stations[row][col]
        if flipCoin():
            col = col + 1 if col < cols - 1 else col - 1
        else:
            row = row + 1 if row < rows - 1 else row - 1
        if stations[row][col] == None or stations[row][col].number == start.number: 
            continue
        target = stations[row][col]
        newRoad = Road(start,target,random.sample(list(randCOLORSET),1)[0],rows*cols)
        if newRoad.invalid(roads):
            continue
        start.connectDots(target)
        roads.add(newRoad)
        uniNumber(stations, start, target)
    return

def uniNumber(stations,start,target):
    left = target.number
    right = start.number
    minn = min(left,right)
    rows = len(stations)
    cols = len(stations[0])
    for row in range(rows):
        for col in range(cols):
            curr = stations[row][col]
            if curr != None:
                #print(curr.number, start.number,target.number)
                if (curr.number == left or curr.number == right):
                    curr.number = minn


def Connected(stations):
    rows = len(stations)
    cols = len(stations[0])
    for row in range(rows):
        for col in range(cols):
            if stations[row][col] == None: continue
            if stations[row][col].number != 0:
                return False
    return True

def flipCoin():
    return random.choice([True, False])

def denseConnect(stations, roads):
    rows = len(stations)
    cols = len(stations[0])
    for row in range(rows):
        for col in range(cols):
            if stations[row][col] != None:
                times = 0
                while len(stations[row][col].conStation) < 3:

                    connectNearDot(stations,row,col,roads)
                    times += 1
                    if times >= 20:
                        break
    return

def connectNearDot(stations,row,col, roads):
    rows = len(stations)
    cols = len(stations[0])
    rowRange = list(range(max(0,row - 4),min(rows,row+5)))
    rowRange.remove(row)
    nRow = random.choice(rowRange)
    colRange = list(range(max(0,col-4),min(cols,col+5)))
    colRange.remove(col)
    nCol = random.choice(colRange)

    if stations[nRow][nCol] != None:

        start = stations[row][col]
        target = stations[nRow][nCol]
        newRoad = Road(start,target,random.sample(list(randCOLORSET),1)[0],rows*cols)
        if not newRoad.invalid(roads):

            start.connectDots(target)
            roads.add(newRoad)

# stations,roads = generateMap(30,1024,700,200,70)
# def Assert(f):
#     if not f:
#         raise(AssertionError)
# Assert(stations == decodeStation(encodeStation(stations)))
# print(stations)
# print(decodeStation(encodeStation(stations)))

            