import random
import string
import pygame
import copy
import numpy
import socket
import pickle
import json
from const import *
from block import Block 
from tickets import Ticket
from road import Road
from station import Station
from task import Task
from player import Player
from player import pubPlayer
from pygame.locals import *
from Map import *
from draw import *
from encodeStation import *
from multiprocessing.connection import Client
###################################
#References:
#maze solving: http://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
#pygame documentation: https://www.pygame.org/docs/
###################################
def preInit(data):
    data.font = pygame.font.SysFont("arial", 32)
    data.sfont = pygame.font.SysFont("monospace", 20)
    data.lfont = pygame.font.SysFont("monospace", 48)
    data.background = pygame.image.load('cartoontrain3.jpg')
    #data.background = pygame.image.load('cartoontrain3.jpg').convert()
    data.background = pygame.transform.smoothscale(data.background, 
        (data.width,data.height))
    data.stationNum = 0
    data.roads = set()
    data.stations = list()
    data.aTickets = list()
#available tickets
    data.tickets = loadTickets()#list
    data.ticketWidth, data.ticketHeight = data.tickets[0].width, data.tickets[0].height
#available tasks
    data.phase = '0'
    data.done = False
    data.gameOver = False
    data.currPlayer = 1
    data.winner = None
    data.player1,data.player2 = pubPlayer("Andrew",dRED),pubPlayer("David",dGREEN)

def adjacentMat(data):
    data.index = dict()
    rows = len(data.stations)
    cols = len(data.stations[0])
    i = 0
    for row in range(rows):
        for col in range(cols):
            if data.stations[row][col] != None:
                data.index[(data.stations[row][col].x,data.stations[row][col].y)] = i
                i += 1
    data.adjMat=[[0]*i for row in range(i)]
    for road in data.roads:
        data.adjMat[data.index[road.end1]][data.index[road.end2]] = 1
        data.adjMat[data.index[road.end2]][data.index[road.end1]] = 1

def loadTickets():
    ticketColors = [BLACK,BLUE,BROWN,GREEN,PURPLE,RED,WHITE,YELLOW]
    tickets = []
    for i in range(10):
        for color in ticketColors:
            tickets.append(Ticket(color))
    return tickets    

def drawATicket(data,screen):#available tickets
    for i in range(len(data.aTickets)):
        ticket = data.aTickets[i] 
        ticket.display(screen,data.width-ticket.width,i*ticket.height)
        
def drawTitle(screen,data):
    title = pygame.image.load("TITLE.jpg")
    #title = pygame.image.load("TITLE.jpg").convert()
    title = pygame.transform.smoothscale(title,(260,35))
    screen.blit(title,(data.width/2-130,10))

def drawHintTask(screen,data):
    hint = data.font.render("Please select a task on the right",1,dBLACK)
    screen.blit(hint,(data.width/2-150,data.height-110))

def drawHintMove(screen,data):
    hint = data.font.render("Pick two tickets on the right or claim a railway",1,dBLACK)
    screen.blit(hint,(data.width/2-250,data.height-110))

def drawScoreBoard(data,screen):
    data.player1.drawScoreBoard(data,screen,0)
    data.player2.drawScoreBoard(data,screen,1)

def initDownload():
    global data
    global sock
    dataPack = sock.recv()
    (data.roads,pdStations,data.stationNum, data.aTickets,data.player1,data.currPlayer,data.index,data.adjMat) = dataPack
    data.stations = decodeStation(pdStations)

def download():
    global sock
    dataPack = sock.recv()
    (data.roads,data.aTickets,data.player1,data.currPlayer) = dataPack
        
def upload():
    global sock
    dataPack = (data.roads,data.aTickets,data.player2,data.currPlayer)
    sock.send(dataPack)


class struct(object):
    pass
data = struct()
data.width, data.height = 1024,600

HOST = '128.2.54.137'
sock = Client((HOST,2525))
sock.send("here")
print("downloading")

def run():
    def redrawSelf1(player):
        player.drawHTicket(data,screen)
        player.drawATask(data,screen)
        player.drawHTask(data,screen)
        pygame.display.flip()
    def redrawSelf2(player):
        player.drawHTask(data,screen)
        player.drawHTicket(data,screen)        
        pygame.display.flip()
    def redrawShare0():
        screen.fill(WHITE)
        notice = data.lfont.render("Waiting...",1,dBLACK)
        screen.blit(notice,(data.width/2-150,data.height//2))
        pygame.display.flip()
    def redrawShare1():
        screen.blit(data.background, (0, 0))
        drawRoads(screen,data.roads)
        drawStations(screen,data.stations)
        drawTitle(screen,data)
        drawHintTask(screen,data)
        drawScoreBoard(data,screen)
        pygame.display.flip()
    def redrawShare2():
        screen.blit(data.background, (0, 0))
        drawRoads(screen,data.roads)
        drawStations(screen,data.stations)
        drawATicket(data,screen)
        drawTitle(screen,data)
        drawHintMove(screen,data)
        drawScoreBoard(data,screen)
        pygame.display.flip()
    def redrawOver():
        screen.blit(data.background, (0, 0))
        drawTitle(screen,data)
        drawScoreBoard(data,screen)
        winnerNotice = data.lfont.render("%s Wins!"%data.winner,1,dBLACK)
        Action = data.lfont.render("Press ENTER to start new game",1,dBLACK)
        screen.blit(winnerNotice,(data.width/2-150,data.height//2))
        screen.blit(Action,(data.width/2-150,data.height//2+50))
        pygame.display.flip()
    def isOver():
        for road in data.roads:
            if road.activate == False:
                return False
        return True

    pygame.init()
    clock = pygame.time.Clock()
    global data
    screen = pygame.display.set_mode((data.width,data.height))
    preInit(data)

    while not data.done:
        clock.tick(10)  
        if data.phase == '0':
            redrawShare0()
            preInit(data)
            initDownload()
            data.phase = '1'
            player2 = Player(data,"David",dGREEN)
            redrawShare1()
            redrawSelf1(player2)

        if data.currPlayer == 1:
            if not (player2.phase == '1' or player2.phase == '0'):
                download()
                redrawShare2();redrawSelf2(player2)

        for event in pygame.event.get():
            if event.type == QUIT:
                data.done = True
                break
            if event.type == MOUSEBUTTONDOWN:
                if player2.phase == '1':
                    currTask = player2.pickTask(data,event)
                    if currTask != None:
                        redrawShare1();redrawSelf1(player2)
                    if len(player2.hTasks)>=2:
                        player2.phase = '2'
                        redrawShare2();redrawSelf2(player2)
                elif player2.phase == '2':#decide whether to buy or to spend ticket
                    if data.currPlayer == 2:
                        if player2.pickATicket(data,event):
                            player2.phase = "2-2" 
                        elif player2.pickHTicket(data,event):
                            player2.phase = '2-1'
                        upload()
                        redrawShare2();redrawSelf2(player2)
                elif player2.phase == '2-1':#one holding ticket has been selected
                    if data.currPlayer == 2:
                        if player2.pickATicket(data,event):
                            player2.phase = "2-2"
                            player2.ticketForClaim = None
                        elif player2.validRoad(data,event):
                            player2.ticketForClaim = None
                            player2.anyTaskCompleted(data)
                            if player2.hTasks == set():
                                redrawShare1();redrawSelf1(player2)
                                player2.phase = '1'
                                continue
                            else:
                                player2.phase = '2'
                                data.currPlayer = 1
                        else:
                            if player2.claimRoad != None: 
                                player2.phase = '2-1' 
                        player2.claimRoad = None
                        upload()
                        redrawShare2();redrawSelf2(player2)
                    
                elif player2.phase == "2-2":#one available ticket has been selected
                    if data.currPlayer == 2:
                        if player2.pickATicket(data,event):
                            player2.phase = '2'
                            data.currPlayer = 1
                        upload()
                        redrawShare2();redrawSelf2(player2)

        data.gameOver = isOver()
        if data.gameOver == True:
            print("over")
            if data.player1.score > data.player2.score:
                data.winner = data.player1.name
            else:
                data.winner = data.player2.name
            data.currPlayer = None
            redrawOver()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        data.phase = '0'
                        continue

    sock.close()
    pygame.quit()

run()














