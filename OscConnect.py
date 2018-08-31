#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 23:35:31 2018

@author: anwaldt
"""
from pythonosc import dispatcher

from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import osc_message_builder as omb
    
class OscSender:
    
    
    
    
    
    def __init__(self):
    
        osc_client  = udp_client.SimpleUDPClient("127.0.0.1", 4002)
        
        
   
        # only needed for SSR
        # osc_client.send_message("/poll",' ') 
        
class OscServer:

    def __init__(self):
              
        server = osc_server.ThreadingOSCUDPServer(( "127.0.0.1", 5005), dispatcher)
  
        print("Serving on {}".format(server.server_address))