import argparse
import jack
import os

from pythonosc import dispatcher
from pythonosc import osc_server


import sys

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QMainWindow, QTextEdit,     QAction, QFileDialog, QApplication, QLineEdit)

from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,QDialog, QSlider,
        QMenu, QPushButton, QRadioButton, QVBoxLayout,QHBoxLayout, QWidget, QButtonGroup, QAbstractButton, QLabel)


from PyQt5.QtGui import (QIcon)


count = 1


class OscPlayer(QMainWindow):
    
    
    glayout = QGridLayout()


 
    oscPath = 0;
    
    
    def __init__(self):
        
        super().__init__()
        
        self.initUI()
        
        
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


        p =  QPushButton("Add Source")

        self.glayout.addWidget(p)
        
        p.clicked.connect(self.Add)
        
        self.currencyButton =  QPushButton("Plot source(s)")
        self.glayout.addWidget(self.currencyButton)
        
        self.currencyButton.clicked.connect(self.handlePlotButton)    
    
        wid = QWidget(self)
        self.setCentralWidget(wid)


        for count in range(1,33):       
            self.Add();
        
       
            
            
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('PY OSC PLAYER')
        self.show()
        wid.setLayout(self.glayout)

        
    
    def Add(self):
        
        global count
     
        
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
        
        # buttonClicked signals with two different signatures
        group.buttonClicked['QAbstractButton *'].connect(self.button_clicked)
        group.buttonClicked['int'].connect(self.button_clicked)

 
           

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
     
        count += 1
     
    def Button(self):
        pass

    #@pyqtSlot(QAbstractButton)
    #@pyqtSlot(int)
    
    def button_clicked(self, button_or_id):
        if isinstance(button_or_id, QAbstractButton):
            #self.output_1.setText('"{}" was clicked'.format(button_or_id.text()))
            1;
        elif isinstance(button_or_id, int):
            #self.output_2.setText('"Id {}" was clicked'.format(button_or_id))
            2;

    def handlePlotButton(self):
        window = PlotWindow(self)
        window.show()

            
    def openProject(self):

        fname = QFileDialog.getExistingDirectory(self, 'Select directory')

        if fname[0]:
            self.oscPath = fname[0], 'r'
            
 

    def newProject(self):

        fname = QFileDialog.getExistingDirectory(self, 'Select directory')

        if fname[0]:
            self.oscPath = fname[0], 'r' 
                
               
            
    def showdialog():
       d = QDialog()
       b1 = QPushButton("ok",d)
       b1.move(50,50)
       d.setWindowTitle("Dialog")
       #d.setWindowModality(Qt.ApplicationModal)
       d.exec_()


        
        
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



if __name__ == "__main__":
    

    app = QApplication(sys.argv)
    ex = OscPlayer()
    sys.exit(app.exec_())