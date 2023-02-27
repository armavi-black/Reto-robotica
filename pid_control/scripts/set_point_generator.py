#!/usr/bin/env python
import rospy
import numpy as np
from pid_control.msg import set_point

# Setup Variables, parameters and messages to be used (if required)
#Setup parameters
amplitude = rospy.get_param("defAmplitude", 0.0)
phaseShift = rospy.get_param("phaseShift", 0.0)
verTraslation = rospy.get_param("verTraslation", 0.0)

#Setup variables
t = 0
y = 0

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("Set_Point_Generator")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    #Setup Publishers
    spPub = rospy.Publisher('set_point', set_point, queue_size=10)

    print("The Set Point Genertor is Running")

    #Run the node
    while not rospy.is_shutdown():
        t = rospy.get_time()
        y = amplitude * np.sin(t + phaseShift) + verTraslation
        spPub.publish(y, t)

        rate.sleep()