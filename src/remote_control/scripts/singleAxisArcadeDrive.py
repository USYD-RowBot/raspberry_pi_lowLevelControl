#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import time
import math
XAxisTopic=rospy.get_param("~axisX","axisX")
YAxisTopic=rospy.get_param("~axisY","axisY")
XAxisMin=rospy.get_param("~axisXMin",0)
YAxisMin=rospy.get_param("~axisYMin",0)
XAxisMax=rospy.get_param("~axisXMax",100)
YAxisMax=rospy.get_param("~axisYMax",100)
XAxisCenter=rospy.get_param("~axisXCtr",(XAxisMin+XAxisMax)/2) 
YAxisCenter=rospy.get_param("~axisYCtr",YAxisMin)# no reversing if this is unset
maxPower=rospy.get_param("~maxPower",100)
minPower=rospy.get_param("~minPower",0)
centerPower=rospy.get_param("~ctrPower",minPower)# if this is unset, no reversing also
leftMotorChannel=rospy.get_param("~LeftMotorChannel","left_motor")
rightMotorChannel=rospy.get_param("~RightMotorChannel","right_motor")
deadTimeout=0.01;#s
lastXTime=0;
lastYTime=0; # if either signal times out, cut the power.
Xfactor=0
Yfactor=0
def Xcallback(data):
    global Xfactor
    _Xfactor=data.data;
    #map from rect to unit square
    if _Xfactor>XAxisCenter:
        Xfactor = (_Xfactor-XAxisCenter)/(XAxisMax-XAxisCenter)
    elif  XAxisCenter != XAxisMin:
        Xfactor = -(XAxisCenter-_Xfactor)/(XAxisCenter-XAxisMin)
    else:
        Xfactor=0
    lastXTime=time.time()

def Ycallback(data):
    global Yfactor
    _Yfactor=data.data;
    #map from rect to unit square
    if _Yfactor>YAxisCenter:
        Yfactor = (_Yfactor-YAxisCenter)/(YAxisMax-YAxisCenter)
    elif (YAxisCenter!=YAxisMin):
        Yfactor = -(YAxisCenter-_Yfactor)/(YAxisCenter-YAxisMin)
    else:
        Yfactor=0
    lastYTime=time.time()


rospy.init_node('singleAxisArcadeDrive', anonymous=True)
# left and right subscribers
rospy.Subscriber(XAxisTopic,Int32,Xcallback)
rospy.Subscriber(YAxisTopic,Int32,Ycallback)
# left and right publishers
pub=[rospy.Publisher(leftMotorChannel, Int32, queue_size=10),rospy.Publisher(rightMotorChannel, Int32, queue_size=10)]
print("Mapping {0},{1} ==> {2},{3}".format(XAxisTopic,YAxisTopic,leftMotorChannel,rightMotorChannel))
while not rospy.is_shutdown():
    #convert into radial coords
    rXY=(Xfactor**2+Yfactor**2)**0.5
    thXY=math.atan2(Yfactor,Xfactor)
    thXY=thXY+math.pi*0.25
    rXY=min(1,rXY)
    #convert into left/right square coords
    sqL=rXY*math.sin(thXY)
    sqR=rXY*math.cos(thXY)
    #convert into L/R thrust vector
    if (sqL>0): outL=centerPower+sqL*(maxPower-centerPower)
    else: outL=centerPower+sqL*(centerPower-minPower)
    if (sqR>0):outR=centerPower+sqR*(maxPower-centerPower)
    else: outR=centerPower+sqR*(centerPower-minPower)
    if lastXTime-time.time()<deadTimeout and lastYTime-time.time()<deadTimeout:
        pub[0].publish(outL)
        pub[0].publish(outR)