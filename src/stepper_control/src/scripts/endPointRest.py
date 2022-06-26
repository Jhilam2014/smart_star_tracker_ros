#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import time
import json

pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)


STRUC_SETT = {
    "Speed Control": [
        {
            "1": 60,
            "2": 0,
            "3": 10000
        }
    ],
    "type": "Speed Control"
}
f = open('pages.json','r+')
jsonData = json.load(f)
jsonString=json.dumps(jsonData)
loadPages = json.loads(jsonString)
loadPages["type"] = "Speed Control"
loadPages["Speed Control"][0]["1"] = 60
loadPages["Speed Control"][0]["2"] = 0
loadPages["Speed Control"][0]["3"] = 10000
Flag = True
def callback(event):
    global Flag
    msg = event.data
    if (msg=="hit"):
        if(Flag == True):
            os.system('rosnode kill /stepper_motor_controller')
            Flag = False
            time.sleep(3)
            os.system('rosrun stepper_control motor_control.py')
            pub_motor.publish(str(loadPages))
    else:
        Flag = True
       


def listener():
    rospy.Subscriber('endswitch_observer',String, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rosnode_killer', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass