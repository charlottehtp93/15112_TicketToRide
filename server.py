import random
import string
import pygame
import copy
import numpy
import socket
import pickle
from const import *
from block import Block 
from tickets import Ticket
from road import Road 
from station import Station
from task import Task
from player import Player
from player import pubPlayer
from pygame.locals import *
from multiprocessing.connection import Listener
from Map import *
from draw import *
###################################
#References:
#maze solving: http://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
#pygame documentation: https://www.pygame.org/docs/
###################################

def preInit(data):
    data.font = pygame.font.SysFont("arial", 28)
    data.sfont = pygame.font.SysFont("arial", 18)
    data.lfont = pygame.font.SysFont("arial", 42)
    data.background = pygame.image.load('cartoontrain3.jpg')
    data.background = pygame.transform.smoothscale(data.background, 
        (data.width,data.height))
#available tickets
    data.tickets = loadTickets()#list
    data.ticketWidth, data.ticketHeight = data.tickets[0].width, data.tickets[0].height
    data.aTickets = list()
    for i in range(5):
        availableTicket(data)
#available tasks
    data.done = False
    data.currPlayer = 1
    data.player1,data.player2 = pubPlayer("Andrew",RED),pubPlayer("David",GREEN)
    data.phase = '0'
    data.stationNum = None

def realInit(data):
    #map
    data.stations,data.roads = generateMap(data.stationNum,data.width,
        data.height,data.ticketWidth,data.ticketHeight)
    adjacentMat(data)
    initUpload()

def loadTickets():
    ticketColors = [BLACK,BLUE,BROWN,GREEN,PURPLE,RED,WHITE,YELLOW]
    tickets = []
    for i in range(10):
        for color in ticketColors:
            tickets.append(Ticket(color))
    return tickets

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


def availableTicket(data):
    length = len(data.tickets)
    data.aTickets.append(data.tickets.pop(random.randint(0,length-1)))
    
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
    
def download():
    global conn
    dataPack = conn.recv()
    (data.roads,data.aTickets,data.player2,data.currPlayer) = dataPack
        
def initUpload():
    global conn
    pdStations = encodeStation(data.stations)
    dataPack = (data.roads,pdStations,data.stationNum, data.aTickets,data.player1,data.currPlayer,data.index,data.adjMat)
    conn.send(dataPack)
def upload():
    global conn
    dataPack = (data.roads,data.aTickets,data.player1,data.currPlayer)
    conn.send(dataPack)

class struct(object):
    pass
data = struct()
data.width, data.height = 1024,600
    
HOST = socket.gethostbyname(socket.gethostname())
PORT = 2525
sock = Listener((HOST,PORT))
conn = sock.accept()
print(conn.recv())
print("loading")

def run():
    def getNumber():
        pygame.font.init()
        currString = []
        drawQuestion(currString)
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    inkey = event.key
                    if inkey == K_BACKSPACE:
                        currString = currString[0:-1]
                    elif inkey == K_RETURN:
                        return int("".join(currString))
                    elif inkey == K_MINUS:
                        currString.append("_")
                    elif inkey <= 127:
                        currString.append(chr(inkey))
            drawQuestion(currString)
    def drawQuestion(string):
        screen.fill(WHITE)
        question = data.lfont.render("Number of stations: " + "".join(string),1,dBLACK)
        screen.blit(question,(data.width/2-150,data.height//2))
        pygame.display.flip()
    
    def redrawSelf1(player):
        player.drawHTicket(data,screen)
        player.drawATask(data,screen)
        player.drawHTask(data,screen)
        pygame.display.flip()
    def redrawSelf2(player):
        player.drawHTask(data,screen)
        player.drawHTicket(data,screen)        
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


#track score
    while not data.done:
        clock.tick(10)
        #for player2
        if data.phase == '0':
            print("new game")
            preInit(data)
            data.stationNum = getNumber()
            print(data.stationNum)
            realInit(data)
            data.phase = '1'
            player1 = Player(data,"Andrew",dRED)
            redrawShare1()
            redrawSelf1(player1)
            
        if data.currPlayer == 2:
            if player1.phase == '1':continue
            else:
                download()
                redrawShare2();redrawSelf2(player1)
        for event in pygame.event.get():
            if event.type == QUIT:
                data.done = True
                break
            if event.type == MOUSEBUTTONDOWN:
                if player1.phase == '1':
                    if player1.pickTask(data,event) != None:
                        redrawShare1();redrawSelf1(player1)
                    if len(player1.hTasks)>=2:
                        player1.phase = '2'
                        redrawShare2();redrawSelf2(player1)
                elif player1.phase == '2':#decide whether to buy or to spend ticket
                    if data.currPlayer == 1:
                        if player1.pickATicket(data,event):
                            player1.phase = '2-2'
                        elif player1.pickHTicket(data,event):
                            player1.phase = '2-1'
                            
                        upload()
                        redrawShare2();redrawSelf2(player1)
                    
                elif player1.phase == '2-1':#one holding tickt has been selected
                    if data.currPlayer == 1:
                        if player1.pickATicket(data,event):
                            player1.phase = '2-2'
                            player1.ticketForClaim = None
                        elif player1.validRoad(data,event):
                            print(data.roads)
                            player1.phase = '2'
                            player1.ticketForClaim = None
                            data.currPlayer = '2'
                            player1.anyTaskCompleted(data)
                            print(player1.hTasks)
                            if player1.hTasks == set():
                                print("completed 2")
                                redrawShare1();redrawSelf1(player1)
                                player1.phase = '1'
                                continue
                            else:
                                player1.phase = '2'
                                data.currPlayer = 2
                        else:
                        #elif not player1.validRoad(data,event):
                            if player1.claimRoad != None: 
                                player1.phase = '2-1'        
                        player1.claimRoad = None
                        
                        upload()
                        redrawShare2();redrawSelf2(player1)
                    
                elif player1.phase == '2-2':#one available ticket has been selected
                    if data.currPlayer == 1:
                        if player1.pickATicket(data,event):
                            player1.phase = '2'
                            data.currPlayer = 2
                        
                        upload()
                        redrawShare2();redrawSelf2(player1)

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
    conn.close()
    pygame.quit()

run()














