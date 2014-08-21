#

# 3rd party imports
import sys
import pygame
import gc

# Local imports
import battle

# Enabling garbage collection - honestly I have no idea how it works
gc.enable()

# Global variables
kLEFT = pygame.K_LEFT
kRIGHT = pygame.K_RIGHT
kUP = pygame.K_UP
kDOWN = pygame.K_DOWN

class Control(object):
    #
    #
    def __init__(self, game):
        self.game = game
        self.state = 'world' # For now, just so we can test
        self.game.battle = battle.Battle()
        self.setup_defaults()
        self.main_loop()

    def setup_defaults(self):
        self.moving = 0 # Total number of directions moving
        self.directions = { # Directions are a pair for diagonal movement
            kUP: (0, -1), kDOWN: (0, 1), kLEFT: (-1, 0), kRIGHT: (1, 0) }
        self.reset_direction_states()

    def reset_direction_states(self):
        # This function also sets states initially, so it must be run
        self.direction_states = {
            kUP: False, kDOWN: False, kLEFT: False, kRIGHT: False }

    ## BATTLE ##
    def start_battle(self):
        self.state = 'battle'
        self.game.battle.setup_new_battle(self.game.player.monsters_in_party)
        self.reset_direction_states() # Prevents movement bugs

    def exit_battle(self):
        self.state = 'world'

    def battle_handle_event(self, event):
        # KEY UPS #
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.game.battle.accept()
                
            elif event.key == pygame.K_r:
                self.game.battle.decline()

    ## WORLD ##  
    def world_handle_movement(self):
        # We allow movement with 2 directions, but we slow the movement.
        # To do this we use a multi flag if the total is 2
        override = False; multi = False
        total = (self.direction_states[kLEFT] + self.direction_states[kRIGHT] +
                 self.direction_states[kUP] + self.direction_states[kDOWN])
        # We want to override movement if there are 3 directional inputs
        if total >= 3 or total == 0:
            override = True
        if total == 2:
            multi = True
        # Decide if the player moves
        if override == False: 
            for direction in self.direction_states:
                if self.direction_states[direction]:
                    self.game.player.move(self.directions[direction], multi)

    def world_update_direction(self, direction, pressed=False):
        if pressed:
            self.direction_states[direction] = True
            self.moving += 1
        else:
            if self.direction_states[direction]:
                self.moving -= 1
                self.direction_states[direction] = False

    def world_handle_event(self, event):
        # KEY UPS #
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_q:
                self.start_battle()
            if event.key in self.directions: 
                self.world_update_direction(event.key, pressed=False)
                
        # KEY DOWNS #
        if event.type == pygame.KEYDOWN: 
            if event.key in self.directions: # Directional events
                self.world_update_direction(event.key, pressed=True)

    ## STATELESS ##
    def update_non_events(self, state):
        # This function updates the state of all things that are not restricted
        # by having an input, such as world movement and animations. These
        # things can be turned on or off but can't be controlled after.
        if state == 'world':
            self.world_handle_movement()
        elif state == 'battle':
            if self.game.battle.state == 'end':
                self.exit_battle()
        for btn in self.game.buttons:
            self.game.buttons[btn].update()

    def handle_non_state_event(self, event):
        # Non state events are events that can happen anywhere such as:
        #   -QWER button press that causes animation
        #   -Pressing ESC to exit game
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.game.running = False # Always allow quitting
            if event.key in self.game.buttons:
                self.game.buttons[event.key].pressed = False # One of the QWER btns
        if event.type == pygame.KEYDOWN:
            if event.key in self.game.buttons:
                self.game.buttons[event.key].is_currently_pressed() # One of the QWER btns

    ## IMPORTANTE ##
    def event_loop(self, state):
        # Goes through every input that has happened since last frame
        # and handles each event accordingly
        for event in pygame.event.get():
            if state == 'world':
                self.world_handle_event(event)
            elif state == 'battle':
                self.battle_handle_event(event)
            self.handle_non_state_event(event)
            
    def main_loop(self):
        # The entire logic of the program here, be careful with changes
        while self.game.running:
            if self.state != 'wait': # wait if player can't do anything
                self.event_loop(self.state)
                self.update_non_events(self.state)
            self.game.update_display(self.state)
            self.game.fps_clock.tick(self.game.fps)

        pygame.quit()
        sys.exit()
