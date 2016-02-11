# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 15:59:48 2018

@author: jj
"""


import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QInputDialog,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from osc_handler2 import osc_handler

class OSCGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        grid = QGridLayout()
        self.setLayout(grid) 
        
        
                    
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Controlling SSR with OSC') 
        
        self.osc = osc_handler()
        
        btn1 = QPushButton('Connect', self)
        btn1.clicked.connect(self.initialize)
        
        btn2 = QPushButton('Add sources',self)
        btn2.clicked.connect(self.addSourcesDialog)
        
        grid.addWidget(btn1, 1,1)
        grid.addWidget(btn2, 2,1)
        
        
        self.show()
        
    def initialize(self):
        self.osc.activate()
    def addSourcesDialog(self):
        N, ok = QInputDialog.getInt(self, 'Add Sources', 
            'How Many?')
        if ok:
            r, ok = QInputDialog.getDouble(self, 'Add Sorces',
            'Distance to center')
            if ok:
                self.osc.create_sources(N,r)
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    oscgui = OSCGUI()
    sys.exit(app.exec_())
