#!/usr/bin/python3
"""OSC Recorder for writing any """

__author__ = "Henrik von Coler"
__date__   = "2019-06-07"



import jack
import os
import time 
 
from pythonosc import dispatcher
from pythonosc import osc_server

from typing import List, Any


class OscRecorder:	

  

    def __init__(self, timer):
         
        self.external_time = 0
        self.timer = timer
        
        
    def start_server(self, ip, po, op):     
         
         self.outpath   = op                  
         self.port      = po         
         self.ip        = ip

         if self.timer == 'jack':
             self.jack_client    = jack.Client('osc-recorder')         
             self.jack_client.activate()
      
         # client.inports.register('input_1')      
      
         

         if not os.path.exists(self.outpath):
             os.makedirs(self.outpath)

  
        
         self.dispatcher = dispatcher.Dispatcher()  
  
         self.dispatcher.map("/*", self.generic_handler)
         
         self.dispatcher.map("/timer", self.external_time_handler)
  
         self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
  
         print("Generic OSC recorder serving on {}".format(self.server.server_address))

         print("Writing files to "+self.outpath)
         
         #self.server.server_activate()
         
         self.server.serve_forever()
         
    #------------------------------------------------------------------------------
      
    
    def generic_handler(self, unused_addr, *oscArgs: List[Any]):
    
        """Generic handler for all OSC paths (addresses)."""
        
        fileString =  unused_addr.replace('/','_') + ".osc"
        
        n_arguments = len(oscArgs)
        
        f       = open(self.outpath + fileString, 'a')
    
        
        
        if self.timer == 'unix':
            timeStamp = time.time()
            f.write('%.12f' % (timeStamp))    
            f.write("\t")
        
        elif  self.timer == 'jack':
            timeStamp = self.jack_client.transport_frame / self.jack_client.samplerate;
            f.write('%.4f' % (timeStamp))
            f.write("\t")
            
        else:# self.timer == 'client':
            timeStamp = self.external_time;
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
        f.close()

        
        
    def external_time_handler(self, unused_addr, timestamp):
        
        self.external_time = timestamp
        
        
    def stop_osc(self):
        
        
        self.server.close()
        
        