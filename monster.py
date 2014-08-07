import pygame

FILE_PATH_X = 'resources\monster1.png'
FILE_PATH_Y = 'resources\monster2.png'

class Monster(object):
    #
    #
    def __init__(self, name, location):
        self.name = name
        self.x, self.y = location
        self.setup_defaults()
        self.setup_image()

    def setup_defaults(self):
        self.level = 5
        self.base_hp = 10
        self.hp = 10
        self.atk = 1
        self.speed = 10

    def setup_image(self):
        self.image = pygame.image.load(FILE_PATH_X)
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        self.rect.topleft = (self.x, self.y)
