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
   
   
########################################################################################
# 
########################################################################################


osc_client = udp_client.SimpleUDPClient("127.0.0.1", 50001)

osc_client.send_message("/poll",' ') 
     
jack_client = jack.Client('osc-player')
  
jack_client.activate();
  
posFiles     = ['pos-1', 'pos-2']

cnt=1

t=[]
ID = []
x=[]
y=[]

for i in posFiles:
    
    print(["loading", i])

    positions  = np.loadtxt(i, delimiter='\t', usecols=(1,2,3,4))

    t.append(positions[:,0])
    ID.append(positions[:,1])
    x.append(positions[:,2])
    y.append(positions[:,3])

jackPos = jack_client.transport_frame

last_jackPos= jackPos;

while 1:
       
    jackPos = jack_client.transport_frame
        
    if jackPos != last_jackPos:
        
        for i in range(0,2):
                    
            tmpIdx = np.argmin(np.abs(t[i] -jackPos))
               
            msg = omb.OscMessageBuilder(address="/source/position")
            msg.add_arg(ID[i][tmpIdx])  
            msg.add_arg(x[i][tmpIdx]*5)
            msg.add_arg(y[i][tmpIdx]*5)
            msg=msg.build()
            osc_client.send(msg)
                
        last_jackPos = jackPos;    
    time.sleep(0.01)

        
        