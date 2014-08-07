import pygame

class Text(object):
    #
    #
    def __init__(self, xy, text_type, location, size, color, bg_color):
        self.xy = xy # Determines which monster of the 2
        self.type = text_type # Determines which text type: hp, name, etc.
        self.x, self.y = location
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.string = 'has not been updated' # Empty so we can initialize
        self.anti_aliasing = True
        self.font_name = 'freesansbold.tff'
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.image = self.font.render(self.string, self.anti_aliasing, self.color, self.bg_color)
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        self.rect.topleft = (self.x, self.y)
