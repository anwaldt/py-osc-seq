
import numpy as np
import math

from OscConnect import OscSender
from pythonosc import osc_message_builder as omb



class OscPlayer:	
    

    
    def __init__(self, id, message):
    
        # states
        # 0 = off
        # 1 = play
        # 2 = record
        
        self.state = "OFF";
    
        self.message = message;
    
        self.t  = []
        self.x  = []
        self.y  = []
        self.z  = []
        
        self.values = []
        
        self.azim = []
        self.dist = []
        self.elev = []
    
    # recording buffers
        self.t_IN  = []
        self.x_IN  = []
        self.y_IN  = []
        self.z_IN  = []
    
        self.ID = id
         
        
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
        
       
       
        print("datapoints: "+str(np.size(self.t)))
      
 
        
    def JackPosChange(self, jackPos, osc_client):
   
        
        print('Jack position change reached source '+self.ID.__str__())
        
        
        
        tmpIdx = np.argmin(np.abs( np.subtract(self.t , jackPos)))
                 

        #print("Temp index: "+str(tmpIdx))   

       
        X = self.x[tmpIdx]
        Y = self.y[tmpIdx]
        
   
        
       # r = np.sqrt(X*X+Y*Y)
        
       # azimuth = np.tanh(Y/X)*(180/math.pi)
        
        
        msg = omb.OscMessageBuilder(address="/track/"+str(self.ID)+"/azim")        
        msg.add_arg(azimuth)          
        msg=msg.build()
        osc_client.SendMsg(msg)
        
        msg = omb.OscMessageBuilder(address="/track/"+str(self.ID)+"/dist")        
        msg.add_arg(r)          
        msg=msg.build()

                
        osc_client.SendMsg(msg)
        
        
    def ChangeState(self, msg):
        
    
        #s = self.f(msg)

#        if msg=="OFF":
#            
#        if msg=="R":
#         
#        if msg=="W":
            
        self.state = msg;
        
        print('CHANGED: '+ self.state)

    
                
    
    