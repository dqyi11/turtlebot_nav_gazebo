'''
Created on Apr 24, 2014

@author: walter
'''

from WorldFileReader import *

import sys 

if __name__ == '__main__':
    
    #file = 'world_wall2.world'
    file = '../world/world03.world'
    app = QtGui.QApplication(sys.argv)
    reader = WorldFileReader(file, 30)
    reader.dump('../world/world03.png')
    #reader.save_to_xml('world02.xml')
    sys.exit(app.exec_())
