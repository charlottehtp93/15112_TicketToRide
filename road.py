import pygame
import random
import math
from station import Station
from const import *
class Road(pygame.sprite.Sprite):
    def __init__(self, station1, station2,color,size):
        pygame.sprite.Sprite.__init__(self)
        self.end1 = (station1.x,station1.y)
        self.end2 = (station2.x,station2.y)
        self.color = color
        self.lordcolor = None
        #calculate least number of blocks 
        self.length = int(math.hypot(self.end1[0]-self.end2[0],self.end1[1]-self.end2[1])//(2000//size)+1)
        self.score = int(self.length**1.5)
        #self.length = random.randint(leastLength, int(1.2*leastLength))
        self.activate = False

    def __repr__(self):
        return COLORSET[self.color]+ " of "+str(self.end1) +"+"+ str(self.end2)+str(self.activate)
        #return str(self.end1) +"+"+ str(self.end2)
        #return "(%d, %d),(%d,%d)" %(self.end1[0],self.end1[1],self.end2[0],self.end2[1])

    def __eq__(self,other):
        if isinstance(other, Road):
            return {self.end1,self.end2} == {other.end1, other.end2}

    def __hash__(self):
        return hash((self.end1,self.end2))

    def invalid(self, roads):
        for other in roads:
            if self == other:
                return True
            if shareStation(other, self):
                #print(other,self)
                if littleAngle(other,self):
                    return True
            elif isCross(other.end1,other.end2,self.end1,self.end2):
                return True
        return False

    def draw(self, screen):
        self.rect = pygame.draw.line(screen,dRED,(self.end1[0],self.end1[1]),
                (self.end2[0],self.end2[1]),2)
        if self.activate == False:
            drawBrick(screen, self.rect,self.color, GREY, self.end1[0],self.end1[1], 
                self.end2[0],self.end2[1], self.length,7)
        else:
            drawBrick(screen, self.rect,self.lordcolor, dBLACK, self.end1[0],self.end1[1], 
                self.end2[0],self.end2[1], self.length,12)

def drawBrick(screen, rect, fill,line,x1,y1,x2,y2,number,height):
    ratio = 0.2
    length = math.hypot(x2-x1,y2-y1)
    if length == 0:
        return
    slength = length/(number+(number+1)*ratio)
    Blocks = pygame.Surface((int(length),height))
    Blocks.fill(WHITE)
    Blocks.set_colorkey(dBLACK)
    for i in range(number):
        rect = pygame.Rect(i*slength+(i+1)*slength*ratio,0,slength,height-1)
        pygame.draw.rect(Blocks,fill,rect)
        pygame.draw.lines(Blocks,line,True,
            [rect.topleft, rect.bottomleft, rect.bottomright, rect.topright],3)
    if (x2-x1)*(y2-y1)<0:
        if x2-x1 <0:
            x1,x2,y1,y2 = x2,x1,y2,y1
        angle = math.degrees(math.acos((x2-x1)/length))
        Blocks = pygame.transform.rotate(Blocks,angle)
        screen.blit(Blocks,(x1,y2))
    elif (x2-x1)*(y2-y1)>0:
        if x2-x1>0:
            x1,x2,y1,y2 = x2,x1,y2,y1
        angle = math.degrees(math.acos((x2-x1)/length))
        Blocks = pygame.transform.rotate(Blocks,angle)
        screen.blit(Blocks,(x2,y2))
    else:
        if x2==x1:
            angle = math.degrees(90)
            Blocks = pygame.transform.rotate(Blocks,angle)
            if y2>y1:
                screen.blit(Blocks,(x1,y1))
            else:
                screen.blit(Blocks,(x2,y2))
        else:
            angle = math.degrees(0)
            Blocks = pygame.transform.rotate(Blocks,angle)
            if x2>x1:
                screen.blit(Blocks,(x1,y1))
            else:
                screen.blit(Blocks,(x2,y2))

    

def shareStation(road1, road2):
    if (road1.end1 == road2.end1 or road1.end1 == road2.end2 
        or road1.end2 == road2.end1 or road1.end2 == road2.end2):
        return True

def littleAngle(roada, roadb):
    for enda in (roada.end1,roada.end2):
        for endb in (roadb.end1,roadb.end2):
            if enda == endb:
                vertex = enda
                side = list({roada.end1,roada.end2,roadb.end1,roadb.end2})
                side.remove(vertex)
                break
    if len(side) == 1:
        return False
    return abs(angle(vertex,side))<15

def angle(vertex,side):
    (x,y) = (vertex[0], vertex[1])
    (x0,y0) = (side[0][0],side[0][1])
    (x1,y1) = (side[1][0],side[1][1])
    cosine = ((x0-x)*(x1-x) + (y0-y)*(y1-y))/(math.hypot(x0-x,y0-y)*math.hypot(x1-x,y1-y))
    angle = math.degrees(math.acos(cosine))
    #print(angle)
    return angle


def mult(a, b, c): 
    return (a[0]-c[0])*(b[1]-c[1])-(b[0]-c[0])*(a[1]-c[1]) 

def isCross(a1,a2,b1,b2): 
    if max(a1[0], a2[0]) < min(b1[0], b2[0]):
        return False 
    if max(a1[1], a2[1]) < min(b1[1], b2[1]): 
        return False 
    if max(b1[0], b2[0]) < min(a1[0], a2[0]):
        return False 
    if max(b1[1], b2[1]) < min(a1[1], a2[1]): 
        return False
    if mult(b1, a2, a1)*mult(a2,b2, a1)<0:
        return False
    if mult(a1, b2, b1)*mult(b2, a2, b1)<0:
        return False  
    return True  


