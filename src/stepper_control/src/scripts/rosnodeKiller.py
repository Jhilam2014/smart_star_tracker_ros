#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import time
import rosnode

pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)

STRUC_SETT = {
    "Speed Control": [
        {
            "1": 60,
            "2": 0,
            "3": 10000
        }
    ],
    "type" : "Speed Control"
}

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