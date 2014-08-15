#

# 3rd party imports
import pygame

# Local imports
import player
import button
import sidemenu

# Display globals
SCREEN_SIZE = (800, 600)
FPS = 30
STATES_THAT_ALLOW_UI = [ 'world', 'battle' ]

# QWER globals
Q_ICON_PATH = 'attack'
W_ICON_PATH = 'summon'
E_ICON_PATH = 'help'
R_ICON_PATH = 'flee'
BUTTON_X_SIZE = 64
BUTTON_Y_OFFSET = 64
BUTTON_X_INITIAL = (SCREEN_SIZE[0] - (BUTTON_X_SIZE*4))/2
Q_LOCATION = (BUTTON_X_INITIAL+BUTTON_X_SIZE*0, SCREEN_SIZE[1]-BUTTON_Y_OFFSET)
W_LOCATION = (BUTTON_X_INITIAL+BUTTON_X_SIZE*1, SCREEN_SIZE[1]-BUTTON_Y_OFFSET)
E_LOCATION = (BUTTON_X_INITIAL+BUTTON_X_SIZE*2, SCREEN_SIZE[1]-BUTTON_Y_OFFSET)
R_LOCATION = (BUTTON_X_INITIAL+BUTTON_X_SIZE*3, SCREEN_SIZE[1]-BUTTON_Y_OFFSET)

class Game(object):
    #
    #
    def __init__(self):
        self.setup_defaults()
        self.setup_pygame()
        self.setup_player()
        self.setup_sidemenu()
        self.setup_qwer()

    def setup_defaults(self):
        self.screen_size = SCREEN_SIZE
        self.refresh_color = (100, 100, 100)
        self.battle_color = (200, 100, 100)
        self.fps = FPS
        self.states_with_ui = STATES_THAT_ALLOW_UI
        self.running = True

    def setup_pygame(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.fps_clock = pygame.time.Clock()

    def setup_player(self):
        self.player = player.Player()

    def setup_qwer(self):
        self.buttons = {
            pygame.K_q: button.Button('q', Q_ICON_PATH, Q_LOCATION, pygame.K_q),
            pygame.K_w: button.Button('w', W_ICON_PATH, W_LOCATION, pygame.K_w),
            pygame.K_e: button.Button('e', E_ICON_PATH, E_LOCATION, pygame.K_e),
            pygame.K_r: button.Button('r', R_ICON_PATH, R_LOCATION, pygame.K_r)
            }
        
    def setup_sidemenu(self):
        self.sidemenu = sidemenu.SideMenu()

    def show_all_objects_in_list(self, objects, is_dictionary=False):
        if is_dictionary:
            for key in objects:
                objects[key].update()
                self.screen.blit(objects[key].image, objects[key].rect)
        else:
            for obj in objects:
                obj.update()
                self.screen.blit(obj.image, obj.rect)

    def update_display(self, state):           
        if state == 'world':
            self.screen.fill(self.refresh_color)
            self.player.update()
            self.screen.blit(self.player.image, self.player.rect)
            
        elif state == 'battle':
            self.screen.fill(self.battle_color)
            
            # Updates
            for text_object in self.battle.text_objects:
                self.battle.update_text(text_object)

            # Show everything from each list
            self.show_all_objects_in_list(self.battle.monsters)
            self.show_all_objects_in_list(self.battle.text_objects)

        if state in self.states_with_ui:
            # Wipe with a background
            self.screen.blit(self.sidemenu.bg_img, self.sidemenu.bg_rect)
            
            # Sidemenu
            monster_display_in_sidemenu = self.player.get_active_monster()
            self.sidemenu.update(monster_display_in_sidemenu)
            #self.screen.blit(self.sidemenu.bg_image, self.sidemenu.bg_rect) # sidemenu bg

            self.show_all_objects_in_list(self.sidemenu.text_objects, is_dictionary=True)
            self.show_all_objects_in_list(self.buttons, is_dictionary=True)
                
        pygame.display.flip()
