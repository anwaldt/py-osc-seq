#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 02:01:23 2018

@author: anwaldt
"""

import jack
import time

class JackTime:
    
    def __init__(self, ):
    
    
        jack_client = jack.Client('osc-player')
      
        jack_client.activate();
        
        jackPos = jack_client.transport_frame
    
        last_jackPos= jackPos;
        
        
        while 1:
           
            jackPos = jack_client.transport_frame
            
            #if jackPos != last_jackPos:
                        
               
                    
            
            last_jackPos = jackPos;    
        
        time.sleep(0.005)   