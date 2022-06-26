#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import time

def callback(event):
    msg = event.data
    if (msg=="hit"):
        os.system('rosnode kill /stepper_motor_controller')
    time.sleep(5)
    #publish the kill info 

def listener():
    rospy.Subscriber('endswitch_observer',String, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rosnode_killer', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass