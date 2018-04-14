import pygame
from const import *
def drawStations(screen, stations):    
    for row in range(len(stations)):
        for col in range(len(stations[0])):
            if stations[row][col] != None:
                stations[row][col].draw(screen)

def drawRoads(screen,roads):
    for road in roads:
            road.draw(screen)

