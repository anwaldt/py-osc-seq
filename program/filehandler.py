import numpy as np
import jack

from os import listdir
from os.path import isfile, join


class filehandler(object):

	def __init__(self, path=None):
		if path is None:
			self.path = "project/"
		else: 
			self.path = path
		
		self.ID=[]
		self.t=[]
		self.x=[]
		self.y=[]
		self.z=[]
	
	def set_path(self, path):
		self.path = path			

	def start_jack(self):
		self.jclient = jack.Client('jack1')
		self.jclient.activate()
	
	def read_all(self):
		oscFiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
		
		N = len(oscFiles)

		for i in oscFiles:
			with open(self.path + i) as f:
				first_line = f.readline()
			self.ID.append(int(first_line))
			filecontent = np.loadtxt(self.path.__add__(i), delimiter='\t',skiprows =1)
			print(filecontent)
			self.t.append(filecontent[:,0])
			self.x.append(filecontent[:,1])
			self.y.append(filecontent[:,2])
			self.z.append(filecontent[:,3])

class parser(filehandler):

	def __init__(self, fh):
		self.ID = fh.ID
		self.t = fh.t
		self.x = fh.x
		self.y = fh.y
		self.z = fh.z
		#standard value is Panoramix
		self.renderer = 0
		self.IP = '127.0.0.1'
		self.port = 4002

	def change_renderer(self, flag)
		# flag = 0 -> Panoramix
		# flag = 1 -> SSR
		self.renderer = flag
		if flag is 0:
			self.port=4002
		if flag is 1:
			self.port=50001

	def test(self):
		print(self.t)
			
			

		
	