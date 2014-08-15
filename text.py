import pygame

class Text(object):
    #
    #
    def __init__(self, text_type, location, size, color, bg_color, xy=None):
        # Determines which text type: hp, name, etc.
        # Valid types:
        # BATTLE - name, hp, battle_message
        # SIDEMENU - name, hp, level, next_xp, curr_xp, atk, def, speed
        self.type = text_type
        
        # Determines which monster of the 2 if making Battle displays.
        # If not making a Battle display, just ignore this
        self.xy = xy

        self.x, self.y = location
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.string = 'has not been updated'
        self.anti_aliasing = True
        self.font_name = 'freesansbold.tff'
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.image = self.font.render(self.string, self.anti_aliasing, self.color, self.bg_color)
        self.rect = self.image.get_rect()
        print 'Created Text() object of type: %s ' % text_type
        self.update()

    def update(self):
        self.image = self.font.render(
            self.string, self.anti_aliasing, self.color, self.bg_color
            )
        self.rect.topleft = (self.x, self.y)
