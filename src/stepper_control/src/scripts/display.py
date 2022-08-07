#!/usr/bin/env python3

from tkinter import font
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
import rospy
from std_msgs.msg import String
import json
import yaml

serial = spi(device=0, port=0,rotate=1)
device = sh1106(serial)

menu = '''
{
    'Menu': 'Ok',
    '*' : 'Initial Position'
}
'''
def displayMsgCbk(data):
    print(data.data)
    
    with canvas(device) as draw:
        line = 5
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        rawMsg = data.data
        displayData = yaml.safe_load(str(rawMsg))
        if('Angle' in displayData.keys()):
            sz = 3
        else:
            sz = 1
        for each in displayData:
            draw.text((5, line), str(each)+':'+str(displayData[each]),font=sz, fill="white")
            line +=10     

def listener():
    rospy.Subscriber('disData',String, displayMsgCbk)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('display_board', anonymous=True)
    # displayMsgCbk(menu)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass