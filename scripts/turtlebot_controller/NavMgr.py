#!/usr/bin/env python

import roslib
import rospy
import tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from nav_msgs.msg import Odometry


class NavMgr():

    def __init__(self):
        #rospy.init_node('nav_mgr', anonymous=False)
        # respond to ctrl+C         
        rospy.on_shutdown(self.shutdown)
       
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.position = [0.0, 0.0]   
        self.orientation = 0.0     
        rospy.Subscriber( "odom", Odometry, self.odometryCb ) 
        rospy.loginfo("wait for the action server to come up")
        # wait 5 second
        self.move_base.wait_for_server( rospy.Duration(5) )
        self.tf_listener = tf.TransformListener()

    def shutdown(self):
        rospy.loginfo("Quit")
   
    def odometryCb(self, msg):
        self.pose =  msg.pose.pose

    def update(self):
        #self.tf_listener.waitForTransform("/map", "/odom", rospy.Time(0), rospy.Duration(3.0)
        try:
            (trans, rot) = self.tf_listener.lookupTransform("/map", "/odom", rospy.Time(0))
        except( tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            return
        self.position[0] = trans[0]
        self.position[1] = trans[1]
        self.orientation = rot[2]

        print "cur pos " + str(self.position[0]) + " " + str(self.position[1]) + " " + str(self.orientation)

        
    def go_to(self, position, quaternion):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose = Pose( Point(position[0], position[1], position[2] ),
                                      Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]) )
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
