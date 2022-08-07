#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import sys
from time import sleep
import yaml

pub = rospy.Publisher('disData', String, queue_size=1000)

class ConnSubscribers(object):

    def __init__(self):

        # TODO : do a wait topic        
        self.encoder = "0"
        self.motorStatus = False

        rospy.Subscriber('stepper_motor_controller_info',String, self.stepperCbk)
        
        
        rospy.logwarn("Starting Loop...")
        rospy.spin()

    


    def endCallbk(self,msg):
        rospy.loginfo('got encoder %f', msg.data)
        print(msg.data)
        msg = msg.data
        if (msg!="L_on" or msg!="R_on"):
            self.encoder = msg
            if(self.motorStatus == True):
                rospy.logwarn("Motor started")
                dt = {"Angle ": msg}
                pub.publish(str(dt))
            

    def stepperCbk(self,msg):
        # This callback is the boss, this one dictates the publish rate
        rospy.loginfo('motor feed %f', msg.data)
        eventData = yaml.safe_load(str(msg.data))
        eventType = eventData['type'] 
        rospy.loginfo(str(eventType))
        if(eventType == 'Speed Control'):
            self.motorStatus = True
            rospy.Subscriber('endswitch_observer',String, self.endCallbk)
        else:
            self.motorStatus = False





if __name__ == '__main__':
    rospy.init_node('rotary_observer_node', anonymous=True,log_level=rospy.WARN)
    try:
         subs = ConnSubscribers()
    except rospy.ROSInterruptException:
        pass


