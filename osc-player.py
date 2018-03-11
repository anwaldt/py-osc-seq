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
  
posFile     = 'positions'     
positions   = np.loadtxt(posFile, delimiter='\t', usecols=(1,2,3,4))

t = positions[:,0]
x = positions[:,2]
y = positions[:,3]


while 1:
       
    jackPos = jack_client.transport_frame
    
    tmpIdx = index = np.argmin(np.abs(t -jackPos))
           
    msg = omb.OscMessageBuilder(address="/source/position")
    msg.add_arg(2)  
    msg.add_arg(x[tmpIdx])
    msg.add_arg(y[tmpIdx])
    msg=msg.build()
    osc_client.send(msg)
   
        
    time.sleep(0.01)

        
        