#!/usr/bin/env python3


import json
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time 
import sys
from time import sleep
from datetime import datetime
import yaml



#stepper motor pins
direction= 22 # Direction (DIR) GPIO Pin 15
step = 23 # Step GPIO Pin 16
EN_pin = 12 # enable pin (LOW to enable)
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_pin,GPIO.OUT)


pub_stepperStatus = rospy.Publisher('stepper_motor_status', String, queue_size=1000)

class CircuitControl:
 

    def motorCode(self,dirc,spd,tm):
        
        mymotortest = RpiMotorLib.A4988Nema(direction, step,(-1,-1,-1), "A4988")
        GPIO.output(EN_pin,GPIO.LOW) 
        pub_stepperStatus.publish(str({"status":"active"+str(spd)+str(dirc)+str(tm)}))
        rospy.loginfo(str(spd))
        mymotortest.motor_go(dirc, # True=Clockwise, False=Counter-Clockwise
                        "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                        int(spd), # number of steps
                        float(tm), # step delay [sec]
                        False, # True = print verbose output 
                        .0) # initial delay [sec]
        pub_stepperStatus.publish(str({"status":"idle"+str(spd)}))

initMotor = CircuitControl()


def stepperCbk(event):
    
    eventData = yaml.safe_load(str(event.data))
    eventType = eventData['type'] 
    rospy.loginfo(str(eventType))
    if(eventType == 'Speed Control'):
        steps = int(eventData['Speed Control'][0]["1"])*500
        direc = bool(int(eventData['Speed Control'][0]["2"]))
        tm = 1/float(eventData['Speed Control'][0]["3"])
        initMotor.motorCode(direc,steps,tm)

    

def listener():
    rospy.Subscriber('stepper_motor_controller_info',String, stepperCbk)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('stepper_motor_controller', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass