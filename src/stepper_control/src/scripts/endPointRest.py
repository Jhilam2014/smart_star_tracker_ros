#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import os
import time
import json

pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)

#stepper motor pins
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 12 # enable pin (LOW to enable)
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_pin,GPIO.OUT)
STRUC_SETT = {
    "Speed Control": [
        {
           
            "1": 60,
            "2": 0,
            "3": 10000,
        }
    ]
}
STRUC_SETT['type'] = 'Speed Control'


class CircuitControl:
 

    def motorCode(self,dirc,spd,tm):
        
        mymotortest = RpiMotorLib.A4988Nema(direction, step,(-1,-1,-1), "A4988")
        GPIO.output(EN_pin,GPIO.LOW) 

        mymotortest.motor_go(dirc, # True=Clockwise, False=Counter-Clockwise
                        "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                        int(spd), # number of steps
                        float(tm), # step delay [sec]
                        False, # True = print verbose output 
                        .0) # initial delay [sec]

initMotor = CircuitControl()

def callback(event):
    msg = event.data
    if (msg=="hit"):
        os.system('rosnode kill /stepper_motor_controller')
        time.sleep(5)

        steps = 30000
        direc = bool(0)
        tm = 1/float(10000)
        initMotor.motorCode(direc,steps,tm)
        time.sleep(5)
        os.system('rosrun stepper_control motor_control.py')
       


def listener():
    rospy.Subscriber('endswitch_observer',String, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rosnode_killer', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass