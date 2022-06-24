#!/usr/bin/env python3


import json
import rospy
from std_msgs.msg import String
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


pub = rospy.Publisher('disData', String, queue_size=1000)
pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)

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
            allInfoInPageKeys = loadPages[initMenu.currentPage][0].keys() #example 1,2
            if(data.data in allInfoInPageKeys):
                query = loadPages[initMenu.breadcrm[-1]][0][str(data.data)] #the name of the object in the json => "1": (Speed)-?> query
                if (query) and type(query) != int and query != 'Run':
                    initMenu.currentPage = query
                    pub.publish(str(loadPages[query][0]))
                    initMenu.breadcrm.append(initMenu.currentPage)
                elif (query == "Run"):
                    dt = loadPages
                    dt["type"] = initMenu.currentPage
                    pub_motor.publish(str(dt))
                else: #set value
                    if(str(data.data) == "1"):
                        loadPages[initMenu.breadcrm[-1]][0][str(data.data)] += 10
                    elif(str(data.data) == "2"):
                        loadPages[initMenu.breadcrm[-1]][0][str(data.data)] = 1 - loadPages[initMenu.breadcrm[-1]][0][str(data.data)]
                    elif(str(data.data) == "3"):
                        loadPages[initMenu.breadcrm[-1]][0][str(data.data)] = 0.1*loadPages[initMenu.breadcrm[-1]][0][str(data.data)]
                    pub.publish(str(loadPages[initMenu.currentPage][0]))

    



def listener():
    rospy.Subscriber('irInfoPubNode',String, menuBoardCbk)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('keyboard_info_parse', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
