#!/usr/bin/env python

#this file will be modified with arduino + roslib + rosserial code and circuit.

import rospy
from std_msgs.msg import String
import os
import json


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('endSwitchStatus',String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()