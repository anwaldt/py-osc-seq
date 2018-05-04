import numpy as np
import jack
import socket
import time
from os import listdir
from os.path import isfile, join
from pythonosc import osc_message_builder as omb



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
	
	def read_all(self):
		oscFiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
		
		N = len(oscFiles)

		for i in oscFiles:
			with open(self.path + i) as f:
				first_line = f.readline()
			self.ID.append(int(first_line))
			filecontent = np.loadtxt(self.path.__add__(i), delimiter='\t',skiprows =1)
			self.t.append(filecontent[:,0])
			self.x.append(filecontent[:,1])
			self.y.append(filecontent[:,2])
			self.z.append(filecontent[:,3])
		print("loaded " + str(N) + " source position files")

class parser(filehandler):

	def __init__(self, fh):
		#pass data from filehandler 
		self.ID = fh.ID
		self.t = fh.t
		self.x = fh.x
		self.y = fh.y
		self.z = fh.z
	
		#standard value is Panoramix
		self.renderer = 0
		self.ip = '127.0.0.1'
		self.port = 4002
	
		#create socket for UDP connection
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def change_renderer(self, flag):
		# flag = 0 -> Panoramix
		# flag = 1 -> SSR
		self.renderer = flag
		if flag is 0:
			self.port=4002
		if flag is 1:
			self.port=50001

	def sendOSC(self, msg):
		self.sock.sendto(msg.dgram, (self.ip, self.port))

	def connect(self):
		if self.renderer is 0:
			pass
		if self.renderer is 1:
			#subscribe to SSR (SSR needs to be SERVER)
			msg1 = omb.OscMessageBuilder(address="/subscribe")
			msg1.add_arg(True,"T")
			msg1=msg1.build()
			self.sendOSC(msg1)
			# change message level of this script to server
			msg2 = omb.OscMessageBuilder(address="/message_level")
			msg2.add_arg(3,"i")
			msg2=msg2.build()
			self.sendOSC(msg2)
			# need to send alive messages after subscription

	# only necessary for SSR communication
	def send_alive_messages(self):
		if self.renderer is 1:
			msg = omb.OscMessageBuilder(address="/alive")
			msg = msg.build()
			while 1:
				self.sendOSC(msg) 
				time.sleep(0.5)
		else:
			pass
	
	# creates sources according to files in the project folder
	def create_sources(self):
		if self.renderer is 0:
			pass #TO DO
		if self.renderer is 1:
			N = len(self.ID)
			for i in range(0,N):
				msg = omb.OscMessageBuilder(address="/source/new")
				msg.add_arg(str(self.ID[i]) , "s")	#name of source
				msg.add_arg("point") 		  	#source type
				msg.add_arg("1", "s") 
				msg.add_arg(self.x[i][0], "f") 	  	#x-coordinate
				msg.add_arg(self.y[i][0], "f") 		#y-coordinate
				msg.add_arg(1.0, "f")			#orientation
				msg.add_arg(1.0, "f")
				msg.add_arg(False,"F")
				msg.add_arg(False,"F")
				msg.add_arg(False,"F")
				msg=msg.build()
				self.sendOSC(msg)

	def start_jack(self):
		self.jclient = jack.Client('jack1')
		self.jclient.activate()

	def play(self): # doesn't work yet
		if self.renderer is 0:
			pass #TO DO
		if self.renderer is 1:
			jackPos = self.jclient.transport_frame
			last_jackPos
			print(jackPos)
			N = len(self.ID)
			while 1:
				jackPos = self.jclient.transport_frame
				if jackPos != last_jackPos:
					print('la')
					for i in range(0,N):    
						tmpIdx = np.argmin(np.abs(self.t[i] -jackPos)) ##??
						msg = omb.OscMessageBuilder(address="/source/position")
						msg.add_arg(ID[i])  
						msg.add_arg(x[i][tmpIdx]*5) #why *5??
						msg.add_arg(y[i][tmpIdx]*-  5)
						msg=msg.build()
						self.sendOSC(msg)
						last_jackPos = jackPos;
					time.sleep(0.02)
	

	

	
			
			

		
	