import numpy as np
import jack
import socket
import time
import math as m
from os import listdir
from os.path import isfile, join
from pythonosc import osc_message_builder as omb
from OSCcodec import decodeOSC



class filehandler(object):

	def __init__(self, path=None):
		if path is None:
			self.path = "project/"
		else: 
			self.path = path
		
		self.ID=[] # list of IDs
		self.id =[] # id entry for every index
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
			filecontent = np.loadtxt(self.path.__add__(i), delimiter='\t', usecols=(2,))

			
			self.ID.append(int(filecontent[0]))
		
		print(self.ID)
		print(oscFiles)
		#sort oscFiles list in the same way as source ID list
		self.ID, oscFiles = (list(k) for k in zip(*sorted(zip(self.ID, oscFiles))))
		print(self.ID)
		print(oscFiles)

		for i in oscFiles:
			try:
				filecontent = np.loadtxt(self.path.__add__(i), delimiter='\t', usecols=(1,2,3,4,5))
			except:
				filecontent = np.loadtxt(self.path.__add__(i), delimiter='\t', usecols=(1,2,3,4))
			self.t.append(filecontent[:,0])
			self.id.append(filecontent[:,1])
			self.x.append(filecontent[:,2])
			self.y.append(filecontent[:,3])
			try:
				self.z.append(filecontent[:,4])
			except:
				zlist = [] # create list with NaN if no z coordinate is given 
				for j in range(0, len(filecontent[:,0])):
					zlist.append(np.nan)
				self.z.append(zlist)				
				print('no z-coordinate given in ' + str(i))
		print("loaded " + str(N) + " source position files")
		
class parser(filehandler):

	def __init__(self, fh):
		#pass data from filehandler 
		self.ID = fh.ID
		self.id = fh.id
		self.t = fh.t
		self.x = fh.x
		self.y = fh.y
		self.z = fh.z
	
		#standard value is Panoramix
		self.renderer = "panoramix"
		self.ip = '127.0.0.1'
		self.port = 4002
	
		#create socket for UDP connection
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# binary list of sources to be played (linked to checkboxgrid in GUI)
		self.sources_to_play = []
		
		#jack server
		self.jclient = jack.Client('jack1')

	def change_renderer(self, flag):
		# flag = 0 -> Panoramix
		# flag = 1 -> SSR
		self.renderer = flag
		if flag is "panoramix":
			self.port=4002
		if flag is "ssr":
			self.port=50001

	def sendOSC(self, msg):
		self.sock.sendto(msg.dgram, (self.ip, self.port))

	def connect(self):
		if self.renderer is "panoramix":
			pass
		if self.renderer is "ssr":
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
		if self.renderer is "ssr":
			msg = omb.OscMessageBuilder(address="/alive")
			msg = msg.build()
			while 1:
				self.sendOSC(msg) 
				time.sleep(0.5)
		else:
			pass
	
	# creates sources according to files in the project folder
	def create_sources(self):
		if self.renderer is "panoramix":
			pass #TO DO
		if self.renderer is "ssr":
			for i in range(0, len(self.sources_to_play)):
				if self.sources_to_play[i] !=0:
					msg = omb.OscMessageBuilder(address="/source/new")
					msg.add_arg(self.sources_to_play[i], "s")	#name of source
					print(self.sources_to_play[i])
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
					print("created sources in SSR")

	def start_jack(self):
		self.jclient.activate()
		self.jclient.transport_start() # is this necessary?

	def prepare_play(self):
		# sources that want to be used need to be selected, when prepare_play() is called
		# only those can be deselected and reselected in real-time while play() is running

		N = len(self.ID)

		self.ID_play =[]
		self.id_play =[]
		self.t_play = []
		self.x_play =[]
		self.y_play=[]
		self.z_play = []

		#self.sampleoffset =[] # offset between start of movements of different sources with respect to first source that should be played
		for i in range(0,N):
			if self.sources_to_play[i] != 0:
				self.ID_play.append(self.ID[i])
				self.id_play.append(self.id[i][:])
				self.t_play.append(self.t[i][:])
				self.x_play.append(self.x[i][:])
				self.y_play.append(self.y[i][:])
				self.z_play.append(self.z[i][:])

		# NOW PUT ALL VALUES IN BIG LISTS AND SORT THEM ALL IN THE SAME WAY BY TIME INDEX		
		 
		self.iid = []
		self.tt = []
		self.xx = []
		self.yy = []
		self.zz = []
		for i in range(0,len(self.ID_play)):
			self.iid.extend(self.id_play[i])
			self.tt.extend(self.t_play[i])
			self.xx.extend(self.x_play[i])
			self.yy.extend(self.y_play[i])
			self.zz.extend(self.z_play[i])
		print(self.iid)
			
		self.tt,self.iid, self.xx, self.yy, self.zz = (list(k) for k in 
			zip(*sorted(zip(self.tt,self.iid,self.xx, self.yy, self.zz))))

		if self.jclient.transport_state != 'ROLLING':
			self.start_jack()

		# if panoramix  is renderer generate polar coordinates
		# !! sth. with the coordinate transform might not be correct. conversion to x,y,z in panoramix gives different cartesian coordinates (e.g. always z=0)
		if self.renderer == "panoramix":
			self.dist = []
			self.az = []
			self.el = []
			for i in range (0, len(self.tt)):
				self.dist.append(m.sqrt(self.xx[i]**2 + self.yy[i]**2 + self.zz[i]**2))
				self.az.append(m.atan2(self.yy[i],self.xx[i]))
				self.el.append(m.acos(self.zz[i]/self.dist[i]))
		
		self.connect()
		self.create_sources()

		
	def play(self):
		ix = 0 # index for iterating through lines from files for the sources to be played
		l_ix = len(self.tt)
		
		init_jackPos = self.jclient.transport_frame
		diffToJack = init_jackPos-self.tt[0] # desired sample difference between jack clock and samples in file
		#PLAY
		#TO DO: SEND FIRST LINE OSC
		ix =1
		while 1:
			if str(int(self.iid[ix])) in self.sources_to_play:			
				#waiting for jack clock to arrive at desired sample value from file
				while 1:
					jackPos = self.jclient.transport_frame
					if diffToJack <=jackPos - self.tt[ix]:
						#sendOSC
						if self.renderer == "panoramix":
							self.send_position_pan(self.iid[ix], self.dist[ix], self.az[ix], self.el[ix])
						if self.renderer == "ssr":
							self.send_position_ssr(self.iid[ix], self.xx[ix], self.yy[ix])
						break
			ix = ix + 1
			if ix == l_ix:
				print('all values played')
				break

	def send_position_pan(self, num, dist, az, el): 
		add = "/track/" +str(int(num))+ "/dist"
		msg = omb.OscMessageBuilder(address=add)
		msg.add_arg(dist)
		msg = msg.build()
		self.sendOSC(msg)
		print("sent "+ add + " " + str(dist) +" to PANORAMIX ( " + self.ip + " port: " + str(self.port) + " )")	

		add = "/track/" +str(int(num))+ "/azim"
		msg = omb.OscMessageBuilder(address=add)
		msg.add_arg(az)
		msg = msg.build()
		self.sendOSC(msg)
		print("sent "+ add + " " + str(az) +" to PANORAMIX ( " + self.ip + " port: " + str(self.port) + " )")

		add = "/track/" +str(int(num))+ "/elev"
		msg = omb.OscMessageBuilder(address=add)
		msg.add_arg(el)
		msg = msg.build()
		self.sendOSC(msg)
		print("sent "+ add + " " + str(el) +" to PANORAMIX ( " + self.ip + " port: " + str(self.port) + " )")

	def send_position_ssr(self, num, x, y):
		add ="/source/position"
		msg = omb.OscMessageBuilder(address=add)
		msg.add_arg(int(num))  
		msg.add_arg(x)
		msg.add_arg(y)
		msg=msg.build()
		self.sendOSC(msg)
		print("sent "+ add + " " + str(int(num)) + " " +str(x) + " " + str(y) +" to SSR ( " + self.ip + " port: " + str(self.port) + " )")	

		
		




	

	
			
			

		
	