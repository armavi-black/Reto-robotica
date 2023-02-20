#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float32

pubProc = rospy.Publisher('proc_signal', Float32, queue_size=10)
y = 0

def callback(data):
    global y
    y = data.data
    
if __name__=='__main__':
    rospy.init_node('process')
    rospy.Subscriber('time', Float32, None)
    rospy.Subscriber('signal', Float32, callback)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        gt = 0.5 -(y/2)
        rospy.loginfo(gt)
        pubProc.publish(gt)
        rate.sleep()


    