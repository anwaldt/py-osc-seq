#!/usr/bin/python3

""" Main file for starting an OSC recorder from command line!"""

__author__ = "Henrik von Coler"
__date__   = "2019-06-07"

 
import argparse


from OscRecorder import OscRecorder

        
##############################################################################
##############################################################################
    
    
if __name__ == "__main__":
    

  parser = argparse.ArgumentParser()        

  parser.add_argument("--timer", default ="unix",help="chose timer mode")
  parser.add_argument("--outpath", default ="test-record",help="filename for ouput")
  parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
  
  args = parser.parse_args()


  
  r = OscRecorder(args.timer)
  r.start_server(args.ip, args.port, args.outpath)

