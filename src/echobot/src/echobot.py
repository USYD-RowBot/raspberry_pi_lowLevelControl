#!/usr/bin/env python
import rospy
from std_msgs.msg import String
def callback(data):
	rospy.loginfo(rospy.get_caller_id()+ "%s", data.data);

rospy.init_node("echobot")
rospy.Subscriber("chatter",String,callback)
rospy.spin()
