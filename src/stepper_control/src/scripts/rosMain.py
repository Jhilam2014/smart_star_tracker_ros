#!/usr/bin/env python3


import json
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time 
import sys
from time import sleep
from datetime import datetime



#IR PIN = 17
ir_pin = 17

#stepper motor pins
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 12 # enable pin (LOW to enable)

MAIN_MENU = '''{
    "1" : "Auto Align",
    "2" : "Speed Control"
}
''' 

class Menu:

    def __init__(self):
        self.currentPage = 'Menu'
        self.breadcrm = []
        self.firstCheck = True


class CircuitControl:

    def __init__(self):
        pass


    def motorCode(self,inputInfo):
        
        mymotortest = RpiMotorLib.A4988Nema(direction, step,(-1,-1,-1), "A4988")
        GPIO.output(EN_pin,GPIO.LOW) 

        dirc = inputInfo['Direction']
        spd = inputInfo['Speed']
        mymotortest.motor_go(dirc, # True=Clockwise, False=Counter-Clockwise
                        "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                        int(spd), # number of steps
                        .0001, # step delay [sec]
                        False, # True = print verbose output 
                        .0) # initial delay [sec]

pub = rospy.Publisher('disData', String, queue_size=1000)
initObj = CircuitControl()
initMenu = Menu()
f = open('pages.json','r+')
jsonData = json.load(f)
jsonString=json.dumps(jsonData)
loadPages = json.loads(jsonString)

def menuBoardCbk(data):
    rospy.loginfo(data)
    if initMenu.firstCheck:
        pub.publish(MAIN_MENU)
        initMenu.firstCheck = False
        initMenu.currentPage = 'Menu'
        initMenu.breadcrm.append(initMenu.currentPage)
    else:
        if (data.data == "<<"):
            if initMenu.breadcrm:
                initMenu.currentPage = initMenu.breadcrm[-2]
                initMenu.breadcrm.append(initMenu.currentPage)
                pub.publish(str(loadPages[initMenu.currentPage][0]))
        else:
            allInfoInPageKeys = loadPages[initMenu.currentPage][0].keys()
            if(data.data in allInfoInPageKeys):
                print(data.data+" in "+initMenu.currentPage)
                query = loadPages[initMenu.breadcrm[-1]][0][str(data.data)] #the name of the object in the json => "1": (Speed)-?> query
                if (query):
                    initMenu.currentPage = query
                    pub.publish(str(loadPages[query][0]))
                    initMenu.breadcrm.append(initMenu.currentPage)
                else: #set value
                    loadPages[initMenu.breadcrm[-1]][0][str(data.data)] = "10"
                    pub.publish(str(loadPages[initMenu.currentPage][0]))

    



def listener():
    rospy.Subscriber('irInfoPubNode',String, menuBoardCbk)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('stepper_motor_controller', anonymous=True)
    try:
        pub.publish(MAIN_MENU)
        listener()
    except rospy.ROSInterruptException:
        pass
