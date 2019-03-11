#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import sys
import time
import serial

PORT_NAME=rospy.get_param("port",'/dev/ttyUSB0')

PWM_MAX=rospy.get_param("val_max",100)
PWM_MIN=rospy.get_param("val_min",0)
TIME_MAX=rospy.get_param("time_max",2.00)# in ms
TIME_MIN=rospy.get_param("time_min",1.00)

ser = serial.Serial(PORT_NAME)  # open serial port
rospy.loginfo("Serial port {0} was opened!".format(ser.name))         # check which port was really used

ser.write(b'hello')     # write a string
x = ser.read()          # read one byte
s = ser.read(10)        # read up to ten bytes (timeout)
line = ser.readline()

ser.close()             # close port



topic=rospy.get_param("topic","thrust")




with navio.pwm.PWM(PWM_OUTPUT) as pwm:
    pwm.set_period(50)
    pwm.enable()

    def callback(data):
        scaled=data.data;
        # clip the range
        if (scaled>PWM_MAX):
            scaled=PWM_MAX
        if (scaled<PWM_MIN):
        scaled=PWM_MIN
        # get the corresponding value
        scaled=(scaled-PWM_MIN)/(PWM_MAX-PWM_MIN)*(TIME_MAX-TIME_MIN)+TIME_MIN;
        pwm.set_duty_cycle(scaled)
        # set the servo power

    rospy.init_node("servoNode",anonymous=True)
    rospy.Subscriber(topic,Int32,callback)
    rospy.spin()
