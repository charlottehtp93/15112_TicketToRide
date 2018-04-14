import pygame
import random
import copy
import numpy
from station import Station
from road import Road
from draw import *
from const import *
class Task(pygame.sprite.Sprite):
    def __init__(self,stations,index,adjMat,number):
        self.number = number
        (self.end1r,self.end1c) = getStation(stations)
        while 1:
            (self.end2r,self.end2c) = getStation(stations)
            if (self.end1r, self.end1c) != (self.end2r,self.end2c):
                break
        self.path = shortestPath(stations,
            stations[self.end1r][self.end1c],stations[self.end2r][self.end2c])
        self.degree = findDegree(index[(stations[self.end1r][self.end1c].x,stations[self.end1r][self.end1c].y)],
            index[(stations[self.end2r][self.end2c].x,stations[self.end2r][self.end2c].y)],adjMat)
        self.score = self.path+self.degree

    def __repr__(self):
        return "(%d,%d)"%(self.end1r,self.end1c)

    def draw(self,screen, stations, roads, background, x, y,width,height):
        rows, cols = len(stations), len(stations[0])
        sStations = [[None]*cols for row in range(rows)]
        for row in range(rows):
            for col in range(cols):
                sStations[row][col] = copy.copy(stations[row][col])
        sStations[self.end1r][self.end1c].color = dRED
        sStations[self.end2r][self.end2c].color = dRED
        sStations[self.end1r][self.end1c].size = 20
        sStations[self.end2r][self.end2c].size = 20
        sRoads = set()
        for road in roads:
            sRoads.add(copy.copy(road))
        for road in sRoads:
            road.color = BLACK
        self.image = pygame.Surface((screen.get_width(), screen.get_height()),flags = 0, depth = 32)
        #self.image.convert()
        self.image.blit(background, (0, 0))
        drawStations(self.image, sStations)
        drawRoads(self.image, sRoads)
        scorefont = pygame.font.SysFont("times", 128)
        score = scorefont.render(str(self.score),1,dBLACK)
        self.image.blit(score, (900,450))
        self.image = pygame.transform.smoothscale(self.image, (width,height))
        self.rect = screen.blit(self.image, (x,y))

def findDegree(ind1,ind2,adjMat):
    multMat = copy.deepcopy(adjMat)
    degree = 0
    while multMat[ind1][ind2] == 0:
        multMat = numpy.dot(multMat,adjMat)
        degree += 1
    return degree

def shortestPath(stations,start,end):
    def extractMin():
        leastDist = 500
        leastV = None
        for v in Q:
            if D[v] <= leastDist:
                leastDist = D[v]
                leastV = v
        Q.remove(leastV)
        return leastV

    D = dict() #shortest path dictionary
    S = set()
    Q = set(D)
    rows = len(stations)
    cols = len(stations[0])
    for row in range(rows):
        for col in range(cols):
            if stations[row][col]!= None:
                v = stations[row][col]
                D[v] = 200
                Q.add(v)
                #P[v] = None
    D[start] = 0
    while Q != set():
        u = extractMin()
        if u == end: break
        S.add(u)
        for v in u.conStation:
            if D[v] > D[u] + u.conStation[v]:
                D[v] = D[u] + u.conStation[v]
                #P[v] = u
    return D[end]

def getStation(stations):
    rows = len(stations)
    cols = len(stations[0])
    row,col = random.randint(0,rows-1), random.randint(0,cols-1)
    while stations[row][col] == None:
        row,col = random.randint(0,rows-1), random.randint(0,cols-1)
    return (row, col)



    #def __eq__(self,other):
    #    return (isinstance(other,Task) and 
    #        {(self.end1r,self.end1c),(self.end2r,self.end2c)} 
    #        == {(other.end1r,other.end1c),(other.end2r,other.end2c)})
    #def __hash__(self):
    #    return hash(((self.end1r,self.end1c),(self.end2r,self.end2c)))
