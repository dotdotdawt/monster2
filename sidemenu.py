import pygame

import text

SCREEN_SIZE = (800, 600) # MAKE SURE THIS IS RIGHT
RIGHT_SIDE_OFFSET = 175
TEXT_EDGE_BUFFER = 8 # Distance between where the menu background starts and text starts
MENU_BOTTOM_BUFFER = 300 # How far from bottom of screen menu hangs
MENU_CUTOFF = (24, 24)
BASE_X_LOCATION = SCREEN_SIZE[0]-RIGHT_SIDE_OFFSET
BASE_Y_LOCATION = 25
X_LOCATION_INCREASE = 50
Y_LOCATION_INCREASE = 16
X_COLUMN = 0
Y_ROW = 0
TEXT_TYPES = ['name', 'level', 'curr_xp', 'next_xp', 'hp', 'atk', 'def', 'speed']
IMPORTANT_TYPES = ['name']
LOCATIONS = {}

#for text_type in TEXT_TYPES:
#    new_x = BASE_X_LOCATION + (X_LOCATION_INCREASE * X_COLUMN)
#    new_y = BASE_Y_LOCATION + (Y_LOCATION_INCREASE * Y_ROW)
#    LOCATIONS[text_type] = (new_x, new_y)

for i in range(0, len(TEXT_TYPES)):
    x = BASE_X_LOCATION + MENU_CUTOFF[0]
    y = BASE_Y_LOCATION + MENU_CUTOFF[1] + (Y_LOCATION_INCREASE * i)
    if i == 0: # Hacking this
        y -= 16 # Seperate the name title from stats
        x += 14 # Center the name
    LOCATIONS[TEXT_TYPES[i]] = (x, y)

TEXT_SIZE_IMPORTANT = 24
TEXT_SIZE_NORMAL = 16
TEXT_COLOR_IMPORTANT = (180, 60, 60)
TEXT_COLOR_NORMAL = (10, 80, 200)
TEXT_BG = (60, 130, 160) # Alpha

class SideMenu(object):
    #
    #
    def __init__(self):
        self.setup_background()
        self.setup_text()

    def setup_text(self):
        self.text_objects = {}
        for text_type in TEXT_TYPES:
            if text_type in IMPORTANT_TYPES:
                self.text_objects[text_type] = text.Text(
                    text_type, LOCATIONS[text_type], TEXT_SIZE_IMPORTANT, TEXT_COLOR_IMPORTANT, TEXT_BG
                    )
            else:
                self.text_objects[text_type] = text.Text(
                    text_type, LOCATIONS[text_type], TEXT_SIZE_NORMAL, TEXT_COLOR_NORMAL, TEXT_BG
                )

    def setup_background(self):
        x_size = RIGHT_SIDE_OFFSET - TEXT_EDGE_BUFFER - MENU_CUTOFF[0]
        y_size = SCREEN_SIZE[1] - MENU_BOTTOM_BUFFER - MENU_CUTOFF[1]
        self.bg_img = pygame.surface.Surface((x_size, y_size))
        self.bg_rect = self.bg_img.get_rect()
        x_loc = BASE_X_LOCATION - TEXT_EDGE_BUFFER + MENU_CUTOFF[0]
        y_loc = MENU_CUTOFF[1]
        self.bg_rect.topleft = (x_loc, y_loc)
        self.bg_img.fill(TEXT_BG)

    def update_text(self, monster):
        # This is called from game and the side menu is updated with a specific
        # monster from the player's party
        self.text_objects['name'].string = str(monster.name)
        self.text_objects['hp'].string = ' HP: %i/%i ' % (monster.hp, monster.base_hp)
        self.text_objects['level'].string = ' Level: %i ' % monster.level
        self.text_objects['next_xp'].string = ' XP to next: %i ' % (monster.level-1)
        self.text_objects['curr_xp'].string = ' Current XP: %i ' % 2003
        self.text_objects['atk'].string = ' Attack: %i ' % monster.atk
        self.text_objects['def'].string = ' Defense: %i ' % 5
        self.text_objects['speed'].string = ' Speed: %i ' % monster.speed

    def update(self, monster):
        self.update_text(monster)
