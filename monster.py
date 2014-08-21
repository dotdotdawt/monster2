import pygame

ATK_SOUND_U = 'resources\sound_attack_boom.ogg'
ATK_SOUND_X = 'resources\sound_attack_twitch.ogg'
DEATH_SOUND = 'resources\sound_death.ogg'
VOLUME_LEVEL = 0.61

FILE_PATH_U = 'resources\monster1.png'
FILE_PATH_X = 'resources\monster2.png'

ALLIED_LOCATION = (0,0)
ENEMY_LOCATION = (100, 100)

# Constants
C_DAMAGE_MULTIPLIER = 1.0
C_MOVE_POWER_DIVISOR = 4.0

C_DEFENSE_MULTIPLIER = 0.75
C_REDUCTION_BASE = 10.0

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
        self.setup_sounds()
        self.setup_image()

    def setup_defaults(self):
        self.base_hp = self.level
        self.hp = self.base_hp
        self.ph_atk = self.level * 2
        self.ph_def = self.level * 1
        self.speed = 10
        self.moves = {
            'Claw': Move('Claw', 10, qwer_loc='q'),
            'Evil Claw': Move('Evil Claw', 5, qwer_loc='w')
            }

    def setup_sounds(self):
        self.sounds = {
            'move1': pygame.mixer.Sound(ATK_SOUND_U),
            'move2': pygame.mixer.Sound(ATK_SOUND_X),
            'death': pygame.mixer.Sound(DEATH_SOUND)
            }
        for sound in self.sounds:
            self.sounds[sound].set_volume(VOLUME_LEVEL)       

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

    def get_calculated_damage(self, target, move):
        # This is very basic and not real for now
        move_base_power = (move.power / C_MOVE_POWER_DIVISOR)
        atk_multiplier = (self.ph_atk * C_DAMAGE_MULTIPLIER)
        raw_damage = (move_base_power * atk_multiplier)

        def_multiplier = (target.ph_def * C_DEFENSE_MULTIPLIER)
        base_reduction = (raw_damage / C_REDUCTION_BASE)
        raw_reduction = (def_multiplier * base_reduction)
        
        return (raw_damage - raw_reduction)        

def set_sprite_anchor_points(new_allied_location, new_enemy_location):
    global ALLIED_LOCATION, ENEMY_LOCATION
    ALLIED_LOCATION = new_allied_location
    ENEMY_LOCATION = new_enemy_location

class Move(object):
    #
    #
    def __init__(self, name, power, qwer_loc=None):
        self.name = name
        self.power = power
        self.qwer_loc = qwer_loc
