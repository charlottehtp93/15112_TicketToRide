from station import Station
def encodeStation(stations):
    pdStations = dict()
    rows = len(stations)
    cols = len(stations[0])
    pdStations['size'] = (rows,cols)
    for row in range(rows):
        for col in range(cols):
            if stations[row][col] == None:
                pdStations[(row,col)] = None
            else:
                station = stations[row][col]
                lst = [station.x,station.y,station.number,station.row,station.col,station.color,station.size]
                for other in station.conStation:
                    lst.append((other.row,other.col))
                pdStations[(row,col)] = tuple(lst)
    return pdStations

def decodeStation(pdStations):
    rows,cols = pdStations['size']
    stations = [[0]*cols for row in range(rows)]
    for index in pdStations:
        if index == 'size':continue
        (row,col) = index
        if pdStations[(row,col)] == None:
            stations[row][col] = None
            continue
        content = pdStations[(row,col)]
        station = Station(content[0],content[1],content[2],content[3],content[4])
        station.color = content[5]
        station.size = content[6]
        stations[row][col] = station
    for index in pdStations:
        if index == 'size':continue
        (row,col) = index
        if pdStations[(row,col)] == None:
            continue
        connections = pdStations[(row,col)][7:]
        for connection in connections:
            (nrow,ncol) = connection
            stations[row][col].connectDots(stations[nrow][ncol])
    return stations




