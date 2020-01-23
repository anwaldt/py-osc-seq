#!/usr/bin/python3

""" OSC Recorder for writing any incoming massages to text files!"""

__author__ = "Henrik von Coler"
__date__   = "2019-06-07"

import time

import argparse
import jack
import os
 
from pythonosc import dispatcher
from pythonosc import osc_server

from typing import List, Any

from OscRecorder import OscRecorder
 
   


        
    
###############################################################################
###############################################################################
#
#def volume_handler(unused_addr, ch1, ch2, gain, timestamp):
#    
#  f = open('gains', 'a')
#  f.write("gain")
#  f.write("\t")
#  #f.write(str(timestamp))
#  f.write(str(client.transport_frame / client.samplerate))
#  f.write("\t")
#  f.write(str(ch1))
#  f.write("\t") 
#  f.write(str(ch2))
#  f.write("\t")
#  f.write(str(gain))
#  f.write("\n")
#    
##------------------------------------------------------------------------------
#
#def handler_wonder(unused_addr, ID, x, y, duration):
#
#  tmpName = args.outpath + "WONDER_" + str(ID) + "_cartesian" + ".osc";
#  
#  f       = open(tmpName, 'a')
#  
#  timeStamp = client.transport_frame / client.samplerate;
#
#  f.write('%.4f' % (timeStamp))
#  f.write("\t")
#
#  f.write(unused_addr)
#  f.write("\t")
#  
#  f.write(str(ID))
#  f.write("\t")
#
#  f.write('%.4f' % (x))
#  f.write("\t")
#
#  f.write('%.4f' % (y))
#  f.write("\t")
#
#  f.write('%.4f' % (duration))
#  f.write("\n")
#    
##------------------------------------------------------------------------------
#  
#def handler_polar_single(unused_addr, value):
#    #
#    """ Designed to process PanoramixApp messages. """
#    
#    [o, t, i, p] = unused_addr.split("/")
#    
#    tmpName = "track_"+str(i)+'_'+str(p)+".osc";
#    f       = open(args.outpath + tmpName, 'a')
#
#    timeStamp = client.transport_frame / client.samplerate;
#
#    f.write('%.4f' % (timeStamp))
#    f.write("\t")
#
#    f.write(unused_addr)
#    f.write("\t")
#  
#    f.write(str(value))
#    f.write("\n")
#

        
##############################################################################
##############################################################################
    
    
if __name__ == "__main__":
    

  parser = argparse.ArgumentParser()        

  parser.add_argument("--timer", default ="unix",help="chose timer mode")
  parser.add_argument("--outpath", default ="posis",help="filename for ouput")
  parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
  
  args = parser.parse_args()


  
  r = OscRecorder(args.timer)
  r.start_server(args.ip, args.port, args.outpath)
  
#  dispatcher = dispatcher.Dispatcher()  
#  
#  dispatcher.map("/*", generic_handler )
#  
#  server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
#  
#  print("Serving on {}".format(server.server_address))  
#  
#  server.serve_forever()
  
