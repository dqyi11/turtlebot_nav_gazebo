'''
Created on Apr 22, 2014

@author: walter
'''

from PyQt4 import QtGui, QtCore
from MapViewer import *
from PlannedPathLoader import *
from TurtlebotManager import *
import datetime, os

class MapViewForm(QtGui.QMainWindow):
    '''
    classdocs
    '''

    def __init__(self, scale):
        super(QtGui.QMainWindow, self).__init__()
        self.mMapViewer = MapViewer(self)
        self.timerId = -1
        self.mgr = TurtlebotManager(0.5)
        self.scale = scale
        self.initUI()
        
    def initUI(self):

        mapAction = QtGui.QAction('Map', self)
        mapAction.triggered.connect(self.showOpenMapFileDialog)
        pathAction = QtGui.QAction('Path', self)
        pathAction.triggered.connect(self.showOpenPathFileDialog)
        startAction = QtGui.QAction('Start', self)
        startAction.triggered.connect(self.startMonitor)
        stopAction = QtGui.QAction('Stop', self)
        stopAction.triggered.connect(self.stopMonitor)

        self.addPointAction = QtGui.QAction('Add', self)
        self.addPointAction.triggered.connect(self.addPoint)
        self.clearPointsAction = QtGui.QAction('clear', self)
        self.clearPointsAction.triggered.connect(self.clearPoints)
        
        menubar = self.menuBar()
        mapMenu = menubar.addMenu('&Map')
        mapMenu.addAction(mapAction)
        pathMenu = menubar.addMenu('&Path')
        pathMenu.addAction(pathAction)
        startMenu = menubar.addMenu('&Start')
        startMenu.addAction(startAction)
        stopMenu = menubar.addMenu('&Stop')
        stopMenu.addAction(stopAction)
        
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(mapAction)
        self.toolbar.addAction(pathAction)
        self.toolbar.addAction(startAction)
        self.toolbar.addAction(stopAction)
        
        self.setCentralWidget(self.mMapViewer)
        
        self.show()

    def showOpenMapFileDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')

        pixmap = QtGui.QPixmap(fname)
        self.mMapViewer.setPixmap(pixmap)
        
        self.world_width = pixmap.width()
        self.world_height = pixmap.height()
        
        print str(self.world_width) + " - " + str(self.world_height)
        self.mMapViewer.mShowPoint = True
        
        self.mgr.scale = self.scale
        self.mgr.worldsize = [self.world_width, self.world_height]    

    def showOpenPathFileDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
                
        mapLoader = PlannedPathLoader()
        
        print fname
        mapLoader.load(str(fname))
        
        
        directory = os.path.dirname(str(fname))
        mapFile = directory + "/" + str(mapLoader.mapFile)
        print mapFile
        pixmap = QtGui.QPixmap(mapFile)

        self.mMapViewer.setPixmap(pixmap)
        
        self.world_width = pixmap.width()
        self.world_height = pixmap.height()
        
        print str(self.world_width) + " - " + str(self.world_height)
        self.mMapViewer.mShowPoint = True
        
        self.mgr.scale = self.scale
        self.mgr.worldsize = [self.world_width, self.world_height]
        
        self.mgr.loadPath(mapLoader.path)
        self.mMapViewer.plannedPath = mapLoader.path
        
        
        
    def timerEvent(self, e):
        
        #print "updating"
        self.mgr.update()
        
        #print str(self.mgr.currentPos[0]) + " " + str(self.mgr.currentPos[1]) + " " + str(self.mgr.currentOrientation)
        
        #posx = int(self.mgr.currentPos[0] * self.scale) + self.world_width/2
        #posy = int(self.mgr.currentPos[1]* self.scale) + self.world_height/2
        posx = self.mgr.currentPos[0]
        posy = self.mgr.currentPos[1]
        
        '''
        xPos = self.mMapViewer.mPoint.x()
        yPos = self.mMapViewer.mPoint.y()
        if xPos < self.mMapViewer.width():
            self.mMapViewer.mPoint.setX(xPos+1)
        if self.mMapViewer.mPoint.y() < self.mMapViewer.height():
            self.mMapViewer.mPoint.setY(yPos+1)
        self.statusBar().showMessage(str(xPos)+"+"+str(yPos))
        '''
        
        self.mMapViewer.mPoint.setX(posx)
        self.mMapViewer.mPoint.setY(posy)  
        self.mMapViewer.mPointYaw = self.mgr.currentOrientation      
        
        self.update()
        self.mgr.control()
        self.mMapViewer.plannedPathReachedIdx = self.mgr.tIdx
        
    def startMonitor(self):
        self.timerId = self.startTimer(50)
        
    def stopMonitor(self):
        self.killTimer(self.timerId)

    def addPoint(self, pos):
        new_point = [self.clickPoint.x(), self.clickPoint.y()]
        print "add point " + str(new_point)
        self.mgr.ctrl.plannedPath.addWaypoint(new_point)
        self.mgr.ctrl.plannedPath.update()
        self.mMapViewer.plannedPath.addWaypoint(new_point)
        self.mMapViewer.plannedPath.update()
        self.update()
         
    def clearPoints(self):
        print "clear points"
        self.mgr.plannedPath.clearWaypoints()
        self.mMapViewer.plannedPath.clearWaypoints()
        self.update()

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        addPointAction = menu.addAction("Add Point")
        addPointAction.triggered.connect(self.addPoint)
        clearPointsAction = menu.addAction("Clear Points")
        clearPointsAction.triggered.connect(self.clearPoints)
        self.clickPoint = event.pos()
        menu.exec_(self.mapToGlobal(event.pos()))
      
        
