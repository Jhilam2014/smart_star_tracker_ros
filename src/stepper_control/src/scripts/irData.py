#!/usr/bin/env python3

import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import String
import json
import yaml
from time import sleep
from datetime import datetime
import time

#IR PIN = 17
ir_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(ir_pin, GPIO.IN)

keyBoardMap = {
    '12901614333' : "Ok",
    '12901663293' : ">>",
    '12901622493' : "<<",
    '12901640343' : '1',
    '12901652583' : '2',
    '12901658703' : '3',
    '12901626063' : '4',
    '12901619943' : '5',
    '12901644933' : '6'
}


class CircuitControl:

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
            
            return timeseries # Returns the raw information about the high and low pulses (HIGH/LOW, time us)

pub = rospy.Publisher('irInfoPubNode', String, queue_size=1000) 

def listener():
    initObj = CircuitControl()
    while not rospy.is_shutdown():
        val = initObj.getIntegerCode(initObj.inputDataRead())
        # try:
        #     sign = keyBoardMap[str(val)]
        #     rospy.loginfo(sign)
        #     pub.publish(sign)
        # except:
        #     pass

        '''
        display IR data
        '''
        try:
            sign =str(val)
            rospy.loginfo(sign)
            pub.publish(sign)
        except:
            pass
        


if __name__ == '__main__':
    rospy.init_node('IR_sensor_Data', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
