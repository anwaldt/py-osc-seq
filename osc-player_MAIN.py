import argparse
import jack
import os
import time

import threading
import _thread

from os import listdir
from os.path import isfile, join

from pythonosc import dispatcher
from pythonosc import osc_server


from JackTime import JackTime

from OscPlayer import OscPlayer

from OscConnect import OscSender
from OscConnect import OscServer

from PlotWindow import PlotWindow

import sys

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QMainWindow,     QAction, QFileDialog)

from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,QDialog, QSlider,
        QMenu, QPushButton, QRadioButton, QVBoxLayout,QHBoxLayout, QWidget, QButtonGroup, QAbstractButton, QLabel)


from PyQt5.QtGui import (QIcon)


count = 1


class OscPlayerMain(QMainWindow):
    
    glayout = QGridLayout()
    
    
    def __init__(self):
        
        super().__init__()
        
        self.initUI()
        
        self.jackPos      = 0
        self.last_jackPos = 0
    
    
    
        self.OSCout = OscSender()
        self.OSCin  = OscServer()

         

        self.PlayerObjects = []

 
        self.oscPath     = 0;
        
    def initUI(self):  
        
        
        #--------- MENU --------------------------------------------------

 
        self.statusBar()

        openDirectory = QAction(QIcon('open.png'), 'Open', self)
        openDirectory.setShortcut('Ctrl+O')
        openDirectory.setStatusTip('Select Directory for loading project')
        openDirectory.triggered.connect(self.openProject)
        
        
        newDirectory = QAction(QIcon('open.png'), 'New', self)
        newDirectory.setShortcut('Ctrl+O')
        newDirectory.setStatusTip('Chose Directory for creating new project')
        newDirectory.triggered.connect(self.newProject)

    

        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&Project')
        fileMenu.addAction(openDirectory)       
        fileMenu.addAction(newDirectory)      
        
    
        #--------- BUTTONS --------------------------------------------------


        pBut =  QPushButton("Add Source")
        self.glayout.addWidget(pBut)        
        pBut.clicked.connect(self.handleAddButton)


        jBut = QPushButton("Connect to Jack")
        self.glayout.addWidget(jBut)
        jBut.clicked.connect(self.handleJackConnect)
        
        self.currencyButton =  QPushButton("Plot source(s)")
        self.glayout.addWidget(self.currencyButton)        
        self.currencyButton.clicked.connect(self.handlePlotButton)    


        #--------- window setup --------------------------------------------------

    
        wid = QWidget(self)        
        self.setCentralWidget(wid)

            
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('PYROscp')
        self.show()
        wid.setLayout(self.glayout)


###############################################################################################
# 
        
    def handleAddButton(self):
        
        global count
        
        self.Add(str(count))
        count += 1
    
###############################################################################################
# method for adding a source, including gui elements        
    
    
    def Add(self, oscFile):
        
        global count
             
        self.PlayerObjects.append(OscPlayer(count))
        
        l1 = QLabel()
        l1.setText("Source "+str(count))
   
         # radiobuttons
        option_1 = QRadioButton('OFF')
        option_2 = QRadioButton('R')
        option_3 = QRadioButton('W')
        option_1.setChecked(True)  # default option

        # button group
        group = QButtonGroup(self)
        group.addButton(option_1)
        group.addButton(option_2)
        group.addButton(option_3)
        
   
    
           

        if 0 < count <= 16:
            yoff = 0
            xoff = 0
            
        elif 16 < count <= 32:
            yoff  = 4
            xoff  = 16
            
        elif 32 < count <= 48:
            yoff  = 8
            xoff  = 32
            
        elif 48 < count :
            yoff  = 12
            xoff  = 48
                
        #b.clicked.connect(self.Button)
        self.glayout.addWidget(l1,      0+yoff,count-xoff)
        self.glayout.addWidget(option_1,1+yoff,count-xoff)
        self.glayout.addWidget(option_2,2+yoff,count-xoff)        
        self.glayout.addWidget(option_3,3+yoff,count-xoff)
     
###############################################################################################
# 
    def handlePlotButton(self):
        window = PlotWindow(self)
        window.show()


###############################################################################################
# 
        
    def handleJackConnect(self):        
    
            
        self.jack_client = jack.Client('osc-player')
        self.jack_client.activate();
        
        #_thread.start_new_thread( JackTime, () )
         
       
        t = threading.Thread(target=self.JackClocker)
             
        t.start()


###############################################################################################
# 
        
    def openProject(self):

        global count
        
        fname = QFileDialog.getExistingDirectory(self, 'Select directory')

        if fname[0]:
            self.oscPath = fname
            
       
        
        
        oscFiles = [f for f in listdir(self.oscPath) if isfile(join(self.oscPath, f))]

        #--------- create objects, first --------------------------------------------------


        for f in oscFiles:
                  
            oscFile = self.oscPath.__add__("/").__add__(f);
            
            print(oscFile)
            print(str(count))
            
            self.Add(count);
            
            count += 1

        #--------- load data --------------------------------------------------

        count = 0
        
        for f in oscFiles:
                
            self.PlayerObjects[count].LoadFile(self.oscPath+"/"+f)
            count +=1

###############################################################################################
#  

    def newProject(self):

        fname = QFileDialog.getExistingDirectory(self, 'Select directory')

        if fname[0]:
            self.oscPath = fname[0], 'r' 
                
               

###############################################################################################
# 
            
    def showdialog():
       d = QDialog()
       b1 = QPushButton("ok",d)
       b1.move(50,50)
       d.setWindowTitle("Dialog")
       #d.setWindowModality(Qt.ApplicationModal)
       d.exec_()


###############################################################################################
# 
       
    def JackClocker(self):
    
        print("starting jack")

        while 1:
                       
            self.jackPos = self.jack_client.transport_frame
            
            
            if self.jackPos != self.last_jackPos:
# 

                for i in self.PlayerObjects:
                                  
                    i.JackPosChange(self.jackPos, self.OSCout)
                    
                
                self.last_jackPos = self.jackPos;    
        
            time.sleep(0.002)          
   

###############################################################################################
# 
            




if __name__ == "__main__":
    

    app = QApplication(sys.argv)
    ex = OscPlayerMain()
    sys.exit(app.exec_())