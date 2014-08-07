#

# 3rd party imports
import pygame

# Local imports
import text
import monster

# Globals
X_NAME_LOCATION = (600, 400)
X_HP_LOCATION = (600, 450)
X_SPRITE_LOCATION = (650, 425)

Y_NAME_LOCATION = (50, 50)
Y_HP_LOCATION = (50, 100)
Y_SPRITE_LOCATION = (100, 75)

NAME_SIZE = 20
HP_SIZE = 16
NAME_COLOR = (200, 200, 100)
NAME_BG_COLOR = (0, 0, 0)
HP_COLOR = (0, 200, 50)
HP_BG_COLOR = (0, 0, 0)

MESSAGE_LOCATION = (200, 500)
MESSAGE_SIZE = 16
MESSAGE_COLOR = (200, 200, 200)
MESSAGE_BG_COLOR = (20, 20, 20)

STATES = [
    'init', 'x_action', 'x_attacking', 'y_action', 'y_attacking', 'end'
    ]

class Battle(object):
    #
    #
    def __init__(self):
        self.state = 'init'
        self.setup_monsters()
        self.setup_text()

    def setup_monsters(self):
        self.monster_x = monster.Monster('George', X_SPRITE_LOCATION)
        self.monster_y = monster.Monster('Bob', Y_SPRITE_LOCATION, level=11)
        self.monsters = [self.monster_x, self.monster_y]

    def setup_text(self):
        self.x_name_text = text.Text(
            'name', X_NAME_LOCATION, NAME_SIZE, NAME_COLOR, NAME_BG_COLOR, xy='x')
        self.y_name_text = text.Text(
            'name', Y_NAME_LOCATION, NAME_SIZE, NAME_COLOR, NAME_BG_COLOR, xy='y')
        self.x_hp_text = text.Text(
            'hp', X_HP_LOCATION, HP_SIZE, HP_COLOR, HP_BG_COLOR, xy='x')
        self.y_hp_text = text.Text(
            'hp', Y_HP_LOCATION, HP_SIZE, HP_COLOR, HP_BG_COLOR, xy='y')
        self.message_text = text.Text(
            'battle_message', MESSAGE_LOCATION, MESSAGE_SIZE, MESSAGE_COLOR, MESSAGE_BG_COLOR)
        self.text_objects = [
            self.x_name_text, self.y_name_text, self.x_hp_text, self.y_hp_text, self.message_text
            ]

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
                return  ' %i/%i ' % (self.monster_x.hp, self.monster_x.base_hp)
            elif text_object.xy == 'y':
                return ' %i/%i ' % (self.monster_y.hp, self.monster_y.base_hp)
        # Battle messages to user
        elif text_object.type == 'battle_message':
            if self.state == 'init':
                return 'The battle has begun. Press Q to continue.'
            elif self.state == 'x_action':
                return 'it is %s\'s turn, please give an action.' % self.monster_x.name
            elif self.state == 'x_attacking':
                return '%s dealt 1 damage. Press Q to continue.' % self.monster_x.name
            else:
                return 'Not completed'

    def deal_damage(self, user, target):
        target.hp -= 1

    def decide_turn(self):
        self.next_turn = 'Bob'

    def is_battle_over(self):
        if self.monster_y.hp <= 0.5:
            return True
        else:
            return False

    def accept(self):
        if self.state == 'init':
            self.state = 'x_action'
        elif self.state == 'x_action':
            self.state = 'x_attacking'
            self.deal_damage(self.monster_x, self.monster_y)
        elif self.state == 'x_attacking':
            if self.is_battle_over():
                self.state = 'end'
            else:
                self.state = 'x_action'

    def decline(self):
        self.state = 'end'


                    
