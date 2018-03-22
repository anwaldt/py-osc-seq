# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 12:33:01 2018

@author: jj
"""
import numpy as np
 
import time

import jack

from pythonosc import udp_client
from pythonosc import osc_message_builder as omb
from pythonosc import dispatcher
from pythonosc import osc_server
   
import os
from os import listdir
from os.path import isfile, join



class osc_handler(object):
      
    def __init__(self, ip=None, sendport=None, receiveport=None, outpath=None, 
                 inpath=None):
        
        if ip is None:
            self.ip = "127.0.0.1"
        else:
            self.ip = ip
        if sendport is None:
            self.sendport = 50001
        else:
            self.sendport = sendport
        if receiveport is None:
            self.receiveport = 5005
        else:
            self.receiveport = receiveport
        if outpath is None:
            self.outpath = "oscwrite/"
        else: 
            self.outpath = outpath 
        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)
        if inpath is None:
            self.inpath = "oscread/"
        else: 
            self.inpath = inpath 
        if not os.path.exists(self.inpath):
            os.makedirs(self.inpath) 
        
        
    def set_ip(self, ip):   
        self.ip =ip
        self.osc_client = udp_client.SimpleUDPClient(self.ip, self.sendport)
    def set_sendport(self, sendport):
        self.sendport =sendport
        self.osc_client = udp_client.SimpleUDPClient(self.ip, self.sendport)
    def set_receiveport(self, receiveport):
        self.receiveport =receiveport
    def set_outpath(self, outpath):
        self.outpath = outpath
    def set_inpath(self, inpath):
        self.inpath = inpath    
        
    def volume_handler(self, unused_addr, ch1, ch2, gain, timestamp): #make this function external?
    
        f = open('gains', 'a')
        f.write("gain")
        f.write("\t")
        #f.write(str(timestamp))
        f.write(str(self.jclient.transport_frame / self.jclient.samplerate))
        f.write("\t")
        f.write(str(ch1))
        f.write("\t") 
        f.write(str(ch2))
        f.write("\t")
        f.write(str(gain))
        f.write("\n")
        
    def position_handler(self, unused_addr, ID, x, y, timestamp): #make this function external?

        tmpName = self.outpath + "pos" + str(ID) + ".osc";
  
        f       = open(tmpName, 'a')
        f.write("position")
        f.write("\t")
        #f.write(str(timestamp))
        f.write(str(self.jclient.transport_frame))
        f.write("\t")
        f.write(str(ID))
        f.write("\t")
        f.write(str(x))
        f.write("\t")
        f.write(str(y))
        f.write("\n")
        
    def activate(self):
        
         #jack client for playing
        self.jclientp = jack.Client('osc-player' + str(id(self)))  #new client necessary for every class member?
        self.jclientp.activate();
        # jack client for recording
        self.jclientr = jack.Client('osc-recorder' + str(id(self)))  #new client necessary for every class member?
        self.jclientr.activate();
        # osc-client for sending osc
        self.osc_client = udp_client.SimpleUDPClient(self.ip, self.sendport)
        # server for recording osc
        self.dispatcher = dispatcher.Dispatcher() 
        self.dispatcher.map("/gain/", self.volume_handler )
        self.dispatcher.map("/source/position", self.position_handler )
        self.server = osc_server.ThreadingOSCUDPServer(
        (self.ip, self.receiveport), dispatcher)
        print("Serving on {}".format(self.server.server_address))
        
        #send poll
        self.osc_client.send_message("/poll",' ') 
        
    def poll(self):
        self.osc_client.send_message("/poll",' ') 
        
        
        
    def read_send(self):
        
        oscFiles = [f for f in listdir(self.inpath) if isfile(join(self.inpath, f))]
     
    
        N = len(oscFiles)
         
    
        t=[]
        ID = []
        x=[]
        y=[]
    
        for i in oscFiles:
            
            print(["loading".__add__(i)])
            
            positions  = np.loadtxt(self.inpath.__add__(i), delimiter='\t', usecols=(1,2,3,4))
            
            msg = omb.OscMessageBuilder(address="/source/new")
            msg.add_arg("source"+ str(i) , "s")
            msg.add_arg("point")
            msg.add_arg("1", "s")
            msg.add_arg(positions[1,2], "f")
            msg.add_arg(positions[1,3], "f")
            msg.add_arg(1.0, "f") #orientation
            msg.add_arg(1.0, "f")
            #msg.add_arg(1, "i")
            #msg.add_arg("1", "s")
            msg.add_arg(False,"F")
            msg.add_arg(False,"F")
            msg.add_arg(False,"F")
            
            msg=msg.build()
            self.osc_client.send(msg)
        
            t.append(positions[:,0])
            ID.append(positions[:,1])
            x.append(positions[:,2])
            y.append(positions[:,3])
            
            
        
        
        print('All files read - ready for playback!')
        
        jackPos = self.jclientp.transport_frame
        
        last_jackPos= jackPos;
        
        
        while 1:
            print(jackPos)
            print(last_jackPos)  
            jackPos = self.jclientp.transport_frame
            
            if jackPos != last_jackPos:
                
                for i in range(0,N):
                    print(str(i) + "position")        
                    tmpIdx = np.argmin(np.abs(t[i] -jackPos))
                       
                    msg = omb.OscMessageBuilder(address="/source/position")
                    msg.add_arg(ID[i][tmpIdx])  
                    msg.add_arg(x[i][tmpIdx]*5)
                    msg.add_arg(y[i][tmpIdx]*-  5)
                    msg=msg.build()
                    self.osc_client.send(msg)
                        
                last_jackPos = jackPos;    
            time.sleep(0.020)   

    def receive_write(self):
        self.server.serve_forever()
         