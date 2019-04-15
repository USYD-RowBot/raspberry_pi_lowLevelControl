#!/usr/bin/env python
# IMU calibrator.

import time
import sys
import rospy
import numpy
import math
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from std_msgs.msg import Header

rospy.init_node("imucalibrator", anonymous=True)

INPUT_CHANNEL = rospy.get_param("input", "imu_raw")  # or lsm - but lsm is not implemented
OUTPUT_CHANNEL = rospy.get_param("output", "imu")

imu_pub = rospy.Publisher(OUTPUT_CHANNEL, Imu)

calibrationSettings=None
vertical=Vector3()
def cb(data):
    global vertical
    global calibrationSettings
    newData=data.data
    if calibrationSettings:
        # rotate old vertical by angular velocity to obtain new vertical
        phi=data.data.angular_velocity.x
        the=data.data.angular_velocity.y
        xi=data.data.angular_velocity.z
        A=numpy.array([[math.cos(phi),math.sin(phi),0],
                       [-math.sin(phi),math.cos(phi),0],
                       [0,0,1],])
        B=numpy.array([[1,0,0],
                       [math.cos(the),math.sin(the),0],
                       [-math.sin(the),math.cos(the),0],
                       [0,0,1],])
        C=numpy.array([[math.cos(xi),math.sin(xi),0],
                       [-math.sin(xi),math.cos(xi),0],
                       [0,0,1],])
        vertical=numpy.matmul(numpy.matmul(numpy.matmul(old_vertical,A),B),C)
        g=Vector3()
        g.x=vertical[0]*-9.81
        g.y=vertical[1]*-9.81
        g.z=vertical[2]*-9.81
        # subtract g from acceleration
        newData.linear_acceleration=newData.linear_acceleration-g
        imu_pub.publish(newData)
    else:
        vertical=numpy.array([0,1,0])


sub=rospy.Subscriber(INPUT_CHANNEL,Imu,cb)
rospy.spin()