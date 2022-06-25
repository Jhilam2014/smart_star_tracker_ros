#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import time

def callback(event):
    nodeName = event.data
    os.system('rosnode kill '+nodeName)
    time.sleep(5)
    #publish the kill info 
    
def listener():
    rospy.Subscriber('killNode',String, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rosnode_killer', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass