
import numpy as np
import math

from OscConnect import OscSender
from pythonosc import osc_message_builder as omb



class OscPlayer:	
    

    
    def __init__(self, id):
    
        self.isrecording = 0;
        self.isplaying   = 0;
    
    
        self.t  = []
        self.x  = []
        self.y  = []
    
    # recording buffers
        self.t_IN  = []
        self.x_IN  = []
        self.y_IN  = []
    
        self.ID = id
         
        
    def LoadFile(self, oscf):
        
        self.OscFile = oscf
         
        print("Loading data from: ".__add__(oscf))
            
        positions  = np.loadtxt(oscf, delimiter='\t', usecols=(1,2,3,4))
    
        self.t = positions[:,0]
        #self.tID.append(positions[:,1])
        self.x = positions[:,2]
        self.y = positions[:,3]
        
        print("datapoints: "+str(np.size(self.t)))
      
 
        
    def JackPosChange(self, jackPos, osc_client):
        
     
        

         
        tmpIdx = np.argmin(np.abs( np.subtract(self.t , jackPos)))
                 

        #print("Temp index: "+str(tmpIdx))   

       
        X = self.x[tmpIdx]
        Y = self.y[tmpIdx]
        
   
        
        r = np.sqrt(X*X+Y*Y)
        
        azimuth = np.tanh(Y/X)*(180/math.pi)
        
        
        msg = omb.OscMessageBuilder(address="/track/"+str(self.ID)+"/azim")        
        msg.add_arg(azimuth)          
        msg=msg.build()
        osc_client.SendMsg(msg)
        
        msg = omb.OscMessageBuilder(address="/track/"+str(self.ID)+"/dist")        
        msg.add_arg(r)          
        msg=msg.build()

                
        osc_client.SendMsg(msg)
        
        