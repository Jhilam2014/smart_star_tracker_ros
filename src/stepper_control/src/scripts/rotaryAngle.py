#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import sys
from time import sleep
import yaml



class ConnSubscribers(object):

    def __init__(self):

        # TODO : do a wait topic        
        self.encoder = "0"
        self.motorStatus = False

        rospy.Subscriber('stepper_motor_controller_info',String, self.stepperCbk)
        rospy.Subscriber('endswitch_observer',String, self.endCallbk)
        if(self.motorStatus == True):
            pub.publish(self.encoder)
    def loop(self):
        rospy.logwarn("Starting Loop...")
        rospy.spin()

pub = rospy.Publisher('disData', String, queue_size=1000)

def endCallbk(self,msg):
    rospy.loginfo('got encoder %f', msg.data)
    msg = msg.data
    if (msg!="L_on" or msg!="R_on"):
        self.encoder = msg

def stepperCbk(self,msg):
    # This callback is the boss, this one dictates the publish rate
    rospy.loginfo('motor feed %f', msg.data)
    eventData = yaml.safe_load(str(msg.data))
    eventType = eventData['type'] 
    rospy.loginfo(str(eventType))
    if(eventType == 'Speed Control'):
        self.motorStatus = True
    else:
        self.motorStatus = False





if __name__ == '__main__':
    rospy.init_node('rotary_observer_node', anonymous=True,log_level=rospy.WARN)
    try:
         subs = ConnSubscribers()
         subs.loop()
    except rospy.ROSInterruptException:
        pass


