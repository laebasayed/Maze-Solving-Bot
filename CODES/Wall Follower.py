#!/usr/bin/env python3
import rospy
from math import inf
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import time

orig_min = 0
current_min = 0
index=0
specific_region=[]
msg= LaserScan()


def callback(msg):
   global orig_min,specific_region
   orig_min = min(msg.ranges[44:89])  
   specific_region = msg.ranges[44:89]


def teleopbot(wrb,wlb,wrf,wlf) :
    msg1= Float64()
    msg2= Float64()
    msg3= Float64()
    msg4= Float64()
    msg1.data = wrb  #wheel right back
    msg2.data = wlb  #wheel left back
    msg3.data = wrf  #wheel right front
    msg4.data = wlf  #wheel left front

    pub1.publish(msg1)
    pub2.publish(msg2)
    pub3.publish(msg3)
    pub4.publish(msg4)
   
def wall():
   global orig_min, specific_region,current_min,index,check
   x= orig_min
   while not rospy.is_shutdown():
       current_min = min(specific_region)
       check = specific_region.count(inf)
       if (x-0.3<= current_min <= x + 0.3):
          teleopbot(30,-30,30,-30)
       elif (current_min > x + 0.3 and check>30):
           teleopbot(30,30,30,30)
       elif (current_min < x -0.3 ): #collision case
           teleopbot(-30,-30,-30,-30)
       else:
          teleopbot(30,-30,30,-30)
      
      


if __name__ == '__main__':  
 
 try:
    rospy.init_node('wall', anonymous=True)
    pub1 = rospy.Publisher('/joint1_vel_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/joint2_vel_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/joint3_vel_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/joint4_vel_controller/command', Float64, queue_size=10)
    sub = rospy.Subscriber('/laser/scan',LaserScan,callback)
    time.sleep(2)
    wall()
 except rospy.ROSInterruptException:
        pass