import pygame
from pygame.locals import *
import indicator
import pygbutton

"""
    Author: Evan Plumley

    The Guard Station component to the prison simulates a remote control of the locks.
    The alternative methods of control for the prison locks are simulated manual key usage
    or physical button pressing in the ICS environemnt
"""

class GuardStation:
    """
       Simulates remote control of prison cell locks and the man trap
    """
    def __init__(self, sim=None, num_cells=0, x=0, y=0):
        if sim:
            screen = sim.screen
            font = sim.font
            self.cell_btns = []
            self.lights = []
            self.btn_statuses = []
            self.button_pushed = []
            self.light_green = []
            self.panel_enabled = True
            self.panel_keyControl = True #enables the key o be overidden
            self.disable_clicked = False
            btn_height = 40;
            btn_width = 100;
            cell_padding_x = 25
            cell_padding_y = 60
            grey = (200, 200, 200)
            dark_grey = (140, 140, 140)
            white = (255, 255, 255)
            black = (0,0,0)

            title_height = 25
            light_height = 35
            light_width = 35
            panel_width = btn_width * num_cells + (num_cells+1)*cell_padding_x
            panel_height = btn_height + 2*cell_padding_y + title_height + light_height

            guard_display_panel = pygame.draw.rect(screen, (grey), (x, y, panel_width, panel_height))
            
         
            #flag for cell button toggle
            for i in range(0, num_cells):
                self.button_pushed.append(False)

            #flag for light to toggle
            for i in range(0, num_cells - 1):
                self.light_green.append(True)

            #Title
            #screen.blit(font.render('Guard Station Panel', True, (black)), (x+20, y+10))

            #guard station image loading
            green_icon = pygame.image.load("images/greenLightAlt.png")
            red_icon = pygame.image.load("images/redLightAlt.png")
            pressed_icon = pygame.image.load("images/pressed.png")
            notPressed_icon = pygame.image.load("images/notpressed.png")
            panelEnabled = pygame.image.load("images/panelenabled.png")
            panelDisabled = pygame.image.load("images/panelDisabled.png")
            

            cell_start_x = x + cell_padding_x
            cell_start_y = y + cell_padding_y+title_height+ (0.5 * light_height)
            light_start_x = x + cell_padding_x + (btn_width*0.5) - (light_width * 0.5)
            light_start_y = y + cell_padding_y
            status_start_x = x + cell_padding_x
            status_start_y = y + cell_padding_y + title_height+ (0.5 * light_height) + btn_height + (btn_height * 0.5)

            #disable button to the right of the panel
            self.disable_btn = pygbutton.PygButton((cell_start_x + (panel_width * 0.37) , y - cell_padding_y , 125, btn_height), "Toggle Panel")
            self.disable_btn.draw(screen)

            #create enabled/disbaled indicator
            panel_icons = [panelEnabled, panelDisabled]
            icon_dimensions = ((400,45))
            self.enable_label = indicator.Indicator(sim, x + (0.18 * panel_width), y + 5 , panel_icons, icon_dimensions, grey)

            for i in range(0, num_cells):
                cell_num = i+1
                if cell_num == num_cells-1:
                    button_text = "Trap 1"
                elif cell_num == num_cells:
                    button_text = "Trap 2"
                else:
                    button_text = "Cell %s" % cell_num

                cell_btn = pygbutton.PygButton((cell_start_x, cell_start_y, btn_width, btn_height), button_text)
                cell_btn.draw(screen)

                #Door light
                if i == num_cells - 2:
                    light_icons = [green_icon, red_icon]
                    light_dimensions = ((35,35))
                    light = indicator.Indicator(sim, light_start_x + (0.63 * btn_width), light_start_y, light_icons, light_dimensions)
                    self.lights.append(light)
                elif i == num_cells -1:
                    pass
                else:
                    light_icons = [green_icon, red_icon]
                    light_dimensions = ((35,35))
                    light = indicator.Indicator(sim, light_start_x, light_start_y, light_icons, light_dimensions)
                    self.lights.append(light)

                #button indicator
                status_icons = [notPressed_icon, pressed_icon]
                status_dimensions = ((100, 20))
                status = indicator.Indicator(sim, status_start_x, status_start_y, status_icons, status_dimensions, grey)

                #adding all objects to respective lists
                self.cell_btns.append(cell_btn)
                self.btn_statuses.append(status)

                #adjusting placements for next iteration of icon and button creation
                light_start_x += btn_width + cell_padding_x
                cell_start_x += btn_width + cell_padding_x
                status_start_x += btn_width + cell_padding_x

 
    def disablePanel(self):
        if self.panel_enabled == True:
             self.panel_enabled = False
             self.enable_label.change_state()
             

    def enablePanel(self):
        if self.panel_enabled == False:
            self.panel_enabled = True
            self.enable_label.change_state()
            
               
            
            
