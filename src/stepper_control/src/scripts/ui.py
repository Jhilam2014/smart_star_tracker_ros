#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import sys
from time import sleep
from flask import Flask, redirect, url_for, request

app = Flask(__name__)


@app.route('/dashboard',methods = ['POST', 'GET'])
def dashboard():
    return "welcome"

def listener():
    rospy.Subscriber('ui_control_control',String, dashboard)
    rospy.spin()

if __name__ == '__main__':
    app.run(debug = True)
    app.run(host='0.0.0.0',port=8800)
    rospy.init_node('ui_control_node', anonymous=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
