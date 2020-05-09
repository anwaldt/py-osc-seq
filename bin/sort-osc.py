#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 09:25:19 2017

@author: anwaldt
"""

########################################################################################
# Start Stuff
########################################################################################

import numpy as np
 
   
from os import listdir
from os.path import isfile, join


import argparse


########################################################################################
# 
########################################################################################

def sort_osc(oscPath):
    
    
    
    ########################################################################################
    # 
    ########################################################################################
     
      
    
    oscFiles = [f for f in listdir(oscPath) if isfile(join(oscPath, f))]
     
    
    N = len(oscFiles)
    
    t=[]
    ID = []
    x=[]
    y=[]
    
    for i in oscFiles:
        
        print(["loading".__add__(i)])
    
        positions  = np.loadtxt(oscPath.__add__(i), delimiter='\t', usecols=(1,2,3,4))
    
        t.append(positions[:,0])
        ID.append(positions[:,1])
        x.append(positions[:,2])
        y.append(positions[:,3])
    
        t2 = 
    
        
    
    
    print('All files read!')
     
     
########################################################################################
# 
########################################################################################



if __name__== "__main__":
  parser = argparse.ArgumentParser()        
  parser.add_argument("--oscpath",
                      default =".",help="The osc-path")
  
  args = parser.parse_args()
    
  sort_osc(args.oscpath)
        