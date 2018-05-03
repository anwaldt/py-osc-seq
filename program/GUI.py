import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QInputDialog,
	QPushButton, QApplication, QLabel, QCheckBox)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class GUI(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		self.setLayout(self.grid)
		self.setGeometry(300, 300, 800, 800)
		self.setWindowTitle('program')
		
		## TABLE WITH CHECKBOXES ##

		textSOURCES = QLabel('SOURCES')		
		textPLAY = QLabel('PLAY')
		textREC = QLabel('REC')

		self.grid.addWidget(textSOURCES, 0,1)
		self.grid.addWidget(textPLAY, 0,2)
		self.grid.addWidget(textREC, 0,3)

		N = 5 # TO DO make N changeable
		numbers = []
		pcb = [] #PLAY checkboxes
		rcb = [] #REC checkboxes

		for i in range (0,N):

			numbers.append(str(i))
			pcb.append(str(pcb) + str(i))
			rcb.append(str(rcb) +str(i))

		for i in range (0,N):

			numbers[i] = QLabel(str(i+1))
			self.grid.addWidget(numbers[i], i+1,1)

			pcb[i] = QCheckBox('')
			self.grid.addWidget(pcb[i], i+1, 2)
			pcb[i].stateChanged.connect(lambda checked, i=i: self.click_pcb(pcb[i], i))
			
			rcb[i] = QCheckBox('')
			self.grid.addWidget(rcb[i], i+1, 3)
			rcb[i].stateChanged.connect(lambda checked, i=i: self.click_rcb(rcb[i], i))	

		self.show()

	# actions that happen when checkboxes are clicked
	def click_pcb(self, box_id,i):
		if box_id.isChecked():
			# TO DO: activate playing of source
			print("playing of source " + str(i) + " got activated")
		else:
			# TO DO: deactivate playing of source
			print("playing of source " + str(i) + " got deactivated")
	def click_rcb(self, box_id,i):
		if box_id.isChecked():
			# TO DO: activate playing of source
			print("recording of source " + str(i) + " got activated")
		else:
			# TO DO: deactivate playing of source
			print("recording of source " + str(i) + " got deactivated")
			
if __name__ == '__main__':

	app = QApplication(sys.argv)
	gui = GUI()
	sys.exit(app.exec_())
		
		