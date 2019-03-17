#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
XAxisTopic=rospy.get_param("axisX","axisX")
YAxisTopic=rospy.get_param("axisY","axisY")
XAxisMin=rospy.get_param("axisXMin",0)
YAxisMin=rospy.get_param("axisYMin",0)
XAxisMax=rospy.get_param("axisXMax",100)
YAxisMax=rospy.get_param("axisYMax",100)
XAxisCenter=rospy.get_param("axisXCtr",(XAxisMin+XAxisMax)/2) 
YAxisCenter=rospy.get_param("axisYCtr",YAxisMin)# no reversing if this is unset
maxPower=rospy.get_param("maxPower",100)
minPower=rospy.get_param("minPower",0)
leftMotorChannel=rospy.get_param("LeftMotorChannel","left_motor")
rightMotorChannel=rospy.get_param("RightMotorChannel","right_motor")
reversePower=rospy.get_param("reversePower",minPower)

reallocationFactor=0;
def Xcallback(data):
    global Xfactor
    reallocationFactor=data.data;
    


rospy.init_node('singleAxisArcadeDrive', anonymous=True)
# left and right subscribers
rospy.Subscriber(XAxisTopic,Int32,Xcallback)
rospy.Subscriber(YAxisTopic,Int32,Ycallback)
# left and right publishers
pub=[rospy.Publisher(leftMotorChannel, Int32, queue_size=10),rospy.Publisher(rightMotorChannel, Int32, queue_size=10)]
