#!/usr/bin/env python
import rospy
import time
import math
from std_msgs.msg import Float32, Bool

rospy.init_node("sine")

### Primer code
primer_channel="prime"
primerState=False
def prime_start(data):
    global primerState
    primerState=data.data
    print("Primer recieved prime!")
primer=rospy.Subscriber(primer_channel,Bool, prime_start)

def wait_for_prime():
    global primerState
    primerState=False;
    print("waiting for primer...")
    while primerState==False and not rospy.is_shutdown():
        time.sleep(0.1)
    print("primed to go!")
    
# main
outputLeft=rospy.Publisher("left",Float32,queue_size=10)
outputRight=rospy.Publisher("right",Float32,queue_size=10)
print ("starting...")
wait_for_prime();
print("nyoom")
t=0
while not rospy.is_shutdown():
    value=math.sin(t*0.001)*60
    outputLeft.publish(value)
    outputRight.publish(value)
    t=t+1

