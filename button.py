import pygame

ANIMATION_THRESHOLD = 3

class Button(object):
    #
    #
    def __init__(self, name, icon_path, location=None, key_bindings=None):
        self.x, self.y = location
        self.load_images(icon_path)
        self.name = name
        self.key_bindings = key_bindings
        self.pressed = False
        self.reset()

    def load_images(self, icon_path):
        directory = 'resources\\'
        normal_path = '%sbtn_%s_normal.jpg' % (directory, icon_path)
        dis_path = '%sbtn_%s_disabled.jpg' % (directory, icon_path)
        self.normal_image = pygame.image.load(normal_path)
        self.disabled_image = pygame.image.load(dis_path)

    def reset(self):
        self.pressed_duration = 0
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def is_currently_pressed(self):
        self.pressed = True
        self.pressed_duration = 1            

    def update(self):
        if self.pressed:
            if self.image == self.normal_image:
                self.image = self.disabled_image
        else:
            if self.pressed_duration > 0:
                self.pressed_duration += 1
                if self.pressed_duration >= ANIMATION_THRESHOLD:
                    self.reset()
