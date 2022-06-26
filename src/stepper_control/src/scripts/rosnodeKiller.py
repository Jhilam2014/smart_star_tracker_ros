#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import time
import json

pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)


f = open('pages.json','r+')
jsonData = json.load(f)
jsonString=json.dumps(jsonData)
STRUC_SETT = json.loads(jsonString)
STRUC_SETT['type'] = 'Speed Control'
STRUC_SETT["Speed Control"][0]["1"] = 60
STRUC_SETT["Speed Control"][0]["2"] = 0
STRUC_SETT["Speed Control"][0]["3"] = 10000

def callback(event):
    msg = event.data
    if (msg=="hit"):
        os.system('rosnode kill /stepper_motor_controller')
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