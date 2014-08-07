import pygame

FILE_PATH_X = 'resources\monster1.png'
FILE_PATH_Y = 'resources\monster2.png'

class Monster(object):
    #
    #
    def __init__(self, name, location, level=None):
        self.name = name
        self.x, self.y = location
        if level:
            self.level = level
        else:
            self.level = 5
        self.setup_defaults()
        self.setup_image()

    def setup_defaults(self):
        self.base_hp = self.level
        self.hp = self.base_hp
        self.atk = 1
        self.speed = 10

    def setup_image(self):
        self.image = pygame.image.load(FILE_PATH_X)
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        self.rect.topleft = (self.x, self.y)
