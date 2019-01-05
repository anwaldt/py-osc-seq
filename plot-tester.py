import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
 
import argparse

import numpy as np

 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 
 
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'XY Plotter'
        self.width = 640
        self.height = 400
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        button = QPushButton('Kann noch nichts!', self)
        button.setToolTip('Noch nicht ...')
        button.move(500,0)
        button.resize(140,100)
 
        self.show()
 
 
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        
        posFile     = args.infile
    
        positions   = np.loadtxt(posFile, delimiter='\t', usecols=(1,2,3,4))
    
        data1 = positions[:,2]
        data2 = positions[:,3]
        
        ax = self.figure.add_subplot(111)
        ax.plot(data1,data2, 'r-')
        ax.set_title(args.infile)
            
        ax.set_xlabel('x')
        ax.set_ylabel('y' ,color = [ 0.3, 0.3, 0.3])
        self.draw()
 
if __name__ == '__main__':
 
    parser = argparse.ArgumentParser()        
    parser.add_argument("--infile",
    default ="pos-1",help="filename for plot")

    args = parser.parse_args()


    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())