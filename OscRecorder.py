#!/usr/bin/python3
"""OSC Recorder for writing any """

__author__ = "Henrik von Coler"
__date__   = "2019-06-07"


import argparse
import jack
import os
 
from pythonosc import dispatcher
from pythonosc import osc_server

from typing import List, Any


class OscRecorder:	

  

    def __init__(self):
         
        1
        
    def start_server(self, ip, po, op):     
         
         
         self.outpath   = op                  
         self.port      = po         
         self.ip        = ip
                 
         self.client    = jack.Client('osc-recorder')
         
         self.client.activate()
      
         # client.inports.register('input_1')      
      
         

         if not os.path.exists(self.outpath):
             os.makedirs(self.outpath)

  
        
         self.dispatcher = dispatcher.Dispatcher()  
  
         self.dispatcher.map("/*", self.generic_handler)
  
         self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), dispatcher)
  
         print("Generic OSC recorder serving on {}".format(self.server.server_address))

         print("Writing files to "+self.outpath)
         
         self.server.server_activate()
         

    #------------------------------------------------------------------------------
      
    def generic_handler(self, unused_addr, *oscArgs: List[Any]):
        """Generic handler for all OSC paths (addresses)."""
        
        fileString = unused_addr.replace('/','_')
        
        n_arguments = len(oscArgs)
        
        f = open(self.outpath + fileString, 'a')
    
        timeStamp = self.client.transport_frame / self.client.samplerate;
            
        f.write('%.4f' % (timeStamp))    
        f.write("\t")
    
        f.write(unused_addr)       
            
        for i in range(n_arguments):
    
            tmpArg = oscArgs[i]        
            
            # this could be needed for checking types
            # print(type(tmpArg))
            
            f.write("\t")
              
            f.write(str(tmpArg))
            
            
        f.write("\n")
            
        
        #------------------------------------------------------------------------------
        
    def stop_osc(self):
        
        
        self.server.close()
        
        