#

# 3rd party imports
import pygame

# Local imports
import text
import monster

# Globals
X_NAME_LOCATION = (500, 400)
X_HP_LOCATION = (500, 450)
X_SPRITE_LOCATION = (550, 425)
Y_NAME_LOCATION = (150, 50)
Y_HP_LOCATION = (150, 100)
Y_SPRITE_LOCATION = (200, 75)
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

# I am trying to find a fancier way of doing this that looks good.
# Look into this more later. 
"""
SCREEN_SIZE = (800, 600) # MAKE SURE THIS IS ACCURATE
HALF_X = SCREEN_SIZE[0]/2
HALF_Y = SCREEN_SIZE[1]/2
SCREEN_OFFSET_BOT = (HALF_X-50, 0)
SCREEN_OFFSET_TOP = (HALF_X+50, 0)
HP_OFFSET = (0, 50)
SPRITE_OFFSET = (100, 25)

X_ANCHOR = (SCREEN_SIZE[0]-SCREEN_OFFSET_BOT[0], SCREEN_SIZE[1]-SCREEN_OFFSET_BOT[1])
Y_ANCHOR = (SCREEN_OFFSET_TOP[0], SCREEN_OFFSET_TOP[1])

X_NAME_LOCATION = (X_ANCHOR[0], X_ANCHOR[1])
X_HP_LOCATION = (X_ANCHOR[0]+HP_OFFSET[0], X_ANCHOR[1]+HP_OFFSET[1])
X_SPRITE_LOCATION = (X_ANCHOR[0]-SPRITE_OFFSET[0], X_ANCHOR[1]+SPRITE_OFFSET[1])

Y_NAME_LOCATION = (Y_ANCHOR[0], Y_ANCHOR[1])
Y_HP_LOCATION = (Y_ANCHOR[0]-HP_OFFSET[0], Y_ANCHOR[1]+HP_OFFSET[1])
Y_SPRITE_LOCATION = (Y_ANCHOR[0]+SPRITE_OFFSET[0], Y_ANCHOR[1]+SPRITE_OFFSET[1])
"""

class Battle(object):
    # Battle holds all references to text surfaces, HP/name displays, and each monster
    # involved in a fight. Battle.state is in charge of everything here.
    def __init__(self):
        self.state = 'off'
        # Sets the X points that are prescribed in battle globally for all monsters
        monster.set_sprite_anchor_points(X_SPRITE_LOCATION, Y_SPRITE_LOCATION)
        self.setup_text()

    def setup_text(self):
        # Put any constantly updated text fields for the battle here
        self.recent_move = 'Empty'
        self.recent_damage = 0
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

    def update_text(self, text_object):
        # Only pertains to a text_object
        text_object.string = self.get_updated_string(text_object)
        text_object.update()

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
                self.monster_x.name, self.recent_move,
                self.recent_damage, self.monster_y.name
                )

        elif self.state == 'second_monster_attacks':
            return '%s used %s and dealt %i damage to %s' % (
                self.monster_y.name, self.recent_move,
                self.recent_damage, self.monster_x.name
                )

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

    def apply_move(self, move_loc):
        #attacking = self.get_attacking_monster()
        attacking = self.monster_x
        if self.monster_x == attacking:
            defending = self.monster_y
        else:
            defending = self.monster_x

        for move in attacking.moves:
            if attacking.moves[move].qwer_loc == move_loc:
                move_used = attacking.moves[move]
                damage = attacking.get_calculated_damage(defending, move_used)
        
        defending.hp -= damage # Actual application of damage
        self.recent_damage = damage
        self.recent_move = move_used.name
        self.recent_death_alert = self.is_monster_dead(defending)

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
            self.apply_move('q')
            self.monster_x.sounds['move1'].play()
            
            if self.recent_death_alert:
                self.state = 'second_monster_dies'
            else:
                self.state = 'second_monster_attacks'

        # Monster Y attacks monster X second
        elif self.state == 'second_monster_attacks':
            self.apply_move('w')
            self.monster_y.sounds['move2'].play()
            
            if self.recent_death_alert:
                self.state = 'first_monster_dies'
            else:
                self.state = 'battle_menu'

        # Monster Y dies and user wins
        elif self.state == 'second_monster_dies':
            self.monster_y.sounds['death'].play()
            self.state = 'victory'

        # User loses game
        elif self.state == 'first_monster_dies':
            self.monster_x.sounds['death'].play()
            self.state = 'game_over'

        # Just exit in any case
        elif self.state == 'victory' or self.state == 'game_over':
            self.state = 'end'

    def decline(self):
        self.state = 'end'

    def setup_new_battle(self, monsters_in_player_party):
        self.state = 'init'
        # Give us some dummy monsters for now so we can beat the shit out of them
        self.monsters_in_player_party = monsters_in_player_party
        self.monster_x = self.monsters_in_player_party[0]
        self.monster_y = monster.Monster('Bob', 'npc', level=4)
        self.monsters = [self.monster_x, self.monster_y]

