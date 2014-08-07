#

# 3rd party imports
import pygame

# Local imports
import text
import monster

# Globals
X_NAME_LOCATION = (50, 50)
X_HP_LOCATION = (50, 100)
X_SPRITE_LOCATION = (100, 75)

Y_NAME_LOCATION = (600, 400)
Y_HP_LOCATION = (600, 450)
Y_SPRITE_LOCATION = (650, 425)

NAME_SIZE = 20
HP_SIZE = 16
NAME_COLOR = (200, 200, 100)
NAME_BG_COLOR = (0, 0, 0)
HP_COLOR = (0, 200, 50)
HP_BG_COLOR = (0, 0, 0)

class Battle(object):
    #
    #
    def __init__(self):
        self.setup_monsters()
        self.setup_text()

    def setup_monsters(self):
        self.monster_x = monster.Monster('George', X_SPRITE_LOCATION)
        self.monster_y = monster.Monster('Bob', Y_SPRITE_LOCATION)
        self.monsters = [self.monster_x, self.monster_y]

    def setup_text(self):
        self.x_name_text = text.Text('x', 'name', X_NAME_LOCATION, NAME_SIZE, NAME_COLOR, NAME_BG_COLOR)
        self.y_name_text = text.Text('x', 'name', Y_NAME_LOCATION, NAME_SIZE, NAME_COLOR, NAME_BG_COLOR)
        self.x_hp_text = text.Text('y', 'hp', X_HP_LOCATION, HP_SIZE, HP_COLOR, HP_BG_COLOR)
        self.y_hp_text = text.Text('y', 'hp', Y_HP_LOCATION, HP_SIZE, HP_COLOR, HP_BG_COLOR)
        self.text_objects = [self.x_name_text, self.y_name_text, self.x_hp_text, self.y_hp_text]

    def update_text_object(self, text_object):
        text_object.string = self.get_updated_string(text_object)
        text_object.update()
        text_object.image = text_object.font.render(
            text_object.string, text_object.anti_aliasing, text_object.color, text_object.bg_color)

    def get_updated_string(self, text_object):
        # Name strings
        if text_object.type == 'name':
            if text_object.xy == 'x':
                return ' %s ' % self.monster_x.name
            elif text_object.xy == 'y':
                return ' %s ' % self.monster_y.name
        # HP strings
        elif text_object.type == 'hp':
            if text_object.xy == 'x':
                return  ' %i/%i ' % (self.monster_x.base_hp, self.monster_x.hp)
            elif text_object.xy == 'y':
                return ' %i/%i ' % (self.monster_y.base_hp, self.monster_y.hp)
