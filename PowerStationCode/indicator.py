import pygame
from pygame.locals import *

"""Author Evan Plumley
"""

class Indicator:
    """ The image controller for the indication of substation status
    """

    def __init__(self, sim=None, x=0, y=0, icons = [], icon_size=None, background_color=None):
        if sim:
            self.state_num = 0
            self.x = x
            self.y = y
            self.icons = icons
            self.sim = sim
            self.icon_size = icon_size
            self.background_color = background_color
            start_state_icon = icons[0]

            if icon_size:
                start_state_icon = pygame.transform.scale(start_state_icon, icon_size)
            sim.screen.blit(start_state_icon, (x, y))


    def change_state(self, screen=None, state_num=None):
        if state_num is None:
            self.state_num = (self.state_num + 1) % 2
        state_icon = self.icons[self.state_num]
        if self.icon_size:
            state_icon = pygame.transform.scale(state_icon, self.icon_size)
        if screen is None:
            screen = self.sim.screen

        if self.background_color:
            shape = pygame.Surface(self.icon_size, flags=SRCALPHA)
            shape.fill(self.background_color)
            screen.blit(shape, (self.x, self.y))
            pygame.display.update()

        screen.blit(state_icon, (self.x, self.y))
