#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 14:01:38 2018

@author: anwaldt
"""

import sys


import random

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QMainWindow,     QAction, QFileDialog, QDialog)

from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,QDialog, QSlider, QLineEdit,
        QMenu, QPushButton, QRadioButton, QVBoxLayout,QHBoxLayout, QWidget, QButtonGroup, QAbstractButton, QLabel)


from PyQt5.QtGui import (QIcon)

from OscPlayer import OscPlayer

 

class RecorderWindow(QDialog):
    
    def __init__(self, parent=None):
        
        super(RecorderWindow, self).__init__(parent)

        # set the layout
        layout = QVBoxLayout()        
        self.setLayout(layout) 
        

        self.button = QPushButton('Start Recorder')
        self.button.clicked.connect(self.start)
        layout.addWidget(self.button)
        
        self.textbox = QLineEdit(self)        
        self.textbox.setText('Enter port!')
        layout.addWidget(self.textbox);

        

        self.resize(630, 150)      
    
        


    def set_data(self, recorder):
        
        self.recorder = recorder
        
        
    def start(self):
        
        self.recorder.start_server("127.0.0.1", 4001, "~/TMP")
        
        self.close
        
        
        