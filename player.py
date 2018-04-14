import random
import pygame
import copy
import numpy
from const import *
from block import Block 
from tickets import Ticket
from road import Road
from station import Station
from task import Task
from pygame.locals import *
from Map import *
from draw import *
class pubPlayer(object):
    def __init__(self,name,color):
        self.name = name
        self.color = color
        self.score = 0
        self.ticketNum = 4
    def __repr__(self):
        return self.name

    def drawScoreBoard(self,data,screen,number):
        scoreBoard = pygame.Surface((data.ticketWidth,data.ticketHeight))
        scoreBoard.fill(self.color)
        name = data.font.render(self.name,1,BACK)
        scoreBoard.blit(name,(20,0))
        ticketNum = data.sfont.render("Ticket: "+str(self.ticketNum),1,BACK)
        score = data.lfont.render(str(self.score),1,BACK)
        scoreBoard.blit(ticketNum,(5,20))
        scoreBoard.blit(score,(data.ticketWidth/2,data.ticketHeight/2))
        screen.blit(scoreBoard,(0,number*data.ticketHeight))
        
class Player(object):
    def __init__(self,data,name,color):
        self.name = name
        self.color = color
        self.stations = data.stations
        self.hTickets = {Ticket(BLACK):0,Ticket(BLUE):0,Ticket(BROWN):0,
        Ticket(GREEN):0,Ticket(PURPLE):0,Ticket(RED):0,Ticket(WHITE):0,Ticket(YELLOW):0}
        self.preholdTicket(data)

        self.aTasks = set()
        for i in range(6):
            self.aTasks.add(Task(data.stations,data.index,data.adjMat,i))
        self.hTasks = set()

        self.adjMat = adjacentMat(self,data)

        self.ticketForClaim = None
        self.claimRoad = None

        self.score = 0
        self.phase = '1'
    def __repr__(self):
        return self.name

    def preholdTicket(self,data):
        for i in range(4):
            length = len(data.tickets)
            aTicket = data.tickets.pop(random.randint(0,length-1))
            self.hTickets[aTicket] += 1
        self.ticketNum = 4

    def drawATask(self,data,screen):
        for task in self.aTasks:
            task.draw(screen,data.stations,data.roads,data.background,
                data.width-data.ticketWidth,task.number*data.ticketHeight,
                data.ticketWidth,data.ticketHeight)

    def pickTask(self,data,event):
        position = pygame.mouse.get_pos()
        for task in self.aTasks:
            if task.rect.collidepoint(position):
                self.hTasks.add(task)
                data.stations[task.end1r][task.end1c].color = self.color
                data.stations[task.end2r][task.end2c].color = self.color
                self.aTasks.remove(task)
                return task
    def drawHTask(self,data,screen):
        for task in self.hTasks:
            task.draw(screen,data.stations,data.roads,data.background,
                data.width-data.ticketWidth,data.height-data.ticketHeight,
                data.ticketWidth,data.ticketHeight)


    def pickATicket(self,data,event):
        position = pygame.mouse.get_pos()
        for ticket in data.aTickets:
            if ticket.rect.collidepoint(position):
                buyTicket(ticket,self,data)
                return True
        return False

    def pickHTicket(self,data,event):
        position = pygame.mouse.get_pos()
        for ticket in self.hTickets:
            if (self.hTickets[ticket] >0 and ticket.rect.collidepoint(position)):
                self.ticketForClaim = ticket
                return True
        return False

    def drawHTicket(self,data,screen):
        i = 0
        for ticket in self.hTickets:
            if self.hTickets[ticket] != 0:
                ticket.display(screen,data.ticketWidth*i,data.height-data.ticketHeight)
                label = data.font.render("%d"%self.hTickets[ticket],1,WHITE)
                pygame.draw.circle(screen, BLUE, (data.ticketWidth*i+8,data.height-data.ticketHeight+10), 12)
                screen.blit(label,(data.ticketWidth*i,data.height-data.ticketHeight))
                i += 1

    def validRoad(self,data,event):
        position = pygame.mouse.get_pos()
        ticket = self.ticketForClaim
        for road in data.roads:
            if road.rect.collidepoint(position):
                self.claimRoad = road
                if (not road.activate and road.color == ticket.color 
                    and self.hTickets[ticket] >= road.length):
                    road.lordcolor = self.color
                    road.activate = True
                    self.hTickets[ticket]-=road.length
                    self.ticketNum -= road.length
                    self.score += road.score
                    for i in range(road.length):
                        data.tickets.append(copy.copy(ticket))
                    if data.player1.name == self.name:
                        data.player1.ticketNum = self.ticketNum
                        data.player1.score = self.score
                    else:
                        data.player2.ticketNum = self.ticketNum
                        data.player2.score = self.score
                    return True
        return False
    def anyTaskCompleted(self,data):
        self.adjMat = adjacentMat(self,data)
        for task in self.hTasks:
            x1,y1 = data.stations[task.end1r][task.end1c].x,data.stations[task.end1r][task.end1c].y
            x2,y2 = data.stations[task.end2r][task.end2c].x,data.stations[task.end2r][task.end2c].y
            if isConnected(data.index[(x1,y1)],data.index[(x2,y2)],self.adjMat):
                self.score += task.score
                if data.player1.name == self.name:
                        data.player1.ticketNum = self.ticketNum
                        data.player1.score = self.score
                else:
                        data.player2.ticketNum = self.ticketNum
                        data.player2.score = self.score
                self.hTasks.remove(task)
                print(task)
                return
    
def adjacentMat(player,data):
    length = len(data.index)
    adjMat=[[0]*length for row in range(length)]
    for road in data.roads:
        if road.lordcolor == player.color:
            adjMat[data.index[road.end1]][data.index[road.end2]] = 1
            adjMat[data.index[road.end2]][data.index[road.end1]] = 1
    return adjMat

def isConnected(ind1,ind2,adjMat):
    multMat = copy.deepcopy(adjMat)
    for degree in range(100):
        multMat = numpy.dot(multMat,adjMat)
        if multMat[ind1][ind2] == 1:
            return True
    return False

def buyTicket(ticket,player,data):
    data.aTickets.remove(ticket)
    player.hTickets[ticket] += 1
    player.ticketNum += 1
    addTicket = random.sample(data.tickets,1)
    data.aTickets += addTicket
    if data.player1.name == player.name:
        data.player1.ticketNum = player.ticketNum
    else:
        data.player2.ticketNum = player.ticketNum


