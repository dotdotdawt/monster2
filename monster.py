import pygame

FILE_PATH_U = 'resources\monster1.png'
FILE_PATH_X = 'resources\monster2.png'
ALLIED_LOCATION = (0,0)
ENEMY_LOCATION = (100, 100)

class Monster(object):
    #
    #
    def __init__(self, name, owner, level=None):
        self.name = name
        self.owner = owner
        self.x, self.y = (0, 0)
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
        if self.owner == 'player':
            self.x, self.y = ALLIED_LOCATION
        else:
            self.x, self.y = ENEMY_LOCATION
        self.rect.topleft = (self.x, self.y)


def set_sprite_anchor_points(new_allied_location, new_enemy_location):
    global ALLIED_LOCATION, ENEMY_LOCATION
    ALLIED_LOCATION = new_allied_location
    ENEMY_LOCATION = new_enemy_location
