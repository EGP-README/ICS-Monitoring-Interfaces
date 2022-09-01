import time
import msvcrt
from pygame.locals import *
import serial
import _thread

"""
# Author: Evan Plumley
# version: 1.0
#
#  The Ybox class interfaces with the Ybox via serial connection as an API to the 
   PLC
# dependencies: pygame, pyserial
"""


class Ybox(object):
    def __init__(self):
        self.ser = serial.Serial(
	    port= 'COM4',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS,
            timeout = 1
            )
        time.sleep(1)
        print ("Initialize Complete")


    def readLine(self):
        line = self.ser.readline().decode()
        line = line.strip ()
        return line

    def sendRead(self, slot, channel):
        msg = "R" + str(slot) + "," + str(channel) + "\n"
        self.ser.write(msg.encode())
        line = self.ser.readline().decode()
        line = line.strip ()
        #Give me an integer
        split=line.split(',')
        line=split[2]
        line=int(line,16)
        return line
    def sendAnRead(self, slot, channel):
        msg = "R" + str(slot) + "," + str(channel) + "\n"
        self.ser.write(msg.encode())
        line = self.ser.readline().decode()
        line = line.strip ()
        return line

    def sendWrite(self, slot, channel, value):
        msg = "W" + str(slot) + "," + str(channel) + "," + str(value) + "\n"
        self.ser.write(msg.encode())
        line = self.ser.readline().decode()
        line = line.strip ()
        return line

    def sendAnWrite(self, slot, channel, value):
        msg = "W" + str(slot) + "," + str(channel) + "," + str(value) + "\n"
        self.ser.write(msg.encode())
        line = self.ser.readline().decode()
        line = line.strip ()
        return line

    def readAll(self, slot):
        slotstr = str(slot)
        msg = 'R1' + slotstr + 'A'
        self.ser.write(msg.encode())
        line = self.ser.readline().decode()
        line = line.strip ()
        return line

    
