#!/usr/bin/env python3

from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
import rospy
from std_msgs.msg import String
import json
import yaml

serial = spi(device=0, port=0)
device = sh1106(serial)

def displayMsg(data):
    print(data.data)
    with canvas(device) as draw:
        line = 10
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        rawMsg = data.data
        displayData = yaml.safe_load(str(rawMsg))
      
        for each in displayData:
            draw.text((20, line), str(each)+':'+str(displayData[each]), fill="white")
            line +=10     

def listener():
    rospy.Subscriber('disData',String, displayMsg)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('display_board', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass