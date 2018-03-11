"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import jack

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel,
                                                         QGridLayout, QVBoxLayout, QHBoxLayout,
                                                         QApplication)

from pythonosc import dispatcher
from pythonosc import osc_server

  ##############################################################################
  ##############################################################################
  


def volume_handler(unused_addr, ch1, ch2, gain, timestamp):
    
  f = open('gains', 'a')
  f.write("gain")
  f.write("\t")
  f.write(str(timestamp))
  f.write("\t")
  f.write(str(ch1))
  f.write("\t") 
  f.write(str(ch2))
  f.write("\t")
  f.write(str(gain))
  f.write("\n")
    
#------------------------------------------------------------------------------

def position_handler(unused_addr, ID, x, y, timestamp):
   
  f = open('positions', 'a')
  f.write("position")
  f.write("\t")
  f.write(str(timestamp))
  f.write("\t")
  f.write(str(ID))
  f.write("\t")
  f.write(str(x))
  f.write("\t")
  f.write(str(y))
  f.write("\n")
  
  
##############################################################################
##############################################################################
  
if __name__ == "__main__":
    
     
  client = jack.Client('MyGreatClient')
  
  client.activate();
  #client.inports.register('input_1')
  
  parser = argparse.ArgumentParser()        
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5001, help="The port to listen on")
  args = parser.parse_args()
  
  dispatcher = dispatcher.Dispatcher()
  

  
  dispatcher.map("/gain/", volume_handler )
  
  dispatcher.map("/source/position", position_handler )
  
  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  
  #server.serve_forever()
  
  while True:
      
      # for debugging: output jack clock
          print(client.transport_frame / client.samplerate)