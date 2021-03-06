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
from pythonosc import udp_client
from pythonosc import osc_message_builder as omb


from JackTime import JackTime

from OscPlayer import OscPlayer
 
from PlotWindow import PlotWindow

from OscRecorder import OscRecorder

from RecorderWindow import RecorderWindow

import sys

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QCheckBox, QLineEdit)

from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,QDialog, QSlider, 
        QMenu, QPushButton, QRadioButton, QVBoxLayout,QHBoxLayout, QWidget, QButtonGroup, QAbstractButton, QLabel)


from PyQt5.QtGui import (QIcon, QPixmap)

 

count = 1


class OscPlayerMain(QMainWindow):
    
    """ The main OSC player tning """
    
    glayout = QGridLayout()
        
    def __init__(self):
        
        super().__init__()
        
        self.tmpID = 0
        
        self.initUI()
        
        self.jackPos      = 0
        self.last_jackPos = 0
    
    
        self.fs = 0;
    
        self.PlayerObjects = []
     
        self.RecorderObjects = []
        
        self.oscPath     = 0;
                
        self.osc_client = udp_client.SimpleUDPClient("127.0.0.1", 7777)        
 

        
    def initUI(self):  
        
        self.setWindowIcon(QIcon('graphics/TU-Berlin-Logo.svg'))
        
        # Optional, resize window to image size
     
        
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

    
        newRecorder = QAction(QIcon('open.png'), 'New recorder', self)
        newRecorder.setShortcut('Ctrl+R')
        newRecorder.setStatusTip('Start a new OSC recorder')
        newRecorder.triggered.connect(self.newRecoder)
        

        listRecorders = QAction(QIcon('open.png'), 'Show all recorders', self)
        listRecorders.setShortcut('Ctrl+A')
        listRecorders.setStatusTip('')
        listRecorders.triggered.connect(self.newRecoder)
        


        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&Project')
        fileMenu.addAction(openDirectory)       
        fileMenu.addAction(newDirectory)      
        
        
        recoderMenu = menubar.addMenu('&Recorder')
        recoderMenu.addAction(newRecorder)       
        
    
        #--------- BUTTONS on left  --------------------------------------------------


        pBut =  QPushButton("Add Source")
        self.glayout.addWidget(pBut)        
        pBut.clicked.connect(self.handleAddButton)

 

        self.textbox = QLineEdit(self)        
        self.glayout.addWidget(self.textbox);
        

        jBut = QPushButton("Connect to Jack")
        self.glayout.addWidget(jBut)
        jBut.clicked.connect(self.handleJackConnect)
        
        
        self.b = QCheckBox("Connected?")
        #self.b.stateChanged.connect(self.clickBox)
        self.glayout.addWidget(self.b);

        self.jacktimeBox = QLineEdit(self)  
        self.jacktimeBox.setReadOnly(1);
        self.glayout.addWidget(self.jacktimeBox);
        
        
        self.currencyButton =  QPushButton("Plot source(s)")
        self.glayout.addWidget(self.currencyButton)        
        self.currencyButton.clicked.connect(self.handlePlotButton)    

        self.PLOTBox = QLineEdit(self)  
        self.glayout.addWidget(self.PLOTBox);
        
        self.offButton =  QPushButton("ALL OFF!")
        self.glayout.addWidget(self.offButton)        
        self.offButton.clicked.connect(self.handleAllOFF)    

        self.readButton =  QPushButton("ALL READ!")
        self.glayout.addWidget(self.readButton)        
        self.readButton.clicked.connect(self.handleAllR)    
        #--------- window setup --------------------------------------------------

    
        wid = QWidget(self)        
        self.setCentralWidget(wid)

            
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('OSCollect')
        self.show()
        wid.setLayout(self.glayout)


###############################################################################################
# 
        
    def handleAllOFF(self):
        
        for i in self.PlayerObjects:
            
            i.state = "OFF"
            
    def handleAllR(self):
        
        for i in self.PlayerObjects:
            
            i.state = "R"        
            
        
    def handleAddButton(self):
        
        global count
        
        self.Add(str(count))
        
        count += 1
 
    
    
    def button_clicked_1(self, button_or_id):
    
        print('"{}" was clicked for source '.format(button_or_id.text()) + self.tmpID.__str__())
             
        self.PlayerObjects[self.tmpID].ChangeState(button_or_id.text())
    
    def button_clicked_2(self, button_or_id):
        
             
        
#        print('"Id {}" was clicked'.format(button_or_id))  
        
        self.tmpID = button_or_id 
            
###############################################################################################
# method for adding a source, including gui elements        
    
    
    def Add(self, oscFile, label):
        
        global count
             
        self.PlayerObjects.append(OscPlayer(count, label))
        
        l1 = QLabel()
        l1.setText(label)
   
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
        
        
        # all buttons of one group have the same ID
        group.setId(option_1,count-1)
        group.setId(option_2,count-1)
        group.setId(option_3,count-1)


        group.buttonClicked['QAbstractButton *'].connect(self.button_clicked_1)        
        group.buttonClicked['int'].connect(self.button_clicked_2)

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
     
        
        self.textbox.clear();
        
         
###############################################################################################
# 
    def handlePlotButton(self):
        
        print("Plotting trayjectory No: "+self.PLOTBox.text())

        player = self.PlayerObjects[int(self.PLOTBox.text())]
        window = PlotWindow(self)
        
        window.set_data(player)
        
        window.show()


###############################################################################################
# 
        
    def handleJackConnect(self):        
                
        self.jack_client = jack.Client('osc-player')
        self.jack_client.activate();
        
        self.fs = self.jack_client.samplerate;
        
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
            
            
            [label, j] = f.split(".")
            
            self.Add(count, label);
            
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

    def newRecoder(self):

        #print("Plotting trayjectory No: "+self.PLOTBox.text())

        window = RecorderWindow(self)

        recorder = OscRecorder()
        
        self.RecorderObjects.append(recorder)  
        
        window.set_data(recorder)
        
        window.show()

               


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
    """ ACID """

    def JackClocker(self):
    
        print("Connecting to Jack server!")

        while 1:
                       
            self.jackPos = self.jack_client.transport_frame
                        
            if self.jackPos != self.last_jackPos:
# 
                Tsec = self.jackPos / self.fs;
                
                self.jacktimeBox.setText('%.2f' % (Tsec));
                
                for i in self.PlayerObjects:
                                  
                    if i.state=="R":
                          
                            i.JackPosChange(Tsec, self.osc_client)                            
                        
                self.last_jackPos = self.jackPos;    
        
            time.sleep(0.002)          
   

###############################################################################################
# 
   
if __name__ == "__main__":
    

    app = QApplication(sys.argv)
    ex = OscPlayerMain()
    sys.exit(app.exec_())
