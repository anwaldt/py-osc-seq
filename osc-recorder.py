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

##############################################################################
##############################################################################

def volume_handler(unused_addr, ch1, ch2, gain, timestamp):
    
  f = open('gains', 'a')
  f.write("gain")
  f.write("\t")
  #f.write(str(timestamp))
  f.write(str(client.transport_frame / client.samplerate))
  f.write("\t")
  f.write(str(ch1))
  f.write("\t") 
  f.write(str(ch2))
  f.write("\t")
  f.write(str(gain))
  f.write("\n")
    
#------------------------------------------------------------------------------

def handler_wonder(unused_addr, ID, x, y, duration):

  tmpName = args.outpath + "WONDER_" + str(ID) + "_cartesian" + ".osc";
  
  f       = open(tmpName, 'a')
  
  timeStamp = client.transport_frame / client.samplerate;

  f.write('%.4f' % (timeStamp))
  f.write("\t")

  f.write(unused_addr)
  f.write("\t")
  
  f.write(str(ID))
  f.write("\t")

  f.write('%.4f' % (x))
  f.write("\t")

  f.write('%.4f' % (y))
  f.write("\t")

  f.write('%.4f' % (duration))
  f.write("\n")
    
#------------------------------------------------------------------------------
  
def handler_polar_single(unused_addr, value):
    #
    """ Designed to process PanoramixApp messages. """
    
    [o, t, i, p] = unused_addr.split("/")
    
    tmpName = "track_"+str(i)+'_'+str(p)+".osc";
    f       = open(args.outpath + tmpName, 'a')

    timeStamp = client.transport_frame / client.samplerate;

    f.write('%.4f' % (timeStamp))
    f.write("\t")

    f.write(unused_addr)
    f.write("\t")
  
    f.write(str(value))
    f.write("\n")


#------------------------------------------------------------------------------
  
def generic_handler(unused_addr, *oscArgs: List[Any]):
    """Generic handler for all OSC paths (addresses)."""
    
    fileString = unused_addr.replace('/','_')
    
    n_arguments = len(oscArgs)
    
    f = open(args.outpath + fileString, 'a')

    timeStamp = client.transport_frame / client.samplerate;
        
    f.write('%.4f' % (timeStamp))    
    f.write("\t")

    f.write(unused_addr)       
        
    for i in range(n_arguments):

        f.write("\t")
        
        tmpArg = oscArgs[i]
        
        print(type(tmpArg))
  
        f.write(str(tmpArg))
        
        
    f.write("\n")
        
##############################################################################
##############################################################################
    
    
if __name__ == "__main__":
    
     
  client = jack.Client('osc-recorder')

  client.activate();
  
  #client.inports.register('input_1')
  
  parser = argparse.ArgumentParser()        
  parser.add_argument("--outpath",
                      default ="posis",help="filename for ouput")
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  if not os.path.exists(args.outpath):
    os.makedirs(args.outpath)
    
  
  dispatcher = dispatcher.Dispatcher()  
  
  dispatcher.map("/*", generic_handler)
  
  dispatcher.map("/gain/", volume_handler )
  
  dispatcher.map("/WONDER/source/position", handler_wonder )
  
  for i in range(1,64):
      
      tmpStr = "/track/"+str(i)+"/azim"
      dispatcher.map(tmpStr, handler_polar_single)
    
      tmpStr = "/track/"+str(i)+"/dist"
      dispatcher.map(tmpStr, handler_polar_single)
      
      tmpStr = "/track/"+str(i)+"/elev"
      dispatcher.map(tmpStr, handler_polar_single)
      
  
  server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
    
  positions = []
  
  server.serve_forever()
  
#  while True:
      
      # for debugging: output jack clock
 #         print(client.transport_frame / client.samplerate)
