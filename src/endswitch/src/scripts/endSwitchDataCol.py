#!/usr/bin/env python

#this file will be modified with arduino + roslib + rosserial code and circuit.

import rospy
from std_msgs.msg import String
import os
import json


pub = rospy.Publisher('endSwitchStatus', String, queue_size=1000) 


def listener():
    while not rospy.is_shutdown():
        val = os.popen("curl --connect-timeout 2.5 http://192.168.1.3/helloWorld").read()
        val = json.loads(val)
        res = val["name"]
        # rospy.loginfo(res)
        if (res):
            pub.publish(res)
        
        

if __name__ == '__main__':
    rospy.init_node('endSwitchObserverNode', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
