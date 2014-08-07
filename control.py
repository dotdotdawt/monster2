#

# 3rd party imports
import sys
import pygame

# Local imports
import battle

class Control(object):
    #
    #
    def __init__(self, game):
        self.game = game
        self.state = 'world'
        self.setup_defaults()
        self.main_loop()

    def setup_defaults(self):
        # Total number of directions moving
        self.moving = 0
        # Self explanatory
        self.directions = {
            'up': (0, -1), 'down': (0, 1),
            'left': (-1, 0), 'right': (1, 0)
            }
        # Pygame's names for each direction
        self.pg_directions = {
            pygame.K_LEFT:'left',
            pygame.K_RIGHT:'right',
            pygame.K_UP: 'up',
            pygame.K_DOWN: 'down'
            }
        self.reset_direction_states()

    def reset_direction_states(self):
        # Do world_movement by polling
        self.direction_states = {
            'up': False, 'down': False, 'left': False, 'right': False
            }

    def world_handle_movement(self):
        total = (self.direction_states['left'] + self.direction_states['right'] +
                 self.direction_states['up'] + self.direction_states['down'])

        # We want to override movement if there are 3 directional inputs
        # We allow movement with 2 directions but we slow the movement. This should be done
        # using vectors... For now just reducing the speed with the multi True/False flag
        override = False
        multi = False
        if total >= 3 or total == 0:
            override = True
        if total == 2:
            multi = True

        # Now decide if the player moves
        if override:
            pass
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

    def world_handle_keyup_event(self, event):
        # Interaction events
        if event.key == pygame.K_q:
            self.start_battle()

        # Directional events
        if event.key in self.pg_directions:
            for direction in self.pg_directions:
                if direction == event.key:
                    self.world_update_direction(self.pg_directions[direction], pressed=False)

    def world_handle_keydown_event(self, event):
        # Directional events
        if event.key in self.pg_directions:
            for direction in self.pg_directions:
                if direction == event.key:
                    self.world_update_direction(self.pg_directions[direction], pressed=True)

    def battle_handle_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                pass
            elif event.key == pygame.K_r:
                self.exit_battle()

    def event_loop(self, state):
        for event in pygame.event.get():
            # Always allow quitting
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.running = False
            # World stuff
            if state == 'world':
                if event.type == pygame.KEYUP:
                    self.world_handle_keyup_event(event)
                elif event.type == pygame.KEYDOWN:
                    self.world_handle_keydown_event(event)
            # Battle stuff
            elif state == 'battle':
                self.battle_handle_event(event)

    def update_non_events(self, state):
        if state == 'world':
            self.world_handle_movement()

    def update_everything(self, state):
        if state != 'wait': # If the player is not allowed to input, state = 'wait'
            self.event_loop(state)
            self.update_non_events(state)

    def start_battle(self):
        self.state = 'battle'
        self.reset_direction_states()
        self.game.battle = battle.Battle()

    def exit_battle(self):
        self.state = 'world'

    def main_loop(self):
        while self.game.running:
            self.update_everything(self.state)
            self.game.update_display(self.state)
            self.game.fps_clock.tick(self.game.fps)

        pygame.quit()
        sys.exit()
