import pygame
from pygame.locals import *
import guard_station
import prison_cell
import time
import _thread
import Ybox
import mantrap
import indicator

"""
 Authors: Evan Plumley

 Runs the prison cell simulation and interface displaying the value
 of the PLC outputs and providing the PLC inputs. Pygame is the
 engine to display and control the interface

"""

class PrisonSim:
    """ 
        The PrisonSim class contains the screen display and threaded execution of all events
    """
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 1400, 950
        self.ybox = Ybox.Ybox()
        self.buttonclick1 = False
        self.buttonclick2 = False
        self.buttonclick3 = False
        self.buttonclick4 = False
        self.buttonclick5 = False
        self.buttontoggle1 = False
        self.buttontoggle2 = False
        self.buttontoggle3 = False
        self.buttontoggle4 = False
        self.buttontoggle5 = False

    def on_init(self):
        """
            Initializes the interface screen and adds the images for display
        """
        pygame.init()
        self.font = pygame.font.SysFont('Times', 25)
        pygame.display.set_caption('Ybox Simulation')
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill((black))

        x_padding = 42.5
        y_padding = 95

        cell_panel_width = 325
        cell_panel_height = 300

        #create the guard station panel with number of cells
        self.guard_station_panel = guard_station.GuardStation(self, 5, 50, 575)

        
        #create each cell at given location
        cell_one_panel = prison_cell.PrisonCell(self, 1, x_padding, y_padding)
        cell_two_panel = prison_cell.PrisonCell(self, 2, 5*x_padding+cell_panel_width, y_padding)
        cell_three_panel = prison_cell.PrisonCell(self, 3, 9*x_padding+2*cell_panel_width, y_padding)

        #add all cells to list
        self.cell_door_panels = [cell_one_panel, cell_two_panel, cell_three_panel]

        #add mantrap display
        self.mantrap = mantrap.ManTrap(self, 3*x_padding+2*cell_panel_width, (2.2 * y_padding) + cell_panel_height)

        #add the title of the program
        main_title_dimensions = ((615, 70))
        main_title_icon = pygame.image.load ("images/title.png")
        main_title_icon2 = pygame.image.load ("images/title.png")
        main_title_icons = [main_title_icon, main_title_icon2]
        main_title = indicator.Indicator(self, 390, 10, main_title_icons , main_title_dimensions)

        # set the inital states
        self.ybox.sendWrite(0,9,1) #panel enabled
        
        self.ybox.sendWrite(0,0,1) #light indicators green
        self.ybox.sendWrite(0,2,1)
        self.ybox.sendWrite(0,4,1)

        self.ybox.sendWrite(0,10,1)
        self.ybox.sendWrite(0,11,1)

        pygame.display.update()
        try:
           _thread.start_new_thread(timedReads, (self,))
        except Exception as e:
           print(e)
        self._running = True

    
    def on_event(self, event):
        """
            Handles all click events and calls the corresponding button execution
        """
        if event.type == pygame.QUIT:
            self._running = False
        else: #Determine if button was clicked
            for i, cell_btn in enumerate(self.guard_station_panel.cell_btns):
                if 'click' in cell_btn.handleEvent(event):
                    try:
                        clickButton(self,i)
                    except Exception as e:
                        print(e)
                    
            for i, cell in enumerate(self.cell_door_panels):
                if 'click' in cell.key_btn.handleEvent(event):
                    try:
                        openDoor(self,i)
                    except Exception as e:
                        print(e)

            if 'click' in self.guard_station_panel.disable_btn.handleEvent(event):
                self.guard_station_panel.disable_clicked = True

            pygame.display.update()



    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
       
        
    def on_execute(self):
        """
            Begins execution loop by calling the execution of the object 
        """
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

def clickButton(self, i):
    """ 
       Activates button press action
    """
    #door one button
    if i == 0 and self.buttonclick1 == False:
        self.buttonclick1 = True
        self.buttontoggle1 = True
    elif i == 0 and self.buttonclick1 == True:
        self.buttonclick1 = False
        self.buttontoggle1 = True

    #door two button
    elif i == 1 and self.buttonclick2 == False:
        self.buttonclick2 = True
        self.buttontoggle2 = True
    elif i == 1 and self.buttonclick2 == True:
        self.buttonclick2 = False
        self.buttontoggle2 = True

    #door three button
    elif i == 2 and self.buttonclick3 == False:
        self.buttonclick3 = True
        self.buttontoggle3 = True
    elif i == 2 and self.buttonclick3 == True:
        self.buttonclick3 = False
        self.buttontoggle3 = True
        
    #door four button
    elif i == 3 and self.buttonclick4 == False:
        self.buttonclick4 = True
        self.buttontoggle4 = True
    elif i == 3 and self.buttonclick4 == True:
        self.buttonclick4 = False
        self.buttontoggle4 = True

    #door five button  
    elif i == 4 and self.buttonclick5 == False:
        self.buttonclick5 = True
        self.buttontoggle5 = True
    elif i == 4 and self.buttonclick5 == True:
        self.buttonclick5 = False
        self.buttontoggle5 = True
        
    else:
        print("Something went wrong in the lock reads")

        
def openDoor(self, i):
    """
        Opens door via the manual key button simulating physical override
    """
    if self.cell_door_panels[i].doorClosed == True:
        self.cell_door_panels[i].cell_door.change_state()
        self.cell_door_panels[i].doorClosed = False
        
    elif self.cell_door_panels[i].doorClosed == False:
        self.cell_door_panels[i].cell_door.change_state()
        self.cell_door_panels[i].doorClosed = True

def timedReads(self):
    """ Monitors the PLC and changes the dispaly accordingly
    """
    past = int(round(time.time() * 1000)) #getting starting milisecond time to execute reads from the ybox
    while True:
        present = int(round(time.time() * 1000)) #getting present time to comapre to past
            #check to see if 100 milliseconds have  passed
        if present - past >= 100:
            past = present
            #########################################
            #set button click values and write accordingly
            ##################################################
            if self.buttonclick1 == True and self.buttontoggle1 == True:
                self.ybox.sendWrite(0,1,1)
                self.buttontoggle1 = False
            elif self.buttonclick1 == False and self.buttontoggle1 == True:
                self.ybox.sendWrite(0,1,0)
                self.buttontoggle1 = False
               
            if self.buttonclick2 == True and self.buttontoggle2 == True:
                self.ybox.sendWrite(0,3,1)
                self.buttontoggle2 = False
            elif self.buttonclick2 == False and self.buttontoggle2 == True:
                self.ybox.sendWrite(0,3,0)
                self.buttontoggle2 = False
                
            if self.buttonclick3 == True and self.buttontoggle3 == True:
                self.ybox.sendWrite(0,5,1)
                self.buttontoggle3 = False
            elif self.buttonclick3 == False and self.buttontoggle3 == True:
                self.ybox.sendWrite(0,5,0)
                self.buttontoggle3 = False
                
            if self.buttonclick4 == True and self.buttontoggle4 == True:
                self.ybox.sendWrite(0,7,1)
                self.buttontoggle4 = False
            elif self.buttonclick4 == False and self.buttontoggle4 == True:
                self.ybox.sendWrite(0,7,0)
                self.buttontoggle4 = False

            if self.buttonclick5 == True and self.buttontoggle5 == True:
                self.ybox.sendWrite(0,8,1)
                self.buttontoggle5 = False
            elif self.buttonclick5 == False and self.buttontoggle5 == True:
                self.ybox.sendWrite(0,8,0)
                self.buttontoggle5 = False

            #################################################
            #read the lock value for all doors from the PLC and then react
            ##############################################
            for i in range(0, len(self.cell_door_panels)):
                #aqcuiring the actual channel number
                if i == 0:
                    readnum = 0
                elif i == 1: 
                    readnum = 3
                elif i == 2:
                    readnum = 6
                else:
                    print("Something went wrong in the lock reads")

                

                resp = self.ybox.sendRead(1, readnum)
                readnum = str(readnum)
                if resp == ("r1," + readnum + ",1") and self.cell_door_panels[i].lockClosed == True: #checks for a lock state change
                    self.cell_door_panels[i].lock_indicator.change_state() #open lock
                    self.cell_door_panels[i].lockClosed = False #lock open state flag
                    #make sure I dont unecesariily change the state due to the manual key
                    if self.cell_door_panels[i].doorClosed == True:
                        self.cell_door_panels[i].cell_door.change_state()
                        self.cell_door_panels[i].doorClosed = False 
                    pygame.display.update()

     
                elif resp == ("r1,"+ readnum +",0") and self.cell_door_panels[i].lockClosed == False:
                    self.cell_door_panels[i].lock_indicator.change_state() #open lock
                    self.cell_door_panels[i].lockClosed = True #lock open state flag
                    #make sure I dont unecesariily change the state due to the manual key
                    if self.cell_door_panels[i].doorClosed == False: 
                         self.cell_door_panels[i].cell_door.change_state()
                         self.cell_door_panels[i].doorClosed = True
                    pygame.display.update()

            #Checking for chnages for the indicator light
            for i in range(0, len(self.cell_door_panels)):
                #mapping to secure lights for the plc
                if i == 0:
                    writenum = 0
                elif i == 1: 
                    writenum = 2
                elif i == 2:
                    writenum = 4
                    
                if (self.cell_door_panels[i].doorClosed == False or self.cell_door_panels[i].lockClosed == False) and self.cell_door_panels[i].indicatorLight == True:
                    self.cell_door_panels[i].cell_door_indicator.change_state()#change to red
                    self.cell_door_panels[i].indicatorLight = False
                    self.ybox.sendWrite(0,writenum,0) # turn the PLC light
                    pygame.display.update()

                elif (self.cell_door_panels[i].doorClosed == True and self.cell_door_panels[i].lockClosed == True) and self.cell_door_panels[i].indicatorLight == False:
                    self.cell_door_panels[i].cell_door_indicator.change_state()#change to green
                    self.cell_door_panels[i].indicatorLight = True
                    self.ybox.sendWrite(0,writenum,1) # turn the PLC light
                    pygame.display.update()

    
            #########################################
            # read prison guard button statuses just for cell doors and mantrap
            #########################################
            for i in range(0, len(self.guard_station_panel.button_pushed)):
                #aqcuiring the actual channel number
                if i == 0:
                    readnum = 1
                    writenum = 1
                elif i == 1:
                    readnum = 4
                    writenum = 3
                elif i == 2:
                    readnum = 7
                    writenum = 5 
                elif i == 3:
                    readnum = 10
                    writenum = 7
                elif i == 4:
                    readnum = 12
                    writenum = 8
                else:
                    print("Something went wrong in the button reads")
              
                resp2 = self.ybox.sendRead(1, readnum)
                readnum = str(readnum)
               
                if resp2 == ("r1,"+ readnum +",1") and self.guard_station_panel.button_pushed[i] == False:
                    self.guard_station_panel.btn_statuses[i].change_state()
                    self.guard_station_panel.button_pushed[i] = True
                    self.ybox.sendWrite(0,writenum,1)
                    pygame.display.update()
                elif resp2 == ("r1,"+ readnum + ",0") and self.guard_station_panel.button_pushed[i] == True:
                    self.guard_station_panel.btn_statuses[i].change_state()
                    self.guard_station_panel.button_pushed[i] = False
                    self.ybox.sendWrite(0,writenum,0)
                    pygame.display.update()



            ###############################################
            #Read guard station light statuses
            ################################################
            for i in range(0, len(self.guard_station_panel.lights)):
                #aqcuiring the actual channel number
                if i == 0:
                    readnum = 2
                elif i == 1:
                    readnum = 5
                elif i == 2:
                    readnum = 8
                elif i == 3:
                    readnum = 13
                else:
                    print("Something went wrong in the button reads")

               

                resp3 = self.ybox.sendRead(1, readnum)
                readnum = str(readnum)
                if resp3 == ("r1,"+ readnum +",1") and self.guard_station_panel.light_green[i] == False:
                    self.guard_station_panel.lights[i].change_state()
                    self.guard_station_panel.light_green[i] = True
                    pygame.display.update()

                elif resp3 == ("r1,"+ readnum +",0") and self.guard_station_panel.light_green[i] == True:
                    self.guard_station_panel.lights[i].change_state()
                    self.guard_station_panel.light_green[i] = False
                    pygame.display.update()

            ############################################
            # Read the locks for the man trap and react appropriatley
            ############################################

            #lock reads for trap door one
            ##############################
            readnum = 9
            writenum = 10
            readnum_2 = 11
            writenum_2 = 11
            resp4 = self.ybox.sendRead(1, readnum)
            resp5 = self.ybox.sendRead(1, readnum_2)
            readnum = str(readnum)
            readnum_2 = str(readnum_2)
            #all reads done for both above
            
            if resp4 == ("r1," + readnum + ",1") and self.mantrap.lock1Closed == True: #checks for a lock state change
                self.mantrap.lock_indicator1.change_state() #open lock
                self.mantrap.lock1Closed = False #lock open state flag
                self.mantrap.trap_door1.change_state()
                self.mantrap.door1Closed = False
                self.ybox.sendWrite(0,writenum,0) # trap door  in unsecure
                if self.mantrap.indicatorLight == True:
                    self.mantrap.indicatorLight = False
                    self.mantrap.secure_indicator.change_state()
                pygame.display.update()

            elif resp4 == ("r1," + readnum + ",0") and self.mantrap.lock1Closed == False: #checks for a lock state change
                self.mantrap.lock_indicator1.change_state() #open lock
                self.mantrap.lock1Closed = True #lock open state flag
                self.mantrap.trap_door1.change_state()
                self.mantrap.door1Closed = True
                self.ybox.sendWrite(0,writenum,1) # trap door  in unsecure
                if resp5 == "r1,11,0" and self.mantrap.indicatorLight == False:
                    self.mantrap.indicatorLight = True
                    self.mantrap.secure_indicator.change_state()
                pygame.display.update()

            #lock reads for trap door 2
            ##############################
         
         
            if resp5 == ("r1," + readnum_2 + ",1") and self.mantrap.lock2Closed == True: #checks for a lock state change
                self.mantrap.lock_indicator2.change_state() #open lock
                self.mantrap.lock2Closed = False #lock open state flag
                self.mantrap.trap_door2.change_state()
                self.mantrap.door2Closed = False
                self.ybox.sendWrite(0,writenum_2,0) # trap door  in unsecure
                if self.mantrap.indicatorLight == True:
                    self.mantrap.indicatorLight = False
                    self.mantrap.secure_indicator.change_state()
                pygame.display.update()

            elif resp5 == ("r1," + readnum_2 + ",0") and self.mantrap.lock2Closed == False: #checks for a lock state change
                self.mantrap.lock_indicator2.change_state() #open lock
                self.mantrap.lock2Closed = True #lock open state flag
                self.mantrap.trap_door2.change_state()
                self.mantrap.door2Closed = True
                self.ybox.sendWrite(0,writenum_2,1) # trap door  secure
                if resp4 == "r1,9,0" and self.mantrap.indicatorLight == False:
                    self.mantrap.indicatorLight = True
                    self.mantrap.secure_indicator.change_state()
                pygame.display.update()

          

            
            #read the key and execute only if the key holds the power to do so
            resp6 = self.ybox.sendRead(1, 14)
            if resp6 == ("r1,14,1") and self.guard_station_panel.panel_enabled == False and self.guard_station_panel.panel_keyControl == True:
                self.ybox.sendWrite(0,9,1)
                self.guard_station_panel.enablePanel()
                pygame.display.update()
            if resp6 == ("r1,14,0") and self.guard_station_panel.panel_enabled == True and self.guard_station_panel.panel_keyControl == True:
                self.ybox.sendWrite(0,9,0)
                self.guard_station_panel.disablePanel()
                pygame.display.update()

            #read the simulation disable buttton and take control power form the key
            if self.guard_station_panel.disable_clicked == True and self.guard_station_panel.panel_enabled == False:
                self.guard_station_panel.panel_keyControl = False
                self.guard_station_panel.disable_clicked = False
                self.ybox.sendWrite(0,9,1)
                self.guard_station_panel.enablePanel()
                pygame.display.update()

            if self.guard_station_panel.disable_clicked == True and self.guard_station_panel.panel_enabled == True:
                self.guard_station_panel.panel_keyControl = False
                self.guard_station_panel.disable_clicked = False
                self.ybox.sendWrite(0,9,0)
                self.guard_station_panel.disablePanel()
                pygame.display.update()

            #return control power to the key if the sim and key match
            if self.guard_station_panel.panel_keyControl == False and resp6 == ("r1,14,1") and self.guard_station_panel.panel_enabled == True:
                self.guard_station_panel.panel_keyControl = True

            if self.guard_station_panel.panel_keyControl == False and resp6 == ("r1,14,0") and self.guard_station_panel.panel_enabled == False:
                self.guard_station_panel.panel_keyControl = True
                


            


if __name__ == "__main__" :
    """Creates the PrisonSim object and begins execution
    """
    
    #Color presets
    green = (200,0,0)
    white = (255, 255, 255)
    black = (0,0,0)
    grey = (200, 200, 200)
    dark_grey = (140, 140, 140)
    light_blue = (0, 0, 255)
    dark_blue = (0, 0, 150)

    prisonSim = PrisonSim()
    prisonSim.on_execute()
