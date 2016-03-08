#!/usr/bin/env python

import roslib
import rospy
import math
import numpy as np

from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
from NavMgr import *

class TurtlebotManager(NavMgr):
    
    def __init__(self, delta, origin, sampleTime):
        
        self.threshold = 2.0

        self.tIdx = 0
        
        self.currentPos = [0.0, 0.0]
        self.currentOrientation = 0.0        
        self.plannedPath = PlannedPath()
        rospy.init_node('gazebo_listener')
        
        self.scale = 1.0
        self.worldsize = [0, 0]

        self.origin = origin
        self.delta = delta
        
    def reached(self, t):
        
        if t >= self.plannedPath.length:
            return False
        
        dist = math.sqrt((self.currentPos[0]-self.plannedPath.waypoints[t][0])**2+(self.currentPos[1]-self.plannedPath.waypoints[t][1])**2)
        if dist <= self.threshold:
            return True
        return False    
    
    
    def loadPath(self, path):
        self.plannedPath = path
        self.tIdx = 0
        
        
    def translateFromPixmapToRobotWorld(self, pos):
        x = self.delta * (pos[0]-self.origin[0])
        y = self.delta * (pos[1]-self.origin[1])
        return [x, y]


