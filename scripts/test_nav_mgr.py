#!/usr/bin/env python

import rospy
from nav_mgr import *

if __name__ == "__main__":
    nav_mgr = NavMgr()
    try:
        nav_mgr.go_to([5.0,5.0,0.0],[0.0,0.0,0.5,1.0])
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown") 
     
