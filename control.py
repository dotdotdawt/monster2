#

# 3rd party imports
import sys
import pygame


class Control(object):
    #
    #
    def __init__(self, game):
        self.game = game
        self.setup_defaults()
        self.main_loop()

    def setup_defaults(self):
        self.moving = 0
        self.directions = {
            'up': (0, -1), 'down': (0, 1),
            'left': (-1, 0), 'right': (1, 0)
            }
        self.direction_states = {
            'up': False, 'down': False, 'left': False, 'right': False
            }
        self.pg_directions = {
            pygame.K_LEFT:'left',
            pygame.K_RIGHT:'right',
            pygame.K_UP: 'up',
            pygame.K_DOWN: 'down'
            }

    def world_movement(self):
        total = (self.direction_states['left'] + self.direction_states['right'] +
                 self.direction_states['up'] + self.direction_states['down'])

        # We want to override movement if there are 3 directional inputs
        # We allow movement with 2 directions but we slow the movement. This should be done
        # using vectors... For now just reducing the speed with the multi True/False flag.
        if total >= 3:
            override = True
        if total == 2:
            override = False
            multi = True
        if total == 1:
            override = False
            multi = False
        if total == 0:
            override = True
            multi = False

        # Now decide
        if override:
            self.no_inputs = True
            pass
        if not override:
            self.no_inputs = False
            for direction in self.direction_states:
                if self.direction_states[direction]:
                    self.game.player.move(self.directions[direction], multi)

    def update_direction(self, direction, pressed=False):
        if pressed:
            self.direction_states[direction] = True
            self.moving += 1
            
        else:
            if self.direction_states[direction]:
                self.moving -= 1
                self.direction_states[direction] = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                self.handle_keyup_events(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_events(event)
        if self.moving:
            self.world_movement()

    def handle_keyup_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.running = False

        if event.key in self.pg_directions:
            for direction in self.pg_directions:
                if direction == event.key:
                    direction_to_update = self.pg_directions[direction]
                    self.update_direction(direction_to_update, pressed=False)

    def handle_keydown_events(self, event):
        if event.key in self.pg_directions:
            for direction in self.pg_directions:
                if direction == event.key:
                    direction_to_update = self.pg_directions[direction]
                    self.update_direction(direction_to_update, pressed=True)

    def main_loop(self):
        while self.game.running:
            self.handle_events()
            self.game.update_display()
            self.game.fps_clock.tick(self.game.fps)

        pygame.quit()
        sys.exit()
