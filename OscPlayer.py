
import numpy as np
import math 
 

from OscConnect import OscSender
from pythonosc import osc_message_builder as omb
from pythonosc import dispatcher
from pythonosc import osc_server

 

class OscPlayer:	
    

    
    def __init__(self, id, message):
    
        self.state = "OFF";
    
        
        # use the filename to select the data type
        # mainPath can then be used to decide what to do
                
        first = message.split('_') 
        self.mainPath =  first[0]        
        print('Main path of this file is: '+self.mainPath)
        
        # this array is needed in any case
        self.t  = []
        
        # these are used for Panoramix
        self.values = []
        self.paths  = []
        
        # these arrays are used for WONDER
        self.id = []
        self.x  = []
        self.y  = []
        self.dt = []
        
     
        """TODO: Redording buffers"""
    
        self.ID = id
         
        self.disp = dispatcher.Dispatcher()  

        
    def LoadFile(self, oscf):
        
        self.OscFile = oscf         
        print("Loading data from: ".__add__(oscf))
            
        data  = np.loadtxt(oscf, delimiter='\t', usecols=(0,2))
  
        self.t      = data[:,0]
        
        
#        self.paths.append(data[:,1])
        self.values = data[:,1]

       # #self.tID.append(data[:,1])
       # self.x = data[:,2]
       # self.y = data[:,3]
        
       
        self.t_start = self.t[0]
       
       
        
        
        with open(oscf, "r+") as f:
            
            data = f.readlines()
            
            count = 0
            
            for line in data:
                
                [d1, path, d2] =  line.split('\t')
                self.paths.append(path)
                
                 
                self.t[count] =  self.t[count]-self.t_start


                print(self.t[count])
                
                count+=1

                 
    
        
        print("datapoints: "+str(np.size(self.t)))
 
       
        
        
                
       # self.disp.map(self.paths[0], self.handler_polar_single)        
       # server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 5005), dispatcher)
       # print("Serving on {}".format(server.server_address))
        
    def JackPosChange(self, timeVal, osc_client):
      
        tmpIdx = np.argmin(np.abs( np.subtract(self.t , timeVal)))
       
        #X = self.x[tmpIdx]
        #Y = self.y[tmpIdx]
        
        
        
       # r = np.sqrt(X*X+Y*Y)
        
       # azimuth = np.tanh(Y/X)*(180/math.pi)
        
        
       
        outPath = self.paths[tmpIdx] 
        
    
        msg = omb.OscMessageBuilder(address=outPath)  

        
            
        
        outVal  = self.values[tmpIdx]                              
            
        msg.add_arg(outVal)          

         
      

        msg     = msg.build()
        osc_client.send(msg)
 
        
    def ChangeState(self, msg):
        
        #s = self.f(msg)

#        if msg=="OFF":
#            
#        if msg=="R":
#         
#        if msg=="W":
            
        self.state = msg;
        
        print('CHANGED: '+ self.state)

    
      
      
    def handler_polar_single(self, unused_addr, value):
        #
        """ Designed to process PanoramixApp messages. """
        [o, t, i, p] = unused_addr.split("/")
        
        self.t.append()
         