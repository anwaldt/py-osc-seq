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

import math



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
            self.receiveport = 50002
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
        self.max_sourceID = 0;
        
        
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
        f.write(str(self.jclientr.transport_frame / self.jclientr.samplerate))
        f.write("\t")
        f.write(str(ch1))
        f.write("\t") 
        f.write(str(ch2))
        f.write("\t")
        f.write(str(gain))
        f.write("\n")
        
    def position_handler(self, unused_addr, ID, x, y, timestamp): #make this function external?
        print("positionhandler working")
        tmpName = self.outpath + "pos" + str(ID) + ".osc";
  
        f       = open(tmpName, 'a')
        f.write("position")
        f.write("\t")
        #f.write(str(timestamp))
        f.write(str(self.jclientr.transport_frame))
        f.write("\t")
        f.write(str(ID))
        f.write("\t")
        f.write(str(x))
        f.write("\t")
        f.write(str(y))
        f.write("\n")
        
    def act_jack(self):
        
         #jack client for playing
        self.jclientp = jack.Client('osc-player' + str(id(self)))  #new client necessary for every class member?
        self.jclientp.activate();
        # jack client for recording
        self.jclientr = jack.Client('osc-recorder' + str(id(self)))  #new client necessary for every class member?
        self.jclientr.activate();
        
    def act_send(self):
        # osc-client for sending osc
        self.osc_client = udp_client.SimpleUDPClient(self.ip, self.sendport)
    def act_dispatcher(self):
        # server for recording osc
        self.dispatcher = dispatcher.Dispatcher() 
        self.dispatcher.map("/gain/", self.volume_handler )
        self.dispatcher.map("update/source/position", self.position_handler )
        self.server = osc_server.ThreadingOSCUDPServer(
        (self.ip, self.receiveport), dispatcher)
        print("Serving on {}".format(self.server.server_address))
        
    def poll(self):
        self.osc_client.send_message("/poll",' ') 
        
    def activate(self):
        self.act_jack()
        self.act_send()
        self.act_dispatcher()
        self.poll()
        
    def subscribe(self):
        msg = omb.OscMessageBuilder(address="/subscribe")
        msg.add_arg(True,"T")
        msg.add_arg(self.ip)
        msg.add_arg(self.receiveport)
        msg=msg.build()
        self.osc_client.send(msg)
        
    def create_sources(self, N, r):
        
        for i in range(0,N):
            
            
            msg = omb.OscMessageBuilder(address="/source/new")
            msg.add_arg("source"+ str(i+1) , "s")
            msg.add_arg("point")
            msg.add_arg("1", "s")
            #arrange sources in a circle
            msg.add_arg(r*math.cos(i/N*3.14159*2+3.14159/2), "f")
            msg.add_arg(r*math.sin(i/N*3.14159*2+3.14159/2), "f")
            msg.add_arg(1.0, "f") #orientation
            msg.add_arg(1.0, "f")
            #msg.add_arg(1, "i")
            #msg.add_arg("1", "s")
            msg.add_arg(False,"F")
            msg.add_arg(False,"F")
            msg.add_arg(False,"F")
            
            msg=msg.build()
            self.osc_client.send(msg)
            
        self.max_sourceID = self.max_sourceID + N
    def delete_source(self, i):
        msg = omb.OscMessageBuilder(address="/source/delete")
        msg.add_arg(i)
        msg=msg.build()
        self.osc_client.send(msg)
        if i == self.max_sourceID:
            self.max_sourceID = self.max_sourceID - 1 # will cause problems if a source with non-maximal ID will be deleted
            
        
    def read_send(self):
        
        oscFiles = [f for f in listdir(self.inpath) if isfile(join(self.inpath, f))]
     
    
        N = len(oscFiles)
         
    
        t=[]
        ID = []
        x=[]
        y=[]
    
        self.create_sources(N)
   
        for i in oscFiles:
            
            print(["loading".__add__(i)])
            
            positions  = np.loadtxt(self.inpath.__add__(i), delimiter='\t', usecols=(1,2,3,4))
    
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
        self.server.serve_forever()  #doesn't work yet
        
         