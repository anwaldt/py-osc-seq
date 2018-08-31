
import numpy as np

class OscPlayer:	
    
    

    
    # value vectors
    t  = [];
    x  = [];
    y  = [];
    
    # recording buffers
    t_IN  = [];
    x_IN  = [];
    y_IN  = [];
    
    
    
    isrecording = 0;
    isplaying   = 0;
    
    def __init__(self, oscf,id):
        
        self.ID = id
         
        self.OscFile = oscf
        
        
        print(oscf)
            
        positions  = np.loadtxt(oscf, delimiter='\t', usecols=(1,2,3,4))
    
        self.t.append(positions[:,0])
        #self.tID.append(positions[:,1])
        self.x.append(positions[:,2])
        self.y.append(positions[:,3])
        
        
    def JackPosChange(self):
        
        print('pos change')
        
        