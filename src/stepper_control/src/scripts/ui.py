#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import sys
from time import sleep
from flask import Flask, redirect, url_for, request, render_template
import json


pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)

app = Flask(__name__)

f = open('pages.json','r+')
jsonData = json.load(f)
jsonString=json.dumps(jsonData)
loadPages = json.loads(jsonString)




@app.route('/dashboard',methods = ['POST', 'GET'])
def dashboard():
    dt = loadPages    
    dt["type"] = 'Speed Control'
    pub_motor.publish(str(dt))
    
    return render_template('dashboard.html')

def listener():
    rospy.Subscriber('ui_control_control',String, dashboard)
    rospy.spin()

if __name__ == '__main__':
    
    rospy.init_node('ui_control_node', anonymous=True)
    app.run(host='0.0.0.0',threaded=True,debug=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
