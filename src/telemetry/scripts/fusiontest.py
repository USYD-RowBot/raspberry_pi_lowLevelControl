#!/usr/bin/env python
import rospy
import tf2_rosfrom sensor_msgs.msg import NavSatFix,Imu
from geometry_msgs.msg import TransformStamped,Vector3
rospy.init_node("fusiontest",anonymous=True)
GPSTOPIC=rospy.get_param("~gpsTopic","gps")
IMUTOPIC=rospy.get_param("~imuTopic","imu")

br=tf2_ros.TransformBroadcaster()

GPS0=False
GPS=Vector3(0,0,0)
# subscribe to GPS data, IMU data
def gpsCache(data):
    global GPS
    global GPS0
    GPS.x=data.latitude
    GPS.y=data.longitude
    GPS.z=data.height
    # record initial GPS location
    if GPS0==False:
        GPS0=GPS
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
    if (GPS0):
        deltaGPS=GPS0-GPS
        gpsT=TransformStamped()
        gpsT.header.stamp=rospy.Time.now()
        gpsT.header.frame_id="world"
        gpsT.child_frame_id="gps"
        gpsT.transform.translation=deltaGPS
        gpsT.transform.rotation= tf_conversions.transformations.quaternion_from_euler(0, 0, 0)
        br.sendTransform(gpsT)
    #for imu
    imuT=TransformStamped()
    imuT.header.stamp=rospy.Time.now()
    imuT.header.frame_id="world"
    imuT.child_frame_id="imu"
    imuT.transform.translation=IMU
    imuT.transform.rotation= tf_conversions.transformations.quaternion_from_euler(0, 0, 0)
    br.sendTransform(imuT)
    # publish the tf frames

