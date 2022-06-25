#!/usr/bin/env python3

import json
import rospy
from std_msgs.msg import String
import time 
import sys
from time import sleep
from datetime import datetime
import re
import operator

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
        self.lastOperation = "1"
        self.editFlag = False


pub = rospy.Publisher('disData', String, queue_size=1000)
pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)

initMenu = Menu()
f = open('pages.json','r+')
jsonData = json.load(f)
jsonString=json.dumps(jsonData)
loadPages = json.loads(jsonString)

opMap = {
    "1": operator.add,
    "3": operator.mul,
    "2": operator.xor,
    "#": operator.sub
}

def operations(val,type,amt):
    if(type=="2"):
        amt=1
        val = int(val)
    else:
        val = float(val)
    val = opMap[type](val,amt)
    return val
        

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
            if(initMenu.currentPage == 'Edit'):
                loadPages[initMenu.currentPage][0]['Enter Value'] += data.data
                pub.publish(str(loadPages['Edit'][0]))
                if(str(data.data) == "Ok"):
                    initMenu.currentPage = loadPages[initMenu.breadcrm[-1]]
                    pub.publish(str(loadPages[initMenu.breadcrm[-1]]))
            else:
                allInfoInPageKeys = loadPages[initMenu.currentPage][0].keys() #example 1,2
                if(data.data in allInfoInPageKeys):
                    query = loadPages[initMenu.breadcrm[-1]][0][str(data.data)] #the name of the object in the json => "1": (Speed)-?> query
                    
                    regex = r"(?!.*\b(?:Run|Stop|Subtract|[\d]{1,})\b).*$"
                    matches = re.match(regex, str(query), re.M)

                    if (matches):
                        initMenu.currentPage = query
                        pub.publish(str(loadPages[query][0]))
                        initMenu.breadcrm.append(initMenu.currentPage)
                    elif (query == "Run"):
                        dt = loadPages
                        dt["type"] = initMenu.currentPage
                        pub_motor.publish(str(dt))
                    else: #set value
                        value = loadPages[initMenu.breadcrm[-1]][0][str(data.data)]
                        
                        if(str(data.data) == "#"):
                            value = loadPages[initMenu.breadcrm[-1]][0][initMenu.lastOperation]
                            loadPages[initMenu.breadcrm[-1]][0][initMenu.lastOperation] = operations(value,str(data.data),10)
                        elif(str(data.data) == "Ok"):
                            initMenu.editFlag = not bool(initMenu.editFlag)
                            if(initMenu.editFlag == True):
                                initMenu.currentPage = 'Edit'
                                pub.publish(str(loadPages['Edit'][0]))
                        else:
                            loadPages[initMenu.breadcrm[-1]][0][str(data.data)] = operations(value,str(data.data),10)
                            initMenu.lastOperation = str(data.data)
                    

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
