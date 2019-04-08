#!/usr/bin/env python
import rospy
import time
import math
from std_msgs.msg import Float32, Bool

### Primer code
primer_channel="prime"
primerState=False
def prime_start(data):
    global primerState
    primerState=data.data
primer=rospy.Subscriber(primer_channel,Bool, prime_start)

def wait_for_prime():
    global primerState
    primerState=False;
    while primerState==False and not rospy.is_shutdown():
        time.sleep(0.1)
    
# main
outputLeft=rospy.Publisher("left",Float32,queue_size=10)
outputRight=rospy.Publisher("right",Float32,queue_size=10)
wait_for_prime();
t=0
while not rospy.is_shutdown():
    value=1.5+math.sin(t*0.01)*0.2
    outputLeft.publish(value)
    outputRight.publish(value)
    time.sleep(0.1)
    t=t+1

