import pygame

ANIMATION_THRESHOLD = 5

class Button(object):
    #
    #
    def __init__(self, name, icon_path, location=None, key_bindings=None):
        self.x, self.y = location
        self.load_images(icon_path)
        self.name = name
        self.key_bindings = key_bindings
        self.reset()

    def load_images(self, icon_path):
        directory = 'resources\\'
        normal_path = '%sbtn_%s_normal.jpg' % (directory, icon_path)
        dis_path = '%sbtn_%s_disabled.jpg' % (directory, icon_path)
        self.normal_image = pygame.image.load(normal_path)
        self.disabled_image = pygame.image.load(dis_path)

    def reset(self):
        self.pressed = False
        self.pressed_duration = 0
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def show_as_pressed(self):
        self.image = self.disabled_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        if self.pressed:
            if self.image != self.normal_image:
                self.show_as_pressed()
            self.pressed_duration += 1
            if self.pressed_duration >= ANIMATION_THRESHOLD:
                self.reset()
"""
    def special_case(self):
        if self.name == 'q' and pygame.K_q in self.key_bindings:
            self.is_q = True
        elif self.name == 'w' and pygame.K_w in self.key_bindings:
            self.is_w = True
        elif self.name == 'e' and pygame.K_e in self.key_bindings:
            self.is_e = True
        elif self.name == 'r' and pygame.K_r in self.key_bindings:
            self.is_r = True
"""
