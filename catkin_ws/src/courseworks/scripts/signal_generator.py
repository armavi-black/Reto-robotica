#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float32

pubSig = rospy.Publisher('signal', Float32, queue_size=10)
pubTime = rospy.Publisher('time', Float32, queue_size=10)
rospy.init_node('signal_generator')
rate = rospy.Rate(10)
t = 0

while not rospy.is_shutdown():
    y = np.sin(t)
    rospy.loginfo(t)
    rospy.loginfo(y)
    pubTime.publish(t)
    pubSig.publish(y)
    t = t + 0.1
    rate.sleep()