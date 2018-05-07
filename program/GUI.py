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

		self.show()

	def showDialog1(self):
		path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.fh.set_path(path + "/")
	
	def read_and_generate_cbg(self):
		self.fh.read_all()
		self.cbg = checkboxgrid()
		self.cbg.initUI(self.fh)
		self.setCentralWidget(self.cbg)
		
		
	
	

class checkboxgrid(QWidget):
	def __init__(self):
		super().__init__()

	def initUI(self, fh):
		self.grid = QGridLayout()
		self.setLayout(self.grid)
		
		self.parser = parser(fh)

		## TABLE WITH CHECKBOXES ##
		
		textSOURCES = QLabel('SOURCES')		
		textPLAY = QLabel('PLAY')
		textREC = QLabel('REC')

		self.grid.addWidget(textSOURCES, 0,1)
		self.grid.addWidget(textPLAY, 0,2)
		self.grid.addWidget(textREC, 0,3)

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
			self.grid.addWidget(self.labelnames[i], i+1,1)

			pcb[i] = QCheckBox('')
			self.grid.addWidget(pcb[i], i+1, 2)
			pcb[i].stateChanged.connect(lambda checked, i=i: self.click_pcb(pcb[i], numbers[i], i))
			
			rcb[i] = QCheckBox('')
			self.grid.addWidget(rcb[i], i+1, 3)
			rcb[i].stateChanged.connect(lambda checked, i=i: self.click_rcb(rcb[i], numbers[i], i))
		
		## -- ##	

		self.show()

	# actions that happen when checkboxes are clicked
	def click_pcb(self, box_id,num_i,i):
		if box_id.isChecked():
			self.parser.sources_to_play[i]=1
			print("playing of source " + str(num_i) + " got activated")
		else:
			self.parser.sources_to_play[i]=0
			print("playing of source " + str(num_i) + " got deactivated")
		print('play: ')
		print (self.parser.sources_to_play)
	def click_rcb(self, box_id,num_i,i):
		if box_id.isChecked():
			self.parser.sources_to_record[i]=1
			print("recording of source " + str(num_i) + " got activated")
		else:
			self.parser.sources_to_record[i]=0
			print("recording of source " + str(num_i) + " got deactivated")
		print('record: ')
		print (self.parser.sources_to_record)
			
if __name__ == '__main__':

	app = QApplication(sys.argv)
	gui = MainWindow()	
	sys.exit(app.exec_())
		
		