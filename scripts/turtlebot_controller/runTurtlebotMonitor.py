'''
Created on Apr 22, 2014

@author: walter
'''

from MapViewer import *
from MapViewForm import *
from PyQt4 import QtGui, QtCore
import sys

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    form = MapViewForm([-23.4, -12.2], 0.05)
    sys.exit(app.exec_())