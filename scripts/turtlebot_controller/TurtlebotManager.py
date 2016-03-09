#!/usr/bin/env python

import roslib
import rospy
import math
import numpy as np

from PlannedPathLoader import *
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
from NavMgr import *
from TurtlebotController import *

class TurtlebotManager():
    
    def __init__(self, delta, origin, sampleTime):
        
        self.threshold = 2.0

        self.tIdx = 0        
        self.currentPos = [0.0, 0.0]
        self.currentOrientation = 0.0        
        self.plannedPath = PlannedPath()
        rospy.init_node('turtlebot_listener')

        self.nav_mgr = NavMgr()
        self.controller = TurtlebotController(sampleTime)
        
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

    def update(self):
        self.nav_mgr.update() 
        self.currentPos = self.translateFromRobotWorldToPixmap( self.nav_mgr.position )
        self.currentOrientation = self.nav_mgr.orientation 
        print "trans pos" + str(self.currentPos[0]) + " " + str(self.currentPos[1]) + " " + str(self.currentOrientation)

        if self.reached(self.tIdx) == True:
            self.tIdx = self.tIdx + 1
    
    def loadPath(self, path):
        self.plannedPath = path
        self.tIdx = 0
        
    def ctrl(self):
        if self.plannedPath.length > 0 and self.tIdx < self.plannedPath.length:
            pos = [self.plannedPath.waypoints[self.tIdx][0], self.plannedPath.waypoints[self.tIdx][1], 0.0]
            orient = [0.0, 0.0, self.plannedPath.wayorientations[self.tIdx], 1.0]
            self.controller.control( pos, self.currentPos, orient, self.currentOrientation )
        
    def translateFromPixmapToRobotWorld(self, pos):
        x = self.delta * pos[0]+self.origin[0]
        y = self.delta * pos[1]+self.origin[1]
        return [x, y]


    def translateFromRobotWorldToPixmap(self, pos):
        x = (pos[0]- self.origin[0])/self.delta 
        y = (pos[1]- self.origin[1])/self.delta 
        return [x, y]


