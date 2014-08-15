#

# 3rd party imports
import pygame

# Local imports
import monster

# Globals
FILE_PATH = 'resources\player.png'


class Player(object):
    #
    #
    def __init__(self):
        self.name = 'player'
        self.all_monsters = []
        self.x = 400
        self.y = 400
        self.size = (32, 32)
        self.size_multiplier = 1.50
        self.frame_index = 0
        self.speed = 16.0
        self.image = pygame.image.load(FILE_PATH)
        self.rect = self.image.get_rect()
        self.setup()

    def setup(self):
        self.all_monsters.append(monster.Monster('George', 'player', level=14))
        self.monsters_in_party = self.all_monsters

    def get_active_monster(self):
        return self.monsters_in_party[0]

    def move(self, direction, multi):
        if multi:
            speed = self.speed * 0.72
            self.x += (speed * direction[0])
            self.y += (speed * direction[1])
        else:
            self.x += (self.speed * direction[0])
            self.y += (self.speed * direction[1])

    def update(self):
        self.rect.topleft = (self.x, self.y)
