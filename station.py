import pygame
import math
from const import *
class Station(pygame.sprite.Sprite):
    #create a station
    def __init__(self, locaX, locaY, number, row,col,color = BLACK, size = 10):
        pygame.sprite.Sprite.__init__(self)
        self.x = locaX
        #print(self.x)
        self.y = locaY
        self.number = number
        self.row = row
        self.col = col
        self.color = color
        self.size = size
        #connected station
        self.conStation = dict()
        

    def __repr__(self):
        #return "%d" %len(self.conStation)
        return "[(%d,%d),%s]"%(self.x,self.y,COLORSET[self.color])

    def __eq__(self,other):
        if isinstance(other,Station):
            return (self.x == other.x and self.y == other.y)

    def __hash__(self):
        return hash((self.x,self.y))

    def connectDots(self, other):
        distance = int(math.hypot(self.x-other.x,self.y-other.y)//60+1)
        self.conStation[other] = distance
        other.conStation[self] = distance

    #draw itself
    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)
              
    


