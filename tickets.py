import pygame
import os
from const import *
class Ticket(pygame.sprite.Sprite):
    def __init__(self,color,scale=0.25):
        self.color = color
        image = pygame.image.load(COLORSET[self.color]+".jpg")
        (width,height) = pygame.Surface.get_size(image)
        self.width, self.height = int(width*scale), int(height*scale)
        

    def __repr__(self):
        return COLORSET[self.color]

    def display(self,screen,x,y,scale=0.3):
        image = pygame.image.load(COLORSET[self.color]+".jpg")
        image = pygame.transform.smoothscale(image, (self.width,self.height))
        #image.convert()
        self.rect = screen.blit(image, (x,y))

    def __hash__(self):
        return hash(self.color)
    def __eq__(self,other):
        return (isinstance(other,Ticket) and self.color == other.color)

 



