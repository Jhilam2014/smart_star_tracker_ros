#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import sys
from time import sleep
from flask import Flask, redirect, url_for, request, render_template, jsonify
import json
import ast
pub_motor = rospy.Publisher('stepper_motor_controller_info', String, queue_size=1000)

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

f = open('pages.json','r+')
jsonData = json.load(f)
jsonString=json.dumps(jsonData)
loadPages = json.loads(jsonString)


@app.route('/run',methods = ['POST'])
def run():
    data = request.data
    data_json = ast.literal_eval(json.loads(data))
    data_json['type'] = "Speed Control -1"
    # pub_motor.publish(str(data))
    return jsonify(data = data_json)
   
@app.route('/dashboard',methods = ['POST', 'GET'])
def dashboard():
    dt = loadPages    
    data = json.dumps(dt, indent=4)
    return render_template('dashboard.html',data=data,valueData=dt)

def listener():
    rospy.Subscriber('ui_control_control',String, dashboard)
    rospy.spin()

if __name__ == '__main__':
    
    rospy.init_node('ui_control_node', anonymous=True)
    app.run(host='0.0.0.0',threaded=True,debug=True)
    # app.run(host='0.0.0.0',threaded=True)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
