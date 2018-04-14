import pygame
class Block(pygame.sprite.Sprite):
    def __init__(self, color, length):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.state = "inactive"

    def draw(self, x0, y0,x1,y1, color, screen):
        pass




