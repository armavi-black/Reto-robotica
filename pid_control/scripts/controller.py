#!/usr/bin/env python
import rospy
import numpy as np
from pid_control.msg import motor_output
from pid_control.msg import motor_input
from pid_control.msg import set_point

#Setup parameters
kp = rospy.get_param("/kp", 0.0)
ki = rospy.get_param("/ki", 0.0)
kd = rospy.get_param("/kd", 0.0)
dt = rospy.get_param("/control_sample_time", 0.001)

#Setup variables
errorP = 0
errorI = 0
errorD = 0
u = 0
setpoint = 0
curr_value = 0
prev_error = 0
t = 0

#Callbacks
def setpointCallback(set_point):
   global t
   global setpoint
   setpoint = set_point.setpoint
   t = set_point.time

def motorCallback(motor):
   global curr_value
   global t
   curr_value = motor.output
   t = motor.time


#control output (system input)
def output(spoint, c_value):
   global errorP, errorI, errorD, u, kp, ki, kd, dt, prev_error
   errorP = spoint - c_value
   errorI = errorI + errorP*dt
   errorD = (errorP-prev_error)/dt
   u = kp * errorP + ki*errorI + kd*errorD
   #Set control limits
   if u >= 13:
      u = 13
   if u <= -13:
      u = -13
   
   prev_error = errorP


#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("controller")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers
    pubIn = rospy.Publisher('motor_input', motor_input, queue_size=1)
    rospy.Subscriber('set_point', set_point, setpointCallback)
    rospy.Subscriber('motor_output', motor_output, motorCallback)


    print("The Controller is Running")
    #Run the node
    while not rospy.is_shutdown():

      output(setpoint, curr_value)
      #rospy.loginfo("error: %f", errorP)
      #rospy.loginfo("motor output: %f", curr_value)
      #rospy.loginfo("time: %f", t)
      pubIn.publish(u, t)

      rate.sleep()
