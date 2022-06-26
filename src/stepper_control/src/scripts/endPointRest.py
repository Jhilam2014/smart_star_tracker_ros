#!/usr/bin/env python3

from numpy import mat
import rospy
from std_msgs.msg import String
import os
import time
import json
import rosnode
import re

pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)


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

def callback(event):
    msg = event.data
    if (msg=="hit"):
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
        os.system('rosrun stepper_control motor_control.py')
        dt = STRUC_SETT
        pub_motor.publish(str(dt))


def listener():
    rospy.Subscriber('endswitch_observer',String, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rosnode_killer', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass