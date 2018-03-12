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
  
#posFiles     = [
#        'hermann-1', 
#        'hermann-2', 
#        'hermann-3', 
#        'hermann-4',
#        'hermann-5',
#        'hermann-6',
#        'hermann-7',
#        'hermann-8',
#        'hermann-9',
#        'hermann-10',
#        'hermann-11',
#        'hermann-12',
#        'hermann-13',
#        'hermann-14',
#        'hermann-15',
#        'hermann-16'
#        ]

posFiles     = [
        'test-project-1',
        'test-project-2',
        'test-project-3',
        'test-project-4',
        'test-project-5',
        'test-project-6',
        'test-project-7',
        'test-project-8',
        'test-project-9',
        'test-project-10',
        'test-project-11',
        'test-project-12',
        'test-project-13',
        'test-project-14',
        'test-project-15',
        'test-project-16',
        'test-project-17',
        'test-project-18',
        'test-project-19',
        'test-project-20',
        'test-project-21',
        'test-project-22',
        'test-project-23',
        'test-project-24',
        'test-project-25',
        'test-project-26',
        'test-project-27',
        'test-project-28',
        'test-project-29',
        'test-project-30',
        'test-project-31',
        'test-project-32',
        ]


N = len(posFiles)



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


print('All files read - ready for playback!')

jackPos = jack_client.transport_frame

last_jackPos= jackPos;

while 1:
       
    jackPos = jack_client.transport_frame
        
    if jackPos != last_jackPos:
        
        for i in range(0,N):
                    
            tmpIdx = np.argmin(np.abs(t[i] -jackPos))
               
            msg = omb.OscMessageBuilder(address="/source/position")
            msg.add_arg(ID[i][tmpIdx])  
            msg.add_arg(x[i][tmpIdx]*5)
            msg.add_arg(y[i][tmpIdx]*-5)
            msg=msg.build()
            osc_client.send(msg)
                
        last_jackPos = jackPos;    
    time.sleep(0.01)

        
        