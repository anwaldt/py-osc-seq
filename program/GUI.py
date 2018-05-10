import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QInputDialog,
	QPushButton, QApplication, QLabel, QCheckBox, QAction, QMainWindow, QFileDialog)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from classes import filehandler, parser

class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		self.setGeometry(300, 300, 800, 800)
		self.setWindowTitle('program')
		

		## objects for filehandling and osc communication ##
		
		self.fh = filehandler()

		## MENU ##

		changeProject = QAction('&choose Project folder', self)
		changeProject.triggered.connect(self.showDialog1)

		loadFiles = QAction('&load files', self)
		loadFiles.triggered.connect(self.read_and_generate_cbg)
		
		self.statusBar()
			
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(changeProject)
		fileMenu.addAction(loadFiles)
		
		## -- ##

		self.cbg = checkboxgrid()
		self.setCentralWidget(self.cbg)	

		self.show()

	def showDialog1(self):
		path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.fh.set_path(path + "/")
	
	def read_and_generate_cbg(self):
		self.fh.read_all()
		self.cbg.initCBG(self.fh)
			

class checkboxgrid(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		self.grid.setColumnStretch(0,1)
		self.grid.setColumnStretch(1,1)
		self.grid.setColumnStretch(2,1)
		self.grid.setRowStretch(0,1)
		self.grid.setRowStretch(1,1)
		self.setLayout(self.grid)
		
	
	def initCBG(self,fh):
		
		self.parser = parser(fh)
		
		## PLAY AND PREPARE PLAY BUTTON ##

		self.prepare_play = QPushButton('prepare playing', self)
		self.grid.addWidget(self.prepare_play, 0, 0)
		self.prepare_play.clicked.connect(self.prepare_play_pressed)

		self.play = QPushButton('PLAY', self)
		self.grid.addWidget(self.play, 0, 1)
		self.play.clicked.connect(self.play_pressed)


		## TABLE WITH CHECKBOXES ##
		
		textSOURCES = QLabel('SOURCES')		
		textPLAY = QLabel('PLAY')
		textREC = QLabel('REC')

		self.grid.addWidget(textSOURCES, 1,0)
		self.grid.addWidget(textPLAY, 1,1)
		self.grid.addWidget(textREC, 1,2)

		numbers = fh.ID #source ID list from filehandler
		N = len(numbers)
		
		for i in range(0,N):
			numbers[i] = str(numbers[i])
		
		pcb = [] #PLAY checkboxes
		rcb = [] #REC checkboxes
		binary_list = [0] * N 
		#information about which sources to play and record
		self.parser.sources_to_play=binary_list
		self.parser.sources_to_record=binary_list

		self.labelnames = []

		for i in range (0,N):
			#generate names for sourcenumber label-widgets
			self.labelnames.append(str(i))
			#generate names for play and record checkbox-widgets
			pcb.append(str(pcb) + str(i))
			rcb.append(str(rcb) +str(i))

		for i in range (0,N):

			self.labelnames[i] = QLabel(numbers[i])
			self.grid.addWidget(self.labelnames[i], i+2,0)

			pcb[i] = QCheckBox('')
			self.grid.addWidget(pcb[i], i+2, 1)
			pcb[i].stateChanged.connect(lambda checked, i=i: self.click_pcb(pcb[i], numbers[i], i))
			
			rcb[i] = QCheckBox('')
			self.grid.addWidget(rcb[i], i+2, 2)
			rcb[i].stateChanged.connect(lambda checked, i=i: self.click_rcb(rcb[i], numbers[i], i))

			self.grid.setRowStretch(i+2,1)
		
		self.show()
		

	# actions that happen when checkboxes are clicked
	def click_pcb(self, box_id,num_i,i):
		if box_id.isChecked():
			self.parser.sources_to_play[i]=num_i
			print("playing of source " + str(num_i) + " got activated")
		else:
			self.parser.sources_to_play[i]=0
			print("playing of source " + str(num_i) + " got deactivated")
		print('play: ')
		print (self.parser.sources_to_play)
	def click_rcb(self, box_id,num_i,i):
		if box_id.isChecked():
			self.parser.sources_to_record[i]=num_i
			print("recording of source " + str(num_i) + " got activated")
		else:
			self.parser.sources_to_record[i]=0
			print("recording of source " + str(num_i) + " got deactivated")
		print('record: ')
		print (self.parser.sources_to_record)

	def play_pressed(self):	
	
		self.parser.play()
		

	def prepare_play_pressed(self):
		self.parser.prepare_play()
		self.prepare_play.setStyleSheet("background-color: yellow")
		print('ready for playing')
			
if __name__ == '__main__':

	app = QApplication(sys.argv)
	gui = MainWindow()	
	sys.exit(app.exec_())
		
		