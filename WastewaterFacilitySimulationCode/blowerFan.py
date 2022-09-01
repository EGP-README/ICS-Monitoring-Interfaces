import pygame
from pygame.locals import *

import pygbutton
"""
    Author: Evan Plumley
"""

class BlowerFan:
    """Adds the fan image to the interface and controls the image rotation
    """

    def __init__(self, sim=None, fan_num=0, x=0,y=0):
        if sim is not None:
            #load the fan onto the screen
            self.fan_num = fan_num
            self.fan_image = pygame.image.load("wwtimages/fanBlade.jpg")
            sim.screen.blit(fan_image, (x,y))


    def rotate(self):
        pygame.transform.rotate(self.fan_image, 3)
