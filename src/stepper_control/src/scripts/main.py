
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time 
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
import sys
from time import sleep
from datetime import datetime

#IR PIN = 17
ir_pin = 17

#stepper motor pins
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 12 # enable pin (LOW to enable)


serial = spi(device=0, port=0)
device = sh1106(serial)

GPIO.setup(ir_pin, GPIO.IN)
GPIO.setup(EN_pin,GPIO.OUT)

keyBoardMap = {
    '12901614333' : "=",
    '12901663293' : ">>",
    '12901622493' : "<<",
    '12901640343' : '1',
    '12901652583' : '2',
    '12901658703' : '3',
    '12901626063' : '4',
    '12901619943' : '5',
    '12901644933' : '6'
}

STRUC = {
    "Speed" : 1000,
    "Direction" : True
}

class CircuitControl:

    def __init__(self):
        pass

    def displayMsg(self,displayData):
        print(displayData)
        with canvas(device) as draw:
            line = 10
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            for each in displayData:
                draw.text((20, line), str(each)+':'+str(displayData[each]), fill="white")
                line +=10     

    def motorCode(self,inputInfo):
        
        mymotortest = RpiMotorLib.A4988Nema(direction, step,(-1,-1,-1), "A4988")
        GPIO.output(EN_pin,GPIO.LOW) 

        dirc = inputInfo['Direction']
        spd = inputInfo['Speed']
        mymotortest.motor_go(dirc, # True=Clockwise, False=Counter-Clockwise
                        "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                        int(spd), # number of steps
                        .0001, # step delay [sec]
                        False, # True = print verbose output 
                        .0) # initial delay [sec]

    def getIntegerCode(self,rawDATA):
            binary = "1" # Decoded binary command
            
            # Covers data to binary
            for (typ, tme) in rawDATA:
                if typ == 1: # Ignore the LOW periods, these should be consitant and thus irrelevant
                    if tme > 1000: # According to NEC protocol a gap of 1687.5 microseconds represents a logical 1 so over 1000 should make a big enough distinction
                        binary += str(1)
                    else:
                        binary += str(0)
                        
            if len(binary) > 34: # Sometimes the binary has two rouge characters on the end
                binary = int(str(binary)[:34])
            
            return int(str(binary),2)
        
    def inputDataRead(self):
            count = 0 #high amplitude data
            timeseries = [] # Pulses and their timings
            lastState = 0 # The previous pin17 state

            val = GPIO.input(ir_pin) # Current pin state
            
            while val: 
                val = bool(GPIO.input(ir_pin))
                sleep(0.0001)
            
            startTime = datetime.now() # Sets start time
            
            while count < 10000:
                if val != lastState: # Waits until change in state occurs
                    now = datetime.now() # Records the current time
                    pulseLength = now - startTime # Calculate time in between pulses
                    startTime = now # Resets the start time
                    timeseries.append((lastState, pulseLength.microseconds)) # Adds pulse time to array (previous val acts as an alternating 1 / 0 to show whether time is the on time or off time)
                
                # Interrupts code if an extended high period is detected (End Of Command)	
                if val:
                    count += 1
                else:
                    count = 0
                
                # Reads values again
                lastState = val
                val = GPIO.input(ir_pin)
            
            return timeseries # Returns the raw information about the high and low pulses (HIGH/LOW, time µs)
while True:
    new = []
    initObj = CircuitControl()
    val = initObj.getIntegerCode(initObj.inputDataRead())
    print(val)
    initObj.displayMsg(STRUC)
    try:
        mapVal = keyBoardMap[str(val)]
#         print("==>",mapVal)
        if mapVal == "=":
            initObj.motorCode(STRUC)
        elif mapVal == ">>":
            STRUC['Direction'] = True
        elif mapVal == "<<":
            STRUC['Direction'] = False
        else:
            STRUC['Speed'] = 1000 * int(mapVal)
        initObj.displayMsg(STRUC)
    except Exception as error:
        print("-->",error)



        

            
    
        




