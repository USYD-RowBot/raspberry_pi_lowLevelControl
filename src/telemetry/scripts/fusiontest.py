#!/usr/bin/env python
import rospy
import tf2_ros
from sensor_msgs.msg import NavSatFix,Imu
from geometry_msgs.msg import TransformStamped,Vector3
rospy.init_node("fusiontest",anonymous=True)
GPSTOPIC=rospy.get_param("~gpsTopic","gps")
IMUTOPIC=rospy.get_param("~imuTopic","imu")

brIMU=tf2_ros.TransformBroadcaster()
brGPS=tf2_ros.TransformBroadcaster()

GPS0=Vector3(0,0,0)
first=False
GPS=Vector3(0,0,0)
# subscribe to GPS data, IMU data
def gpsCache(data):
    global GPS
    global GPS0
    global first
    GPS.x=data.latitude
    GPS.y=data.longitude
    GPS.z=data.height
    # record initial GPS location
    if first==False:
        GPS0=GPS
        first=True
rospy.Subscriber(GPSTOPIC,NavSatFix,gpsCache)
IMU=Vector3(0,0,0)
def imuCache(data):
    global IMU
    IMU.x=IMU.x+data.linear_acceleration.x
    IMU.y=IMU.y+data.linear_acceleration.y
    IMU.z=IMU.z+data.linear_acceleration.z

rospy.Subscriber(IMUTOPIC,Imu,imuCache)

while not rospy.is_shutdown():
    # calculate and set tf transform of self based on gps
    if first==True:
        deltaGPS=GPS0-GPS
        gpsT=TransformStamped()
        gpsT.header.stamp=rospy.Time.now()
        gpsT.header.frame_id="world"
        gpsT.child_frame_id="gps"
        gpsT.transform.translation=deltaGPS
        gpsT.transform.rotation.w=1
        gpsT.transform.rotation.x=0
        gpsT.transform.rotation.y=0
        gpsT.transform.rotation.z=0
        brGPS.sendTransform(gpsT)
        print ("GPS OK")
    #for imu
    imuT=TransformStamped()
    imuT.header.stamp=rospy.Time.now()
    imuT.header.frame_id="world"
    imuT.child_frame_id="imu"
    imuT.transform.translation=IMU
    imuT.transform.rotation.w=1
    imuT.transform.rotation.x=0
    imuT.transform.rotation.y=0
    imuT.transform.rotation.z=0
    brIMU.sendTransform(imuT)
    # publish the tf frames

