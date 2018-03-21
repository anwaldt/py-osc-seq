#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 09:25:19 2017

@author: anwaldt
"""

########################################################################################
# Start Stuff
########################################################################################

import numpy as np
 
import time

import jack

from pythonosc import udp_client
from pythonosc import osc_message_builder as omb
   
from os import listdir
from os.path import isfile, join


import argparse


########################################################################################
# 
########################################################################################

def osc_player(oscPath):
    
    osc_client = udp_client.SimpleUDPClient("127.0.0.1", 50001)
    
    osc_client.send_message("/poll",' ') 
    
    ########################################################################################
    # 
    ########################################################################################
    
    
         
    jack_client = jack.Client('osc-player')
      
    jack_client.activate();
    
    ########################################################################################
    # 
    ########################################################################################
    
      
    
    oscFiles = [f for f in listdir(oscPath) if isfile(join(oscPath, f))]
     
    
    N = len(oscFiles)
         
    
    t=[]
    ID = []
    x=[]
    y=[]
    
    for i in oscFiles:
        
        print(["loading".__add__(i)])
        
        positions  = np.loadtxt(oscPath.__add__(i), delimiter='\t', usecols=(1,2,3,4))
        
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
        osc_client.send(msg)
    
        t.append(positions[:,0])
        ID.append(positions[:,1])
        x.append(positions[:,2])
        y.append(positions[:,3])
        
        
    
    
    print('All files read - ready for playback!')
    
    jackPos = jack_client.transport_frame
    
    last_jackPos= jackPos;
    
    
    while 1:
        print(jackPos)
        print(last_jackPos)  
        jackPos = jack_client.transport_frame
        
        if jackPos != last_jackPos:
            
            for i in range(0,N):
                print(str(i) + "position")        
                tmpIdx = np.argmin(np.abs(t[i] -jackPos))
                   
                msg = omb.OscMessageBuilder(address="/source/position")
                msg.add_arg(ID[i][tmpIdx])  
                msg.add_arg(x[i][tmpIdx]*5)
                msg.add_arg(y[i][tmpIdx]*-  5)
                msg=msg.build()
                osc_client.send(msg)
                    
            last_jackPos = jackPos;    
        time.sleep(0.020)   

   

#########################################################################################
## 
#########################################################################################
#
# 
#
#
#########################################################################################
## 
#########################################################################################



if __name__== "__main__":
  parser = argparse.ArgumentParser()        
  parser.add_argument("--oscpath",
                      default =".",help="The osc-path")
  
  args = parser.parse_args()
    
  osc_player(args.oscpath)
        