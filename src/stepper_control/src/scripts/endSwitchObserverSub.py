#!/usr/bin/env python

#this file will be modified with arduino + roslib + rosserial code and circuit.

import rospy
from std_msgs.msg import String
import os
import json

pub = rospy.Publisher('killNode', String, queue_size=1000) 

def callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    pub.publish("/stepper_motor_controller")

def listener():
    rospy.Subscriber('endSwitchStatus',String, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('endswitch_observer_encoder', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass