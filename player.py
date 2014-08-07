#

# 3rd party imports
import pygame

# Globals
FILE_PATH = 'resources\player.png'


class Player(object):


    def __init__(self):
        self.name = 'player'
        self.units = []
        self.x = 400
        self.y = 400
        self.size = (32, 32)
        self.size_multiplier = 1.50
        self.frame_index = 0
        self.speed = 16.0
        self.image = pygame.image.load(FILE_PATH)
        self.rect = self.image.get_rect()

    def move(self, direction, multi):
        if multi == False:
            self.x += (self.speed * direction[0])
            self.y += (self.speed * direction[1])
        if multi == True:
            speed = self.speed * 0.72
            self.x += (speed * direction[0])
            self.y += (speed * direction[1])

    def update(self):
        self.rect.topleft = (self.x, self.y)
