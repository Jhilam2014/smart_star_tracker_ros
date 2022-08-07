#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import time
import json
import rosnode
import re

flag = True

def callback(event):
    flagData = globals()
    msg = event.data
    if (msg=="L_on" or msg=="R_on"):
        
        if(flagData['flag']):
            flagData['flag'] = False
            allNodes = rosnode.get_node_names()
            regex = r"\/stepper_motor_controller.*$"
            allSelectedNodes = []
            for each in allNodes:
                matches = re.match(regex, str(each), re.M)
                if(matches):
                    allSelectedNodes.append(matches.group())
            for i in allSelectedNodes:
                os.system('rosnode kill '+i)
            time.sleep(5)
            os.system('rosrun stepper_control motor_control.py &')
    else:
        flagData['flag'] = True
    # rospy.loginfo(flagData['flag'])



def listener():
    rospy.Subscriber('endswitch_observer',String, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rosnode_killer', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass