#!/usr/bin/env python3
import rospy
from math import inf
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import time

region1=region2=region3=region_check=[]
orig_min=min1=min2=min3=0
msg= LaserScan()


def callback(msg):
   global orig_min,region1,region2,region3,region_check
   orig_min = min(msg.ranges[0:89])  
   region1 = msg.ranges[36:71]
   region2 = msg.ranges[72:107]
   region3 =  msg.ranges[108:143]
   region_check = msg.ranges[80:100]

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
   global orig_min,region1,region2,region3,region_check,min1,min2,min3,min_check
   x= orig_min+0.5
   while not rospy.is_shutdown():
       min1=min(region1)
       min2=min(region2)
       min3=min(region3)
       min_check = min(region_check)
       if(x-0.3<=min1<=x+0.3 and min2>1.5):
          teleopbot(1000,-1000,1000,-1000)
       elif (min1>x+0.3 and min2>1.5) :
        teleopbot(1000,1000,1000,1000)
       elif ((min1<x-0.3 and min2<1.5) or (min_check<1.5)):
         teleopbot(-1000,-1000,-1000,-100)
       elif (min2==inf and min3==inf):
          teleopbot(0,0,0,0)
          break
       else:
           teleopbot(1000,-1000,1000,-1000)
      
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