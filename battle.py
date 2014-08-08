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

MESSAGE_LOCATION = (250, 500)
MESSAGE_SIZE = 20
MESSAGE_COLOR = (200, 180, 200)
MESSAGE_BG_COLOR = (20, 40, 20)

class Battle(object):
    # Battle holds all references to text surfaces, HP/name displays, and each monster
    # involved in a fight. Battle.state is in charge of everything here.
    def __init__(self):
        self.state = 'init'
        self.setup_monsters()
        self.setup_text()

    def setup_monsters(self):
        # Give us some dummy monsters for now so we can beat the shit out of them
        self.monster_x = monster.Monster('George', X_SPRITE_LOCATION, level=14)
        self.monster_y = monster.Monster('Bob', Y_SPRITE_LOCATION, level=4)
        self.monsters = [self.monster_x, self.monster_y]

    def setup_text(self):
        # Put any constantly updated text fields for the battle here
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
            
        # Battle messages
        elif text_object.type == 'battle_message':
            return self.get_updated_battle_message(self.state)

    def get_updated_battle_message(self, state):
        # Seperated this out into it's own function for ease of use. This will probably
        # get messy if we just use strings for states. Not sure what a good alternative
        # is.
        if self.state == 'init':
            return 'Encountered a wild %s!' % self.monster_y.name

        elif self.state == 'battle_menu':
            return 'Please choose type of action from menu using QWER.'
        
        elif self.state == 'fight_menu':
            return 'Please choose your attack using QWER keys.'

        elif self.state == 'first_monster_attacks':
            return '%s used %s and dealt %i damage to %s' % (
                self.monster_x.name, "Claw", 2, self.monster_y.name)

        elif self.state == 'second_monster_attacks':
            return '%s used %s and dealt %i damage to %s' % (
                self.monster_y.name, "Evil Claw", 1, self.monster_x.name)

        elif self.state == 'change_hp_and_check':
            return 'Checking HP'

        elif self.state == 'second_monster_dies':
            return '%s has been obliterated by %s!' % (self.monster_y.name, self.monster_x.name)

        elif self.state == 'first_monster_dies':
            return '%s has been obliterated by %s!' % (self.monster_x.name, self.monster_y.name)

        elif self.state == 'victory':
            return 'You have defeated %s and earned %i gold!' % (self.monster_y.name, 20)

        elif self.state == 'game_over':
            return 'Annihilated...'
        else:
            return 'Not completed'
            
    def deal_damage(self, user, target, damage):
        target.hp -= damage # This is very basic for now

    def decide_turn(self):
        return 'first_monster_attacks'

    def is_monster_dead(self, monster):
        if monster.hp <= 0.5:
            return True
        else:
            return False

    def accept(self):
        #print 'battle.state = %s' % self.state # Debug the state here
        # Press Q to stop the text barrage
        if self.state == 'init':
            self.state = 'battle_menu'
        elif self.state == 'battle_menu':
            self.state = 'fight_menu'
        elif self.state == 'fight_menu':
            self.state = self.decide_turn()

        # Monster X attacks monster Y first
        elif self.state == 'first_monster_attacks':
            self.deal_damage(self.monster_x, self.monster_y, 2)
            monster_was_killed = self.is_monster_dead(self.monster_y)
            if monster_was_killed:
                self.state = 'second_monster_dies'
            else:
                self.state = 'second_monster_attacks'

        # Monster Y attacks monster X second
        elif self.state == 'second_monster_attacks':
            self.deal_damage(self.monster_y, self.monster_x, 1)
            monster_was_killed = self.is_monster_dead(self.monster_x)
            if monster_was_killed:
                self.state = 'first_monster_dies'
            else:
                self.state = 'battle_menu'

        # Monster Y dies and user wins
        elif self.state == 'second_monster_dies':
            self.state = 'victory'

        # User loses game
        elif self.state == 'first_monster_dies':
            self.state = 'game_over'

        # Just exit in any case
        elif self.state == 'victory' or self.state == 'game_over':
            self.state = 'end'

    def decline(self):
        self.state = 'end'
