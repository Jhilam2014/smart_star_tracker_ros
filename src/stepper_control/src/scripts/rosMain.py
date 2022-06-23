#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time 
import sys
from time import sleep
from datetime import datetime



#IR PIN = 17
ir_pin = 17

#stepper motor pins
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 12 # enable pin (LOW to enable)


class CircuitControl:

    def __init__(self):
        pass


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


initObj = CircuitControl()
def motorControlCbk(data):
    rospy.loginfo(data)

def listener():
    
    rospy.Subscriber('irInfoPubNode',String, motorControlCbk)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('stepper_motor_controller', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
