#

# 3rd party imports
import pygame

# Local imports
import player


class Game(object):
    #
    #
    def __init__(self):
        self.setup_defaults()
        self.setup_pygame()
        self.setup_player()

    def setup_defaults(self):
        self.screen_size = (800, 600)
        self.refresh_color = (100, 100, 100)
        self.battle_color = (200, 100, 100)
        self.fps = 30
        self.running = True

    def setup_pygame(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.fps_clock = pygame.time.Clock()

    def setup_player(self):
        self.player = player.Player()

    def update_display(self, state):
        if state == 'world':
            self.screen.fill(self.refresh_color)
            self.player.update()
            self.screen.blit(self.player.image, self.player.rect)

        elif state == 'battle':
            self.screen.fill(self.refresh_color)
            for monster in self.battle.monsters:
                monster.update()
                self.screen.blit(monster.image, monster.rect)
            for text_object in self.battle.text_objects:
                self.battle.update_text_object(text_object)
                self.screen.blit(text_object.image, text_object.rect)
                
        #pygame.display.flip()
        pygame.display.update()
