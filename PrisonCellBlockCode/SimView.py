import os
import pygame
import sys
import time
from pygame.locals import *
import serial
import thread
import pygbutton

"""
# Author: Evan Plumley
#
# The Sim class was built to simulate the supervision and control of an
# automated prison cell door. It communicates to a Y-box (AFIT Propriatary Device)
# and polls it to find the status of the door (open or closed) and displays the
# status. It can also send an open or close command to the Y-box.
#
# dependencies: pygame, pyserial
"""



display_width = 1025
display_height = 700



class Sim(object):
    """
       Controls the overall simulation and supervision of the interface
    """
    def __init__(self):
        pygame.init()
        self.openState = False
        self.font = pygame.font.SysFont('Times', 25)
        pygame.display.set_caption('Ybox Simulation')
        self.screen = pygame.display.set_mode((display_width, display_height), 0, 32)
        self.screen.fill((black))
        pygame.display.update()
        clock = pygame.time.Clock()


    def addLightRect(self):
        #self.ButtonRect = pygame.draw.rect(self.screen, (grey), (195, 500, 200, 100), 0)
        button_obj = pygbutton.PygButton((195,500,200,100), '')
        button_obj.draw(self.screen)
        pygame.display.update()

    def addDarkRect(self):
        #self.ButtonRect = pygame.draw.rect(self.screen, (dark_grey), (195, 500, 200, 100), 0)
        #pygame.display.update()
        pass

    def eraseText(self):
        self.screen.fill((black), (160, 400, 280, 40))
        pygame.display.update()

    def addClosedText(self):
        self.screen.blit(self.font.render('DOOR CLOSED', True, (white)), (210, 400))
        pygame.display.update()

    def addOpenText(self):
        self.screen.blit(self.font.render('DOOR OPEN', True, (white)), (225, 400))
        pygame.display.update()

    def addButtonText(self):
        if Display.openState == True:
            self.screen.blit(self.font.render('Close Door', True, (black)), (230, 535))
        else:
            self.screen.blit(self.font.render('Open Door', True, (black)), (235, 535))
        pygame.display.update()

    def addTitleText(self):
        self.screen.blit(title, (250, 30))
        pygame.display.update()

    def drawGreenLight(self):
        self.screen.blit (greenL, (200, 180))

    def drawRedLight(self):
        self.screen.blit (redL, (200, 180))

    def drawClosedDoor(self):
        self.screen.blit (closedDoor, (600, 150))

    def drawOpenDoor(self):
        self.screen.blit (openDoor, (600, 150))

    def doorOpenState(self):
        Display.eraseText()
        Display.addOpenText()
        Display.drawRedLight()
        Display.drawOpenDoor()
        pygame.display.update()

    def doorClosedState(self):
        Display.eraseText()
        Display.addClosedText()
        Display.drawGreenLight()
        Display.drawClosedDoor()
        pygame.display.update()


def asend(cmd):
    ard.write(cmd.encode())

def aRead(cmd):
    ard.write(cmd.encode())
    line = ard.readline().decode()
    return line

def timedReads():
    past = int(round(time.time() * 1000)) #getting starting milisecond time to execute reads from the ybox

    while True:
        present = int(round(time.time() * 1000)) #getting present time to comapre to past
            #check to see if 100 milliseconds have  passed
        if present - past >= 100:
            past = present
            asend("R1,0\n") #conduct a read and check the value
            line = ard.readline().decode()
            line = line.strip()
            if line == ("r1,0,400") and Display.openState == True: #if the value is energized, change the state
                Display.doorClosedState()
                Display.openState = False
                Display.addDarkRect()
                Display.addButtonText()
            elif line == ("r1,0,0") and Display.openState == False: #if the value is energized, change the state
                Display.doorOpenState()
                Display.openState = True
                Display.addDarkRect()
                Display.addButtonText()


if __name__ == '__main__':
    #defining color schemes
    green = (200,0,0)
    white = (255, 255, 255)
    black = (0,0,0)
    grey = (200, 200, 200)
    dark_grey = (140, 140, 140)
    light_blue = (0, 0, 255)
    dark_blue = (0, 0, 150)

    #preloading images
    title = pygame.image.load("images/prisonTitle.png")
    greenL = pygame.image.load("images/greenLightAlt.png")
    redL = pygame.image.load("images/redLightAlt.png")
    closedDoor = pygame.image.load ("images/closedDoor.png")
    openDoor= pygame.image.load ("images/openDoor.png")
    """
    #open serial port to arduino
    print ('opening serial port')
    #The first arguement is the com port number. Base 0 (e.g Com port 4 is 3)
    ard = serial.Serial(
	port='COM4',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
        timeout = 1
	)
    time.sleep(1)
    print ("Initialize Complete")
    print ('Aquiring Ybox data')

    CMD = "M\n"

    modules = []

    asend(CMD)
    for i in range(0, 9):
        line = ard.readline().decode()
        line = line.strip ('\r\n')
        modules.append(line)
    print (modules)
    """
    #executing initial displays
    #when we are communicating we need to read the ybox
    #to know what the inital display should be
    Display = Sim()
    Display.addLightRect()
    Display.addTitleText()

    """
    ######!!!!!!!!!!!! under construction !!!!!!!!!!!!!!!!!!!!#########
    #### need to determine the proper starting state
    asend("R1,0\n") #conduct a read and check the value
    line = ard.readline().decode()
    line = line.strip()
    if line == "r1,0,400": ##hard coded for the slot
       Display.doorClosedState()
    else:
       Display.doorOpenState()
    try:
       _thread.start_new_thread(timedReads, ())
    except:
       print ("Error: unable to start thread")

    print ('here')
    """
    qt = False #quit event
    inZone = False

    #main event handling loop
    while not qt:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                qt = True

            #If you are in the button zone make the button darker, else make it light
            if (195 + 200 > mouse[0] > 195 and 500 + 100 > mouse [1] > 500) and inZone == False:
                Display.addLightRect()
                Display.addButtonText()
                inZone = True
            #Not in the zone nor previously in the zone
            elif not(195 + 200 > mouse[0] > 195 and 500 + 100 > mouse [1] > 500) and inZone == False:
                inZone = False
                Display.addButtonText()
            #exiting the zone
            elif not(195 + 200 > mouse[0] > 195 and 500 + 100 > mouse [1] > 500) and inZone == True:
                inZone = False
                Display.addDarkRect()
                Display.addButtonText()

            #If you are in the button zone and you click and the door is closed, open the door
            if event.type == pygame.MOUSEBUTTONDOWN and Display.openState == False and \
               195 + 200 > mouse[0] > 195 and 500 + 100 > mouse [1] > 500:
                #asend("W0,0,1\n")
                Display.doorOpenState()
                Display.openState = True
                Display.addLightRect()
                Display.addButtonText()
            #If you are in the button zone and you click and the door is open, close the door
            elif event.type == pygame.MOUSEBUTTONDOWN and Display.openState == True  and \
                195 + 200 > mouse[0] > 195 and 500 + 100 > mouse [1] > 500:
                #asend("W0,0,0\n")
                Display.doorClosedState()
                Display.openState = False
                Display.addLightRect()
                Display.addButtonText()





    #quit gracefully
    pygame.quit()
    quit()
