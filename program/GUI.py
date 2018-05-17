import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QInputDialog, QMessageBox,
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
	
		addPrefix = QAction('&add filename prefix for recording', self)
		addPrefix.triggered.connect(self.addPrefix)
		
		self.statusBar()
			
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(changeProject)
		fileMenu.addAction(loadFiles)
		fileMenu.addAction(addPrefix)
		
		## -- ##
		self.cbg = checkboxgrid()
		self.setCentralWidget(self.cbg)	

		self.show()

	def showDialog1(self):
		path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.fh.set_path(path + "/")
	
	def read_and_generate_cbg(self):
		self.fh.read_all()
		self.parser = parser(self.fh)
		self.cbg.initCBG(self.fh, self.parser)

	def addPrefix(self):
		if self.cbg.recording == 0:
			text, ok = QInputDialog.getText(self, 'add prefix to filenames for recording', 'enter prefix:')
        
			if ok:
				self.parser.set_prefix(str(text))
				print(str(text))
		else: 
			QMessageBox.about(self,"add prefix to filenames for recording", "stop Recording first")

	def closeEvent(self, event):
		try:
			if self.parser.p_alive.is_alive() == True:
				self.parser.p_alive.terminate()
				print("alive message process terminated")
		except:
			pass
		try:
			if self.parser.p_record.is_alive() == True:
				self.parser.p_record.terminate()
				print("record process terminated")
		except:
			pass
		try:
			if self.parser.p_play.is_alive() == True:
				self.parser.p_play.terminate()
				print("play process terminated")
		except:
			pass
		try:
			for i in range(0,len(self.parser.writefiles)):
				self.parser.writefiles[i].close()
			print("files closed")
		except:
			pass
			

class checkboxgrid(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		self.setLayout(self.grid)		
		self.sp = QSizePolicy()
		self.sp.setHorizontalStretch(0)
		self.sp.setVerticalStretch(0)
		
	
	def initCBG(self, fh, parser):
		
		self.fh = fh
		self.parser = parser

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
		
		## PLAY AND RECORD BUTTONS ##

		self.playing = 0
		self.recording = 0

		self.prepare_play = QPushButton('prepare playing', self)
		self.prepare_play.setSizePolicy(self.sp)
		self.prepare_play.setStyleSheet("background-color: white")
		self.grid.addWidget(self.prepare_play, 1, 0)
		self.prepare_play.clicked.connect(self.prepare_play_pressed)

		self.play = QPushButton('PLAY', self)
		self.play.setSizePolicy(self.sp)
		self.play.setStyleSheet("background-color: white")
		self.grid.addWidget(self.play, 1, 1)
		self.play.clicked.connect(self.play_pressed)	

		self.prepare_rec = QPushButton('prepare recording', self)
		self.prepare_rec.setSizePolicy(self.sp)
		self.prepare_rec.setStyleSheet("background-color: white")
		self.grid.addWidget(self.prepare_rec, 1, 2)
		self.prepare_rec.clicked.connect(self.prepare_rec_pressed)

		self.rec = QPushButton('REC', self)
		self.rec.setSizePolicy(self.sp)
		self.rec.setStyleSheet("background-color: white")
		self.grid.addWidget(self.rec, 1, 3)
		self.rec.clicked.connect(self.rec_pressed)


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

		numbers = self.fh.ID #source ID list from filehandler
		N = len(numbers)
		
		for i in range(0,N):
			numbers[i] = str(numbers[i])
		
		self.pcb = [] #PLAY checkboxes
		self.rcb = [] #REC checkboxes
		binary_list = [0] * N 
		#information about which sources to play and record
		self.parser.sources_to_play=binary_list
		self.parser.sources_to_record=binary_list

		self.labelnames = []

		for i in range (0,N):
			#generate names for sourcenumber label-widgets
			self.labelnames.append(str(i))
			#generate names for play and record checkbox-widgets
			self.pcb.append(str(self.pcb) + str(i))
			self.rcb.append(str(self.rcb) +str(i))

		for i in range (0,N):

			self.labelnames[i] = QLabel(numbers[i])
			self.labelnames[i].setSizePolicy(self.sp)
			self.grid.addWidget(self.labelnames[i], i+3,0)
			

			self.pcb[i] = QCheckBox('')
			self.pcb[i].setSizePolicy(self.sp)
			self.grid.addWidget(self.pcb[i], i+3, 1)
			self.pcb[i].stateChanged.connect(lambda checked, i=i: self.click_pcb(self.pcb[i], numbers[i], i))
			
			self.rcb[i] = QCheckBox('')
			self.rcb[i].setSizePolicy(self.sp)
			self.grid.addWidget(self.rcb[i], i+3, 2)
			self.rcb[i].stateChanged.connect(lambda checked, i=i: self.click_rcb(self.rcb[i], numbers[i], i))

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


	def prepare_play_pressed(self):
		self.parser.prepare_play()
		self.prepare_play.setStyleSheet("background-color: yellow")
		for i in range(0,len(self.fh.ID)):
			if str(self.fh.ID[i]) in self.parser.sources_to_play:
				self.pcb[i].setStyleSheet("background-color: yellow")
			else: 
				self.pcb[i].setStyleSheet("background-color: white")
		
		print('ready for playing')

	def play_pressed(self):	
		if self.playing== 0:
			self.parser.play()
			self.playing = 1
			self.play.setStyleSheet("background-color: green")
			print("playing ... ")
		else:
			self.playing = 0
			self.play.setStyleSheet("background-color: white")
			self.parser.p_play.terminate()
			print("playing stopped")

	def prepare_rec_pressed(self):
		self.parser.prepare_record()
		self.prepare_rec.setStyleSheet("background-color: yellow")
		for i in range(0,len(self.fh.ID)):
			if str(self.fh.ID[i]) in self.parser.sources_to_play:
				self.rcb[i].setStyleSheet("background-color: yellow")
			else: 
				self.rcb[i].setStyleSheet("background-color: white")
		print('ready for recording')

	def rec_pressed(self):
		if self.recording == 0:
			self.parser.record()
			self.recording = 1
			self.rec.setStyleSheet("background-color: red")
			print("recording ...")
		else:
			self.recording = 0
			self.rec.setStyleSheet("background-color: white")
			self.parser.p_record.terminate()
			print("recording stopped")
			self.parser.close_files()
			print("files closed")
		







			
if __name__ == '__main__':

	app = QApplication(sys.argv)
	gui = MainWindow()	
	sys.exit(app.exec_())
		
		