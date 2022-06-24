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


def stepperCbk(event):
    rospy.loginfo(str(event))

def listener():
    rospy.Subscriber('stepper_motor_controller_info',String, stepperCbk)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('stepper_motor_controller', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass