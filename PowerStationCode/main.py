import pygame
from pygame.locals import *
import time
import _thread
import Ybox
import math
import indicator
import pygbutton



"""
# Author: Evan Plumley 
#
# This program is the comminication engine for the Y-box and the GUI
# for monitoring and controlliong the power substation
#
#
"""

class PsSim:
    """ The primary simlution object that controls the interface and
        displays corresponding images
    """
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 1350, 970
        self.ybox = Ybox.Ybox()
        self.prisonPower = True
        self.waterPower = True
        self.homePower = True
        self.meterAlarm1Trip = False
        self.meterAlarm2Trip = False
        self.line1amps = 31.1000
        self.line2amps = 31.1000
        self.clickhigh1 = False
        self.clickhigh2 = False
        self.clickmid1 = False
        self.clickmid2 = False
        self.clicklow1 = False
        self.clicklow2 = False
        self.clickzero1 = False
        self.clickzero2 = False
        

        startAmp = 400

        #send original mA to the meters
        self.ybox.sendWrite(0,2,startAmp) # write meter 1
        self.ybox.sendWrite(0,3,1500)
        
        self.ybox.sendWrite(0,1,startAmp) # 2
        self.ybox.sendWrite(0,4,1500)
        


        #line trips at 40 resets at 35
        #nuetral trips at 90 and resets at 85
        
        #Initialize screen
        print ("here")
        pygame.init()
        self.font = pygame.font.SysFont('Times', 25)
        self.font2 = pygame.font.SysFont('Times', 45)
        self.font3 = pygame.font.SysFont('Times', 35)
        self.font4 = pygame.font.SysFont('Times', 15)
        pygame.display.set_caption('Power Substation Monitor')
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill((white))
        self.screen.set_colorkey(white)

        #add the pygbuttons
        btn_height = 35
        btn1x = 275
        btn2x = 450
        btn3x = 625

        self.screen.blit(self.font4.render('Line 1 trips at 40 resets at 35.' , True, (black)), (270, 900))
        self.screen.blit(self.font4.render('Nuetral (Line 2) trips at 90 and resets at 85' , True, (black)), (270, 920))

        self.screen.blit(self.font4.render('Line 1 Amp Control' , True, (black)), (270, 650))
        self.screen.blit(self.font4.render('Line 2 Amp Control' , True, (black)), (450, 650))
        
        self.line1high_btn = pygbutton.PygButton(( btn1x, 700, 125, btn_height), "High: 50")
        self.line2high_btn = pygbutton.PygButton(( btn2x, 700, 125, btn_height), "High: 50")
       

        self.line1mid_btn = pygbutton.PygButton(( btn1x, 750, 125, btn_height), "Mid: 31.1")
        self.line2mid_btn = pygbutton.PygButton(( btn2x, 750, 125, btn_height), "Mid: 31.1")
       

        self.line1low_btn = pygbutton.PygButton(( btn1x, 800, 125, btn_height), "Low: 8.1")
        self.line2low_btn = pygbutton.PygButton(( btn2x, 800, 125, btn_height), "Low: 8.1")
       

        self.line1zero_btn = pygbutton.PygButton(( btn1x, 850, 125, btn_height), "Zero")
        self.line2zero_btn = pygbutton.PygButton(( btn2x, 850, 125, btn_height), "Zero")
       

        self.line1high_btn.draw(self.screen)
        self.line2high_btn.draw(self.screen)
        

        self.line1mid_btn.draw(self.screen)
        self.line2mid_btn.draw(self.screen)
        

        self.line1low_btn.draw(self.screen)
        self.line2low_btn.draw(self.screen)
        

        self.line1zero_btn.draw(self.screen)
        self.line2zero_btn.draw(self.screen)
       
     

      
        #add PLC output title
        pygame.draw.rect(self.screen, black, (450, -5, 500, 55), 2)
        self.screen.blit(self.font3.render('Power Meter and Relay Output' , True, (black)), (480, 5))


    
        #add the meter
        self.meterpos = (300,150)
        self.meter = pygame.image.load("psimages/meter.png")
        self.screen.blit(self.meter, self.meterpos)
        pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)

        #add the relay
        self.relaypos = (800, 100)
        self.relay = pygame.image.load("psimages/relay.jpg")
        self.screen.blit(self.relay, self.relaypos)
        pygame.draw.rect(self.screen, light_green, (916, 237, 280, 65), 0)
        #self.rice = pygame.image.load("psimages/rice.jpg")
        #self.screen.blit(self.rice, (1030,239))

        #add raiden and electricity
        self.raidenpos = (35, 320)
        self.raidenboltpos = (151, 330)
        #self.raiden = pygame.image.load("psimages/pikachu.png")
        self.raiden = pygame.image.load("psimages/raiden.png")
        self.screen.blit(self.raiden, self.raidenpos)
        self.raidenbolt = pygame.image.load("psimages/raidenpower.png")
        self.screen.blit(self.raidenbolt, self.raidenboltpos)
        self.power1 = pygame.image.load("psimages/power.png")
        self.power2 = pygame.image.load("psimages/power.png")
        self.power3 = pygame.image.load("psimages/power.png")
        self.power1pos = (720, 300)
        self.power2pos = (720, 340)
        self.power3pos = (720, 380)
        self.screen.blit(self.power1, self.power1pos)
        self.screen.blit(self.power2, self.power2pos)
        self.screen.blit(self.power3, self.power3pos)
        

        #add indicator lights for power at idividual stations
        green_icon = pygame.image.load("psimages/greenLightAlt.png")
        red_icon = pygame.image.load("psimages/redLightAlt.png")
        light_icons = [green_icon, red_icon]
        light_dimensions = ((100,100))
        self.light1 = indicator.Indicator(self, 850, 800, light_icons, light_dimensions)
        self.light2 = indicator.Indicator(self, 1020, 800, light_icons, light_dimensions)
        self.light3 = indicator.Indicator(self, 1190, 800, light_icons, light_dimensions)

        self.screen.blit(self.font3.render("Prison", True, (black)), (860, 900))
        self.screen.blit(self.font3.render("Water", True, (black)), (1030, 900))
        self.screen.blit(self.font3.render("Home", True, (black)), (1200, 900))

        lightning = pygame.image.load("psimages/lightning.png")
        cover = pygame.image.load("psimages/whiteCover.png")
        lightning_icons = [lightning, cover]
        lightning_dimensions = ((40,100))
        
        self.lightning1 = indicator.Indicator(self, 875, 700, lightning_icons, lightning_dimensions)
        self.lightning2 = indicator.Indicator(self, 1045, 700, lightning_icons, lightning_dimensions)
        self.lightning3 = indicator.Indicator(self, 1210, 700, lightning_icons, lightning_dimensions)

        #################################
        # add the amps to the meter
        #################################
        pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
        self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
        self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
        self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
   
    
        self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300))
        self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
      
            
        pygame.display.update()


    
     
        
        
        try:
            _thread.start_new_thread(timedReads, (self,))
        except Exception as e:
           print(e)
        self._running = True

    #Handle all events
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        else: #Determine if button was clicked
            if 'click' in self.line1high_btn.handleEvent(event):
                self.clickhigh1 = True
            if 'click' in self.line2high_btn.handleEvent(event):
                self.clickhigh2 = True
                
            if 'click' in self.line1mid_btn.handleEvent(event):
                self.clickmid1 = True
            if 'click' in self.line2mid_btn.handleEvent(event):
                self.clickmid2 = True
                
            if 'click' in self.line1low_btn.handleEvent(event):
                self.clicklow1 = True
            if 'click' in self.line2low_btn.handleEvent(event):
                self.clicklow2 = True

            if 'click' in self.line1zero_btn.handleEvent(event):
                self.clickzero1 = True
            if 'click' in self.line2zero_btn.handleEvent(event):
                self.clickzero2 = True
                
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






def timedReads(self):
     past = int(round(time.time() * 1000)) #getting starting milisecond time to execute reads from the ybox               
     meter_current = 13.0001
     
     
     while True:
        present = int(round(time.time() * 1000)) #getting present time to comapre to past
            #check to see if 100 milliseconds have  passed
        if present - past >= 40:
            past = present
    

            ####################################
            # read the SEL power state and display
            ###################################
            prisonState = self.ybox.sendRead(1,4)
            waterState = self.ybox.sendRead(1,5)
            homeState = self.ybox.sendRead(1,6)

            
            #Prison change display
            if self.prisonPower == True and prisonState == ("r1,4,1"):
                self.prisonPower = False
                self.light1.change_state()
                self.lightning1.change_state()
                self.ybox.sendWrite(2,0,1)

            if self.prisonPower == False and prisonState == ("r1,4,0"):
                self.prisonPower = True
                self.light1.change_state()
                self.lightning1.change_state()
                self.ybox.sendWrite(2,0,0)
                
            #Water change display
            if self.waterPower == True and waterState == ("r1,5,1"):
                self.waterPower = False
                self.light2.change_state()
                self.lightning2.change_state()
                self.ybox.sendWrite(2,1,1)

            if self.waterPower == False and waterState == ("r1,5,0"):
                self.waterPower = True
                self.light2.change_state()
                self.lightning2.change_state()
                self.ybox.sendWrite(2,1,0)

            
            #Home change display
            if self.homePower == True and homeState == ("r1,6,1"):
                print(homeState)
                self.homePower = False
                self.light3.change_state()
                self.lightning3.change_state()
                self.ybox.sendWrite(2,2,1)

            if self.homePower == False and homeState == ("r1,6,0"):
                self.homePower = True
                self.light3.change_state()
                self.lightning3.change_state()
                self.ybox.sendWrite(2,2,0)



            ######################################################
            # Read state of the meter alarm to foward to the relay
            ######################################################
            meterAlarm1 = self.ybox.sendRead(1,1)
            meterAlarm2 = self.ybox.sendRead(1,2)



            if meterAlarm1 == ("r1,1,1"):# and self.meterAlarm1Trip == False:
                self.meterAlarm1Trip == True
                self.ybox.sendWrite(2,4,1)

            if meterAlarm1 == ("r1,1,0"):# and self.meterAlarm1Trip == True:
                self.meterAlarm1Trip == False
                self.ybox.sendWrite(2,4,0)


            if meterAlarm2 == ("r1,2,1"):# and self.meterAlarm2Trip == False:
                self.meterAlarm2Trip == True
                self.ybox.sendWrite(2,5,1)

            if meterAlarm2 == ("r1,2,0"): #and self.meterAlarm2Trip == True:
                self.meterAlarm2Trip == False
                self.ybox.sendWrite(2,5,0)


            pygame.display.update()


            if self.clickhigh1 == True:
                self.clickhigh1 = False
                self.line1amps = 50.00
                self.ybox.sendWrite(0,2,700) # write meter 1
                self.ybox.sendWrite(0,3,4000)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
               
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
                
                
                
            if self.clickhigh2 == True:
                self.clickhigh2 = False
                self.line2amps = 50.00
                self.ybox.sendWrite(0,1,700) # write meter 1
                self.ybox.sendWrite(0,4,4000)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
               
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
             


            if self.clickmid1 == True:
                self.clickmid1 = False
                self.line1amps = 31.10
                self.ybox.sendWrite(0,2,400) # write meter 1
                self.ybox.sendWrite(0,3,3000)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
                
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
                
                

            if self.clickmid2 == True:
                self.clickmid2 = False
                self.line2amps = 31.10
                self.ybox.sendWrite(0,1,400) # write meter 1
                self.ybox.sendWrite(0,4,3000)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
            
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
               
          

            if self.clicklow1 == True:
                self.clicklow1 = False
                self.line1amps = 8.10
                self.ybox.sendWrite(0,2,100) # write meter 1
                self.ybox.sendWrite(0,3,1500)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
                
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
                
            if self.clicklow2 == True:
                self.clicklow2 = False
                self.line2amps = 8.10
                self.ybox.sendWrite(0,1,100) # write meter 1
                self.ybox.sendWrite(0,4,1500)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
                
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
          

            if self.clickzero1 == True:
                self.clickzero1 = False
                self.line1amps = 0
                self.ybox.sendWrite(0,2,0) # write meter 1
                self.ybox.sendWrite(0,3,0)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
                
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
                
            if self.clickzero2 == True:
                self.clickzero2 = False
                self.line2amps = 0
                self.ybox.sendWrite(0,1,0) # write meter 1
                self.ybox.sendWrite(0,4,0)
                pygame.draw.rect(self.screen, white, (380, 226, 265, 255), 0)
                self.screen.blit(self.font3.render("Amps", True, (black)), (460, 235))
                self.screen.blit(self.font3.render("1:", True, (black)), (400, 300))
                self.screen.blit(self.font3.render("2:", True, (black)), (400, 340))
                
                self.screen.blit(self.font3.render("%.4f" % self.line1amps, True, (black)), (460, 300)) 
                self.screen.blit(self.font3.render("%.4f" % self.line2amps, True, (black)), (460, 340))
                pygame.display.update()
            


            

            
   

          
            

            
        
            
            
            


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
    light_green = (30,210,30)

    psSim = PsSim()
    psSim.on_execute()

   

