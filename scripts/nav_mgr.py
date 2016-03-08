#!/usr/bin/env python

import roslib
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from nav_msgs.msg import Odometry


class NavMgr():

    def __init__(self):
        rospy.init_node('nav_mgr', anonymous=False)
        # respond to ctrl+C         
        rospy.on_shutdown(self.shutdown)
       
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.pose = None        
        rospy.Subscriber( "odom", Odometry, self.odometryCb ) 
        rospy.loginfo("wait for the action server to come up")
        # wait 5 second
        self.move_base.wait_for_server( rospy.Duration(5) )

    def shutdown(self):
        rospy.loginfo("Quit")
   
    def odometryCb(self, msg):
        self.pose =  msg.pose.pose

    def go_to(self, position, quaternion):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose = Pose( Point(position[0], position[1], position[2] ),
                                      Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]) )r
        self.move_base.send_goal( goal )

        try_time = 10
        for i in range(try_time):
            success = self.move_base.wait_for_result( rospy.Duration(5) )
            if success:
                state = self.move_base.get_state()
                if state == GoalStatus.SUCCEEDED:
                    rospy.loginfo("GOAL REACHED")
                    return True
                else:
                    print self.pose
            else:
                rospy.loginfo("query error at trial "+str(i))
                print self.pose

        return False
