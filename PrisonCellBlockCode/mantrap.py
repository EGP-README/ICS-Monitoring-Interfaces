import pygame
from pygame.locals import *

import pygbutton
import indicator

"""
    Author: Evan Plumley
"""

class ManTrap:
    """
        The ManTrap simulates the access mechanism where two locked doors create a secure
        buffer space for entry into a secured area. The logic in this class ensures
        accurate simulation of mantrap logic is executes. Both doors cannot be opened 
        aty trhe same time and only one door can be unlocked at a time. This class
        also displays the door statuses on the interface.
    """
    def __init__(self, sim=None, x=0, y=0, current_state=0):
        """
            Initializes the ManTrap at a specific location on the interface 
            and controls image transformation as actions take place
        """
        if sim is not None:
            cell_padding_x = 25
            cell_padding_y = 25
            title_height = 25
            indicators_panel_width = 100
            grey = (200, 200, 200)
            dark_grey = (140, 140, 140)
            white = (255, 255, 255)
            black = (0,0,0)
            screen = sim.screen
            font = sim.font
            #self.inLoop = False #if a thread is running on a door
            self.door1Closed = True
            self.lock1Closed = True
            self.door2Closed = True
            self.lock2Closed = True
            self.indicatorLight = True #True is green state
            

            panel_width = (3*cell_padding_x+200) * 2
            panel_height = 2*cell_padding_y+325+title_height

            cell_door_start_x = x+ cell_padding_x+indicators_panel_width + 15
            cell_door_start_y = y+(3 * cell_padding_y)+title_height 

            cell_control_panel = pygame.draw.rect(screen, (grey), (x, y, panel_width, panel_height))

            #Title and door labels
            screen.blit(font.render('Man Trap', True, (black)), (x+10, y+10))
            screen.blit(font.render('1', True, (black)), (cell_door_start_x + 60 , cell_door_start_y - 40))
            screen.blit(font.render('2', True, (black)), (cell_door_start_x + 215 , cell_door_start_y - 40))

            #Trap Door 1 
            trap_door_dimensions = ((130,260))
            closed_door_icon = pygame.image.load ("images/closedTrap.png")
            open_door_icon= pygame.image.load ("images/openTrap.png")
            cell_door_icons = [closed_door_icon, open_door_icon]
            self.trap_door1 = indicator.Indicator(sim, cell_door_start_x, cell_door_start_y, cell_door_icons, trap_door_dimensions)

            #Trap Door 2 
            trap_door_dimensions = ((130,260))
            closed_door_icon = pygame.image.load ("images/closedTrap.png")
            open_door_icon= pygame.image.load ("images/openTrap.png")
            cell_door_icons = [closed_door_icon, open_door_icon]
            self.trap_door2 = indicator.Indicator(sim, cell_door_start_x + 150, cell_door_start_y, cell_door_icons, trap_door_dimensions)


            #Control Panel icon loading
            green_icon = pygame.image.load("images/greenLightAlt.png")
            red_icon = pygame.image.load("images/redLightAlt.png")
            lock_icon = pygame.image.load("images/locked.png")
            unlock_icon = pygame.image.load("images/unlocked.png")

            #Door light
            indicator_start_x =  cell_door_start_x + 105
            indicator_start_y = cell_door_start_y - 80
            indicator_icons = [green_icon, red_icon]
            indicator_dimensions = ((65, 70))
            self.secure_indicator = indicator.Indicator(sim, indicator_start_x, indicator_start_y, indicator_icons, indicator_dimensions)

            #lock unlock icon 1
            lock_start_x = cell_door_start_x - 100
            lock_start_y = cell_door_start_y + 70
            lock_icons = [lock_icon, unlock_icon]
            lock_dimensions = ((65,70))
            self.lock_indicator1 = indicator.Indicator(sim, lock_start_x, lock_start_y, lock_icons, lock_dimensions, grey)

             #lock unlock icon 2
            lock_start_x = cell_door_start_x + 310
            lock_start_y = cell_door_start_y + 70
            lock_icons = [lock_icon, unlock_icon]
            lock_dimensions = ((65,70))
            self.lock_indicator2 = indicator.Indicator(sim, lock_start_x, lock_start_y, lock_icons, lock_dimensions, grey)



