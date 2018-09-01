#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 14:01:38 2018

@author: anwaldt
"""

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QMainWindow,     QAction, QFileDialog)

from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,QDialog, QSlider,
        QMenu, QPushButton, QRadioButton, QVBoxLayout,QHBoxLayout, QWidget, QButtonGroup, QAbstractButton, QLabel)


from PyQt5.QtGui import (QIcon)

class PlotWindow(QMainWindow):
    
    def __init__(self, parent=None):
        
        super(PlotWindow, self).__init__(parent)
        
        wid = QWidget(self)
        
        self.setCentralWidget(wid)
        
        layout = QVBoxLayout()
         
        self.setGeometry(  350, 300, 700, 700)    
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(300)
        self.sl.setValue(0)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(10)        
        layout.addWidget(self.sl)

         
        self.sl2 = QSlider(Qt.Horizontal)
        self.sl2.setMinimum(0)
        self.sl2.setMaximum(300)
        self.sl2.setValue(300)
        self.sl2.setTickPosition(QSlider.TicksBelow)
        self.sl2.setTickInterval(10)        
        layout.addWidget(self.sl2)

                    
        wid.setLayout(layout)