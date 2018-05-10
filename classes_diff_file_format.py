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

		self.sources_to_play=[]
		self.sources_to_record=[]
	
	def set_path(self, path):
		self.path = path			
	
	def read_all(self):
		oscFiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
		
		N = len(oscFiles)

		for i in oscFiles:
			with open(self.path + i) as f:
				first_line = f.readline()
			self.ID.append(int(first_line))
		#sort oscFiles list in the same way as source ID list
		self.ID, oscfiles = (list(k) for k in zip(*sorted(zip(self.ID, oscFiles))))
		
		for i in oscFiles:		
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
		
		# binary list of sources to be played (linked to checkboxgrid in GUI)
		self.sources_to_play = []

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
		self.jclient.transport_start() # is this necessary?

	def play(self): # doesn't work yet
		if self.renderer is 0:
			pass #TO DO
		if self.renderer is 1:
			N = len(self.ID)
			sampleoffset =[] # offset between start of movements of different sources with respect
			sampleoffset[0] = 0 #  to first source in ID list
			for i in range(1,N):
				sampleoffset[i]=t[i][0]-t[0][0]
			diffToJack=[] # desired sample difference between jack clock and samples in file
			diffToJack[0] = self.jclient.transport_frame-t[0][0]
			for i in range(1,N):
				diffToJack[i]=diffToJack[0]-sampleoffset[i] 

			sampleoffset =[]
			#iterate through sources that should be played
			for i in range(0,len(self.sources_to_play)):
				if sources_to_play[i] is 0:
					pass
				if len(sampleoffset) is 0:
					sampleoffset
				else:
					t_ix = 0
					msg = omb.OscMessageBuilder(address="/source/position")
					msg.add_arg(self.sources_to_play[i])
					msg.add_arg(self.x[i][t_ix])
					msg.add_arg(self.y[i][t_ix])
					msg=msg.build()
					self.sendOSC(msg)
			while 1:
				for i in range(0,len(self.sources_to_play)):
					if sources_to_play[i] is 0:
						pass
					else:
						pass	
				
										


				print('loop i=' + str(i)) 
				print(self.t[i])
				print(jackPos)
				print(np.abs(self.t[i] - jackPos))  
				tmpIdx = np.argmin(np.abs(self.t[i] -jackPos)) ##??
				print(tmpIdx)
				msg = omb.OscMessageBuilder(address="/source/position")
				msg.add_arg(self.ID[i])  
				msg.add_arg(self.x[i][tmpIdx]*5) #why *5??
				msg.add_arg(self.y[i][tmpIdx]*-  5)
				msg=msg.build()
				self.sendOSC(msg)
				last_jackPos = jackPos;
				ime.sleep(0.02)
	

	

	
			
			

		
	