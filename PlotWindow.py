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

from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,QDialog, QSlider,
        QMenu, QPushButton, QRadioButton, QVBoxLayout,QHBoxLayout, QWidget, QButtonGroup, QAbstractButton, QLabel)


from PyQt5.QtGui import (QIcon)

from OscPlayer import OscPlayer

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class PlotWindow(QDialog):
    
    def __init__(self, parent=None):
        
        super(PlotWindow, self).__init__(parent)
        
        
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        


    def set_data(self, player):
        
        self.player = player
        print(player.mainPath)
        
        self.plot()
        
        
    def plot(self):
        
        ''' plot some random stuff '''
        # random data
        data = self.player.values

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data)

        # refresh canvas
        self.canvas.draw()        
        