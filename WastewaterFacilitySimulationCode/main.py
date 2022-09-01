import pygame
from pygame.locals import *
import time
import _thread
import Ybox
import math



"""
    Authors: Evan Plumley and Andrew Chaves

    This program is the comminication engine for the Y-box and the GUI
    for monitoring and powering the physical wastewater system. This engine
    controls the simulation of oxygen flow into the wastewater 
    treatment environement and displays the corresposnding
    sensor readings to the engineer interface. Control is done through 
    Ybox API via serial connection

    Controls: Allen-Bradley PowerFlex 40 AC variable frequency drive
              Allen-Bradley RSLogix 5000 system


"""

class WwtSim:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 1450, 850
        self.ybox = Ybox.Ybox()
        self.erase_width = 140
        self.erase_height = 35
        self.vfd_spin = True

        #Initialize Dissolved Oxygen and ORP and send to PLC
        DO=2.0
        ORP=-20

        #Convert ORP (-50 to +50 scale) to something the ybox can use (0-4095)
        ORP=ORP+150

        #Initial Valve Positions
        Aerobic_Valve=50
        Anaerobic_Valve=50
        
        #Scale for sending DO (Converts 0-4 and 0-100) to ybox values
        Scale_DO=math.ceil(4095/7)
        Scale_ORP=math.ceil(4095/700)
        Scale_Valves=math.ceil(4095/100)

        #Scales and casts as an int DO, ORP, and Valves
        Send_DO=int(DO*Scale_DO)
        Send_ORP=int(ORP*Scale_ORP)
        Send_Aerobic_Valve=Scale_Valves*Aerobic_Valve
        Send_Anaerobic_Valve=Scale_Valves*Anaerobic_Valve
        Fan_1=0
        Fan_2=0

        #Let it fly
        self.ybox.sendAnWrite(2,0,Send_DO)
        self.ybox.sendAnWrite(2,4,Send_ORP)
        self.ybox.sendAnWrite(2,2,Send_Aerobic_Valve)
        self.ybox.sendAnWrite(2,3,Send_Anaerobic_Valve)
        self.ybox.sendWrite(3,0,Fan_1)
        self.ybox.sendWrite(3,1,Fan_2)
        self.ybox.sendWrite(3,2,0)
        self.ybox.sendWrite(3,3,0)
        self.ybox.sendWrite(3,4,0)
        self.ybox.sendWrite(3,5,0)
        self.ybox.sendWrite(3,6,0)

        #What are we sending to the YBOX?
        print('DO_Initial:', Send_DO)
        print('\nORP_Initial:', Send_ORP)
        print('\nSend_Aerobic_Valve_Initial: ', Send_Aerobic_Valve)
        print('\nSend_Anaerobic_Valve_Initial: ', Send_Anaerobic_Valve)

        #Tell the infinite loop below what the intialized values are...(Set them as the starting values)
        self.Initial_DO=Send_DO
        self.Initial_ORP=Send_ORP
        Initial_Aerobic_Valve=Send_Aerobic_Valve
        Initial_Anaerobic_Valve=Send_Anaerobic_Valve

        #####################################################################################
        
        #Initialize screen
        print ("Waste Water Monitor Running")
        pygame.init()
        self.font = pygame.font.SysFont('Times', 25)
        self.font2 = pygame.font.SysFont('Times', 25)
        self.font3 = pygame.font.SysFont('Times', 35)
        self.font4 = pygame.font.SysFont('Times', 20)
        pygame.display.set_caption('Waste Water Treatment Monitor')
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill((white))
        self.screen.set_colorkey(white)
        self.fan_width = 300
        self.oxygen_content = 20

      
        #add PLC output title
        pygame.draw.rect(self.screen, black, (490, -5, 500, 55), 2)
        self.screen.blit(self.font3.render('Sensor Data Output' , True, (black)), (590, 5))

        #divider line and input title
        pygame.draw.line(self.screen, black, (0,630), (1450,630), 2)
        pygame.draw.rect(self.screen, black, (435, 630, 600, 50), 2)
        self.screen.blit(self.font3.render('PLC Output to Sensors' , True, (black)), (560, 635))

        #add the fans
        self.fan1cord = (25,150)
        self.fan2cord = (325,150)
   
        self.fan1 = pygame.image.load("wwtimages/fanBlade.jpg")
        self.fan2 = pygame.image.load("wwtimages/fanBlade.jpg")
   
        self.fan1.set_colorkey((0,0,0))
        self.fan2.set_colorkey((0,0,0))
        
        self.screen.blit(self.fan1, self.fan1cord)
        self.screen.blit(self.fan2, self.fan2cord)
       

        #add fan titles
        self.screen.blit(self.font.render('Oxygen Blower System' , True, (black)), (170, 95))
        
       

        #add rectangles for fan speed display and their descriptions
        self.screen.blit(self.font.render('VFD Hz' , True, (black)), (230, 390))
        pygame.draw.rect(self.screen, dark_grey, (210, 425, 150, 45), 5)
        self.screen.blit(self.font2.render('50' , True, (red)), (255, 435))
 
        #add the pipe valves
        self.pipe1cord = (700,140)
        self.pipe2cord = (1050,140)
        self.pipe1 = pygame.image.load("wwtimages/pipe.png")
        self.pipe2 = pygame.image.load("wwtimages/pipe.png")
        self.screen.blit(self.pipe1, self.pipe1cord)
        self.screen.blit(self.pipe2, self.pipe2cord)


        #add valve titles
        self.screen.blit(self.font.render('Disolved Oxygen Valve' , True, (black)), (705, 95))
        self.screen.blit(self.font.render('Oxygen Reduction Valve' , True, (black)), (1050, 95))

        #add rectangles and labels to display valve open percentage
        self.screen.blit(self.font.render('Percentage Open' , True, (black)), (740, 390))
        self.screen.blit(self.font.render('Percentage Open' , True, (black)), (1100, 390))
        pygame.draw.rect(self.screen, dark_grey, (750, 425, 150, 45), 5)
        pygame.draw.rect(self.screen, dark_grey, (1110, 425, 150, 45), 5)
        #self.screen.blit(self.font2.render('50' , True, (dark_blue)), (800, 435))
        #self.screen.blit(self.font2.render('100' , True, (dark_blue)), (1160, 435))

        #oxygen  content ORP display
        self.screen.blit(self.font4.render('Disolved Oxygen (mg/L):' , True, (black)), (680, 480))
        
        pygame.draw.rect(self.screen, red, (680, 510, 50, 75), 0)
        pygame.draw.rect(self.screen, green, (730, 510, 230, 75), 0)
        pygame.draw.rect(self.screen, red, (960, 510, 20, 75), 0)
        pygame.draw.rect(self.screen, black, (680, 510, 300, 75), 2)

        self.screen.blit(self.font4.render('Oxygen Reduction (mV):' , True, (black)), (1050, 480))
        
        pygame.draw.rect(self.screen, red, (1035, 510, 50, 75), 0)
        pygame.draw.rect(self.screen, green, (1085, 510, 230, 75), 0)
        pygame.draw.rect(self.screen, red, (1315, 510, 20, 75), 0)
        pygame.draw.rect(self.screen, black, (1035, 510, 300, 75), 2)


        ##############################################################################
        # Add the logical output
        ###############################################################################
        #add rectangles for fan speed display and their descriptions
        self.screen.blit(self.font.render('PLC Hz' , True, (black)), (230, 715))
        pygame.draw.rect(self.screen, dark_grey, (210, 745, 150, 45), 5)
        #self.screen.blit(self.font2.render('50' , True, (red)), (115, 755))
       

        #add rectangles and labels to display valve open percentage
        self.screen.blit(self.font.render('Percentage Open' , True, (black)), (740, 715))
        self.screen.blit(self.font.render('Percentage Open' , True, (black)), (1100, 715))
        pygame.draw.rect(self.screen, dark_grey, (750, 745, 150, 45), 5)
        pygame.draw.rect(self.screen, dark_grey, (1110, 745, 150, 45), 5)
        #self.screen.blit(self.font2.render('50' , True, (dark_blue)), (800, 755))
        #self.screen.blit(self.font2.render('100' , True, (dark_blue)), (1160, 755))

     
        pygame.display.update()
        
        try:
            _thread.start_new_thread(timedReads, (self,))
            _thread.start_new_thread(spinFans, (self,))
        except Exception as e:
           print(e)
        self._running = True

    #Handle all events
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        else: #Determine if button was clicked
            pygame.display.update()



    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
       
        
    #start program
    def on_execute(self):
        #if self.on_init() == False:
            #self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

def spinFans(self):

    rotationDegree1 = 2 #rotation degrees for each fan
    rotationDegree2 = 2
    past = int(round(time.time() * 1000)) #getting starting milisecond time to execute reads from the ybox
     
    while True:
       present = int(round(time.time() * 1000)) #getting present time to comapre to past
        #check to see if 100 milliseconds have  passed
       if present - past >= 40:
            past = present

        ########################
        #rotate the fans
        #############################

            rotationDegree1 = rotationDegree1 % 360 #rotation degree for fan 1
            rotationDegree2 = rotationDegree2 % 360 #rotation degree for fan 2

            ##conduct the actual movements
            if self.vfd_spin:
                newFan1 = rot_center(self.fan1, rotationDegree1)
                self.screen.blit(newFan1, self.fan1cord)
                newFan2 = rot_center(self.fan2, rotationDegree2)
                self.screen.blit(newFan2, self.fan2cord)
                rotationDegree1 = rotationDegree1 + 10 #move the dwgrees
                rotationDegree2 = rotationDegree2 + 10 #move the dwgrees
                pygame.display.update()
    

    
#method to monitor the PLC and chnage the display accordingly

def timedReads(self):
     white = (255, 255, 255)
     past = int(round(time.time() * 1000)) #getting starting milisecond time to execute reads from the ybox               
     rotationDegree1 = 2 #rotation degrees for each fan
     rotationDegree2 = 2
     #waterSize1 = 1
     #waterSize2 = 100
     oxyBarPos = 0
     reduction = 0
     
     while True:
        present = int(round(time.time() * 1000)) #getting present time to comapre to past
            #check to see if 100 milliseconds have  passed
        if present - past >= 100:
            past = present

            #Read the Setpoint for DO and ORP from PLC
            DO_Set_Point=(self.ybox.sendRead(0,0)*(1/(4095/7)))
            ORP_Set_Point=(self.ybox.sendRead(0,3)*(1/(4095/700)))

            #Read the output (%) of the PIDs controlling the VFD and Valves
            Valve_Aerobic_Percent_Output=self.ybox.sendRead(0,4) #valve percenatge
            Valve_Anaerobic_Percent_Output=self.ybox.sendRead(0,5)
            Frequency_Percent_Increase=self.ybox.sendRead(0,2)

            #Scale valves and VFD speed values to 0-100
            zero_to_hun_scale=100/4095
            Frequency_Scale=60/4095#100/4095
                
            #Use the Scale
            ##############################################
            #Display Frequecny sent to the VFP from the PLC
            ##############################################
            Frequency_Percent_Increase_Scaled=(Frequency_Percent_Increase*Frequency_Scale) #0-60
            print("PLC Freq\n", Frequency_Percent_Increase)
            pygame.draw.rect(self.screen, white, (215, 750, self.erase_width, self.erase_height), 0)
            self.screen.blit(self.font2.render("%.4f" % Frequency_Percent_Increase_Scaled , True, (red)), (235, 755)) #displays 0-60 scale
            
            ###################################
            #Display Aerobic Valve updates
            ##################################
            Valve_Aerobic_Percent_Output_Scaled=int(Valve_Aerobic_Percent_Output*zero_to_hun_scale) # Aerobic valve open percentage
            self.screen.blit(self.pipe1, self.pipe1cord)
            pygame.draw.circle(self.screen, blue, (830,265), Valve_Aerobic_Percent_Output_Scaled)
            pygame.draw.rect(self.screen, white, (753, 428, self.erase_width, self.erase_height), 0)
            self.screen.blit(self.font2.render(str(Valve_Aerobic_Percent_Output_Scaled) , True, (dark_blue)), (800, 435))
            pygame.display.update()
            
            ###################################
            #Display Anerobic Valve updates
            ##################################
            Valve_Anaerobic_Percent_Output_Scaled=int(Valve_Anaerobic_Percent_Output*zero_to_hun_scale)# =Anerobic valve open percetage
            self.screen.blit(self.pipe2, self.pipe2cord)
            pygame.draw.circle(self.screen, blue, (1177,265), Valve_Anaerobic_Percent_Output_Scaled)
            pygame.draw.rect(self.screen, white, (1115, 430, self.erase_width, self.erase_height), 0)
            self.screen.blit(self.font2.render(str(Valve_Anaerobic_Percent_Output_Scaled) , True, (dark_blue)), (1160, 435))

            #Print Valve positions and VFD speed
            #print('Aerobic Valve Percent: ', Valve_Aerobic_Percent_Output_Scaled)
            #print('\nAnaerobic Valve Percent: ', Valve_Anaerobic_Percent_Output_Scaled)
            #print('\nVFD Speed Percent: ', Frequency_Percent_Increase_Scaled)

            #Send the valve positions to the 3-10V meters and display to the GUI
            #Logical Output to valves
            ##########################################
            #Output to valves
            Aerobic_Valve_Scaled_Display=Valve_Aerobic_Percent_Output
            Anaerobic_Valve_Scaled_Display=Valve_Anaerobic_Percent_Output

            self.ybox.sendAnWrite(2,2,Aerobic_Valve_Scaled_Display)
            self.ybox.sendAnWrite(2,3,Anaerobic_Valve_Scaled_Display)

            #display the outputs to the meter
            Valve_Anaerobic_meter_display=int(Anaerobic_Valve_Scaled_Display*zero_to_hun_scale)# =Anerobic valve open percetage
            Valve_Aerobic_meter_display=int(Aerobic_Valve_Scaled_Display*zero_to_hun_scale)# =Anerobic valve open percetage
            pygame.draw.rect(self.screen, white, (760, 750, self.erase_width, self.erase_height), 0)
            pygame.draw.rect(self.screen, white, (1120, 750, self.erase_width, self.erase_height), 0)
            self.screen.blit(self.font2.render( str(Valve_Aerobic_meter_display), True, (dark_blue)), (800, 755)) #aerobic
            self.screen.blit(self.font2.render(str(Valve_Anaerobic_meter_display) , True, (dark_blue)), (1160, 755)) #anerobic
            
            pygame.display.update()

            ################Decrease DO AND ORP#################

            #Subtract percentage of valves from 100 and use that to determine how much to lower DO and ORP
            #The more anaerobic the water, the lower ORP and DO both are
            DO_Subtract=(101-Valve_Aerobic_Percent_Output_Scaled)
            ORP_Subtract=(101-Valve_Anaerobic_Percent_Output_Scaled)

            #Subtract the values and divide by two to make the change less agressive (helps the PIDs)
            DO_Update=int(self.Initial_DO-(DO_Subtract/8))
            ORP_Update=int(self.Initial_ORP-(ORP_Subtract/8))

            #Update the previous oxygen value so next time through the loop we are subtracting from the most recent correct value
            self.Initial_DO=DO_Update
            self.Initial_ORP=ORP_Update
                
            #Let it fly
            self.ybox.sendAnWrite(2,0,DO_Update)
            self.ybox.sendAnWrite(2,4,ORP_Update)
            


            ################INCREASE DO AND ORP#################
                
            #Increase DO and ORP if valves are opening according to equation
            Slope_Up_DO=.15
            Slope_Up_ORP=.15
               
            #Multiply the valve percentage by a slope, add this value to previous DO and ORP values
            DO_Update=self.Initial_DO+(Slope_Up_DO*Valve_Aerobic_Percent_Output_Scaled)
            ORP_Update=self.Initial_ORP+(Slope_Up_ORP*Valve_Anaerobic_Percent_Output_Scaled)
                
            #Update the previous DO and ORP values so next time through the loop we are adding to the correct value
            self.Initial_DO=DO_Update
            self.Initial_ORP=ORP_Update

            #Cast as an integer for the YBOX's sake
            DO_Update=int(DO_Update)
            ORP_Update=int(ORP_Update)

                
            #Show what is being sent                                     
            print('\nDO_Update: ', DO_Update)
            print('\nORP Update: ', ORP_Update)

            #let DO and ORP fly
            self.ybox.sendAnWrite(2,0,DO_Update)
            self.ybox.sendAnWrite(2,4,ORP_Update)
            pygame.display.update()


            #################################
            # add and update oxygen level bar
            #################################
            #oxyBarPos = oxyBarPos % 300
            #oxyContent = oxyBarPos / 75 # this is between 0 and 4
            #reduction = (oxyBarPos / 3) - 50 # reduction is between -50 and 50

            #disolved oxygen
            pygame.draw.rect(self.screen, white, (910, 480, 80, 30), 0)
            if (DO_Update / (4095/7)) > 1 and (DO_Update / (4095/7)) < 5.5:
                self.screen.blit(self.font.render("%.4f" % (DO_Update / (4095/7)) , True, (dark_green)), (910, 480))
            else:
                self.screen.blit(self.font.render("%.4f" % (DO_Update / (4095/7)) , True, (red)), (910, 480))
            oxyBarPos = (DO_Update / (4095/7)) * 42.85
            pygame.draw.rect(self.screen, red, (680, 510, 40, 75), 0)
            pygame.draw.rect(self.screen, green, (720, 510, 180, 75), 0)
            pygame.draw.rect(self.screen, red, (915, 510, 45, 75), 0)
            pygame.draw.rect(self.screen, black, (680, 510, 300, 75), 2)
            if oxyBarPos >= 0 and oxyBarPos <= 300:
                pygame.draw.line(self.screen, black, (oxyBarPos + 680,510), (oxyBarPos + 680, 510+75), 6)
            pygame.display.update()

            #oxygen reduction
            pygame.draw.rect(self.screen, white, (1270, 480, 120, 30), 0)
            if ((ORP_Update / (4095/700)) - 150) > -30 and ((ORP_Update / (4095/700)) - 150) < 450:
                self.screen.blit(self.font.render("%.4f" % ((ORP_Update / (4095/700)) - 150) , True, (dark_green)), (1270, 480))
            else:
                self.screen.blit(self.font.render("%.4f" % ((ORP_Update / (4095/700)) - 150) , True, (red)), (1270, 480))
            orpOxyBarPos = (ORP_Update / (4095/700)) * .43
            pygame.draw.rect(self.screen, red, (1035, 510, 50, 75), 0)
            pygame.draw.rect(self.screen, green, (1085, 510, 210, 75), 0)
            pygame.draw.rect(self.screen, red, (1295, 510, 40, 75), 0)
            pygame.draw.rect(self.screen, black, (1035, 510, 300, 75), 2)
            if orpOxyBarPos >= 0 and orpOxyBarPos <= 300:
                pygame.draw.line(self.screen, black, (orpOxyBarPos + 1035,510), (orpOxyBarPos + 1035, 510+75), 6)
            pygame.display.update()


            ##############GET TOTAL VALVE POSITION ##################
            #Get the total valve position (0-200): (Anaerobic (100) + Aerobic (100) = 200 Total)
            Total_Valve_Position=int(Valve_Aerobic_Percent_Output+Valve_Anaerobic_Percent_Output)
            Total_Valve_Scale=200/4095

            #Print the Total Valve Position
            print('\nTotal_valve: ', Total_Valve_Position*Total_Valve_Scale)

            #Let the Total Valve position fly
            self.ybox.sendAnWrite(2,5,Total_Valve_Position)

            ##############GET VFD TRUE SPEED ##################
            #Get the VFD's direct output from the Ybox for its speed NOTE: the VFD must be running!!!!, not just on!!!
            True_Frequency=self.ybox.sendRead(0,6)

            print("True Frequency Raw", True_Frequency)

            #Convert the signal to 0-60 hertz
            True_Frequency_Scaled=True_Frequency*(60/4095)

            if True_Frequency_Scaled < 5:
                self.vfd_spin = False
            else:
                self.vfd_spin = True

            ###############################
            # Display true frequency to gui
            ###########################
            pygame.draw.rect(self.screen, white, (215, 430, self.erase_width, self.erase_height), 0)
            self.screen.blit(self.font2.render("%.4f" % True_Frequency_Scaled , True, (red)), (255, 435))
            pygame.display.update()
                
            #Print the true VFD frequency
            print('\nTrue VFD Frequency: ', True_Frequency_Scaled)

            #Start fans if the VFD is runnning
            if True_Frequency_Scaled > 5:
                self.ybox.sendWrite(3,0,1)
                self.ybox.sendWrite(3,1,1)
            else:
                self.ybox.sendWrite(3,0,0)
                self.ybox.sendWrite(3,1,0)
                

            #Print divider for next time through loop
            print('######################################\n')

            #########Obtain Alarms, check alarms, send to light if necessary######
            DO_High=self.ybox.sendRead(1,0)
            if DO_High==1:
                self.ybox.sendWrite(3,4,1)
            else:
                self.ybox.sendWrite(3,4,0)

            DO_Low=self.ybox.sendRead(1,1)
            if DO_Low==1:
                self.ybox.sendWrite(3,5,1)
            else:
                self.ybox.sendWrite(3,5,0)

                        
            ORP_High=self.ybox.sendRead(1,5)
            if ORP_High==1:
                self.ybox.sendWrite(3,2,1)
            else:
                self.ybox.sendWrite(3,2,0)

                        
            ORP_Low=self.ybox.sendRead(1,3)
            if ORP_Low==1:
                self.ybox.sendWrite(3,3,1)
            else:
                self.ybox.sendWrite(3,3,0)

                        
            Pressure_High=self.ybox.sendRead(1,4)
            if Pressure_High==1:
                self.ybox.sendWrite(3,6,1)
            else:
                self.ybox.sendWrite(3,6,0)


            pygame.display.update()


            
            
            
            

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    rot_image = rot_image.convert()
    return rot_image


if __name__ == "__main__" :

    red = (225,0,0)
    white = (255, 255, 255)
    black = (0,0,0)
    grey = (200, 200, 200)
    dark_grey = (140, 140, 140)
    blue = (130, 130, 255)
    dark_blue = (0, 0, 150)
    green = (0,240,0)
    dark_green = (0,175,0)

    wwtSim = WwtSim()
    wwtSim.on_execute()

   
