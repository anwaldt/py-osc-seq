import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QInputDialog,
	QPushButton, QApplication, QLabel, QCheckBox, QAction, QMainWindow, QFileDialog, QSizePolicy)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from classes import filehandler, parser

class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		self.setGeometry(300, 300, 1000, 1000)
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
		self.setLayout(self.grid)
		#self.grid.setColumnStretch(0,1)
		#self.grid.setColumnStretch(1,1)
		#self.grid.setColumnStretch(2,1)
		#self.grid.setRowStretch(0,1)
		#self.grid.setRowStretch(1,1)
		
		self.sp = QSizePolicy()
		self.sp.setHorizontalStretch(0)
		self.sp.setVerticalStretch(0)
		
	
	def initCBG(self,fh):
		
		self.parser = parser(fh)

		## CHANGE RENDERER ##

		self.pan = QCheckBox('Panoramix')
		self.ssr = QCheckBox('SSR')

		self.pan.setSizePolicy(self.sp)
		self.ssr.setSizePolicy(self.sp)		


		self.grid.addWidget(self.pan,0,0 )
		self.grid.addWidget(self.ssr,0,1 )

		self.pan.setCheckState(QtCore.Qt.Checked)

		self.pan.stateChanged.connect(lambda checked: self.click_pan(self.pan))
		self.ssr.stateChanged.connect(lambda checked: self.click_ssr(self.ssr))
		
		## PLAY AND PREPARE PLAY BUTTON ##

		self.prepare_play = QPushButton('prepare playing', self)
		self.prepare_play.setSizePolicy(self.sp)
		self.grid.addWidget(self.prepare_play, 1, 0)
		self.prepare_play.clicked.connect(self.prepare_play_pressed)

		self.play = QPushButton('PLAY', self)
		self.play.setSizePolicy(self.sp)
		self.grid.addWidget(self.play, 1, 1)
		self.play.clicked.connect(self.play_pressed)	


		## TABLE WITH CHECKBOXES ##
		
		textSOURCES = QLabel('SOURCES')
		textPLAY = QLabel('PLAY')
		textREC = QLabel('REC')

		textSOURCES.setSizePolicy(self.sp)
		textPLAY.setSizePolicy(self.sp)
		textREC.setSizePolicy(self.sp)

		self.grid.addWidget(textSOURCES, 2,0)
		self.grid.addWidget(textPLAY, 2,1)
		self.grid.addWidget(textREC, 2,2)

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
			self.labelnames[i].setSizePolicy(self.sp)
			self.grid.addWidget(self.labelnames[i], i+3,0)
			

			pcb[i] = QCheckBox('')
			pcb[i].setSizePolicy(self.sp)
			self.grid.addWidget(pcb[i], i+3, 1)
			pcb[i].stateChanged.connect(lambda checked, i=i: self.click_pcb(pcb[i], numbers[i], i))
			
			rcb[i] = QCheckBox('')
			rcb[i].setSizePolicy(self.sp)
			self.grid.addWidget(rcb[i], i+3, 2)
			rcb[i].stateChanged.connect(lambda checked, i=i: self.click_rcb(rcb[i], numbers[i], i))

			self.grid.setRowStretch(i+2,1)

		## SHOW ##

		self.show()

	def click_pan(self, pan):
		if pan.isChecked():
			self.parser.change_renderer("panoramix")
			self.ssr.setCheckState(QtCore.Qt.Unchecked)
			print("switched to Panoramix Renderer")

	
	def click_ssr(self,ssr):
		if ssr.isChecked():
			self.parser.change_renderer("ssr")
			self.pan.setCheckState(QtCore.Qt.Unchecked)
			print("switched to Sound Scape Renderer")
		

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
		
		