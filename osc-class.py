

class OscPlayer:

    from pythonosc import udp_client
    from pythonosc import osc_message_builder as omb
    
    
    # value vectors
    t  = [];
    ID = [];
    x  = [];
    y  = [];
    
    isrecording = 0;
    isplaying   = 0;
    
    def __init__(self, id):
        
        self.ID = id
        
        
        