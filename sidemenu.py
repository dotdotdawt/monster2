import pygame

import text

SCREEN_SIZE = (800, 600) # MAKE SURE THIS IS RIGHT
RIGHT_SIDE_OFFSET = 125
TEXT_EDGE_BUFFER = 10 # Distance between where the menu background starts and text starts
BASE_X_LOCATION = SCREEN_SIZE[0]-RIGHT_SIDE_OFFSET
BASE_Y_LOCATION = 50
X_LOCATION_INCREASE = 50
Y_LOCATION_INCREASE = 24
X_COLUMN = 0
Y_ROW = 0
TEXT_TYPES = ['name', 'hp', 'level', 'next_xp', 'curr_xp', 'atk', 'def', 'speed']
LOCATIONS = {}

#for text_type in TEXT_TYPES:
#    new_x = BASE_X_LOCATION + (X_LOCATION_INCREASE * X_COLUMN)
#    new_y = BASE_Y_LOCATION + (Y_LOCATION_INCREASE * Y_ROW)
#    LOCATIONS[text_type] = (new_x, new_y)

for i in range(0, len(TEXT_TYPES)):
    x = BASE_X_LOCATION
    y = 50 + (24 * i)
    LOCATIONS[TEXT_TYPES[i]] = (x, y)

TEXT_SIZE = 18
TEXT_COLOR = (10, 20, 100)
TEXT_BG = (15, 100, 150) # Alpha

class SideMenu(object):
    #
    #
    def __init__(self):
        self.setup_background()
        self.setup_text()

    def setup_text(self):
        self.text_objects = {}
        for text_type in TEXT_TYPES:
            self.text_objects[text_type] = text.Text(
                text_type, LOCATIONS[text_type], TEXT_SIZE, TEXT_COLOR, TEXT_BG)

    def setup_background(self):
        self.bg_img = pygame.surface.Surface((RIGHT_SIDE_OFFSET+TEXT_EDGE_BUFFER, SCREEN_SIZE[1]))
        self.bg_rect = self.bg_img.get_rect()
        self.bg_rect.topleft = (BASE_X_LOCATION-TEXT_EDGE_BUFFER, 0)
        self.bg_img.fill(TEXT_BG)

    def update_text(self, monster):
        # This is called from game and the side menu is updated with a specific
        # monster from the player's party
        self.text_objects['name'].string = str(monster.name)
        self.text_objects['hp'].string = ' %i/%i ' % (monster.hp, monster.base_hp)
        self.text_objects['level'].string = str(monster.level)
        self.text_objects['next_xp'].string = str(0)
        self.text_objects['curr_xp'].string = str(0)
        self.text_objects['atk'].string = str(2)
        self.text_objects['def'].string = str(1)
        self.text_objects['speed'].string = str(monster.speed)

    def update(self, monster):
        self.update_text(monster)
