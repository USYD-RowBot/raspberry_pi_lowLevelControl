#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import sys
import time
import navio.pwm
import navio.util

navio.util.check_apm()
PWM_OUTPUT=rospy.get_param("srv_num",0)
PWM_MAX=rospy.get_param("val_max",100)
PWM_MIN=rospy.get_param("val_min",0)
TIME_MAX=rospy.get_param("time_max",2.00)# in ms
TIME_MIN=rospy.get_param("time_min",1.00)
topic=rospy.get_param("topic","thrust")
pwm=navio.pwm.PWM(PWM_OUTPUT)
pwm.set_period(50)
pwm.enable()

def callback(data):
    scaled=data.data;
    # clip the range
    if (scaled>PWM_MAX)scaled=PWM_MAX
    if (scaled<PWM_MIN)scaled=PWM_MIN
    # get the corresponding value
    scaled=(scaled-PWM_MIN)/(PWM_MAX-PWM_MIN)*(TIME_MAX-TIME_MIN)+TIME_MIN;
    pwm.set_duty_cycle(scaled)
    # set the servo power
	rospy.loginfo(rospy.get_caller_id()+ "%s", data.data)

rospy.init_node("servoNode",anonymous=True)
rospy.Subscriber(topic,Int32,callback)
rospy.spin()
