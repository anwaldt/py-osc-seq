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
import matplotlib.pyplot as mpl
 
########################################################################################
# READ FILEs
########################################################################################



########################################################################################
# PLOT Amplitudes
########################################################################################

def plot_apmlitudes(sourceID):
    
    AmpFile = 'gains' 
    
    #amplitudes = np.loadtxt(AmpFile, dtype='d', delimiter='\t')
    
    
    
    amplitudes  = np.loadtxt(AmpFile, delimiter='\t', usecols=(1,2,3,4))
    
    paths       = np.genfromtxt(AmpFile ,usecols=(0) ,dtype='str')
    
    #mpl.style.use('default')
    #fig, ax1 = mpl.subplots()
    #ax1.set_xlabel('frame')
    #ax1.set_ylabel('Partial amplitudes' ,color = [ 0.3, 0.3, 0.3])
    #ax1.plot(amplitudes[:10,1],  label='P_1', linewidth=0.5)
 
 


########################################################################################
# PLOT Amplitudes
########################################################################################

def plot_position(sourceID,startIDX,stopIDX):

    
    
    posFile = 'pos-2' 

    #amplitudes = np.loadtxt(AmpFile, dtype='d', delimiter='\t')
    
    
    
    positions  = np.loadtxt(posFile, delimiter='\t', usecols=(1,2,3,4))
    #paths      = np.genfromtxt(posFile ,usecols=(0) ,dtype='str')
    
#    
#    sourceIDS  = positions[:,1]
#    idxs       = np.where(sourceIDS == sourceID)
#    newAR      = positions[idxs[0],:]    
#    
    newAR = positions;
    
    mpl.style.use('default')
    fig, ax1 = mpl.subplots()
    
    ax1.set_xlabel('x')
    ax1.set_ylabel('y' ,color = [ 0.3, 0.3, 0.3])
    
    #newAR = newAR[startIDX:stopIDX,:]    
    N = len(newAR)
    
    if startIDX == -1:
        startIDX = 0
        
    if stopIDX == -1:
        stopIDX = N
    
    # Does not work for long trajectories
    #for i in range(N-1):
    #    colIDX = i/N
        
   #     ax1.plot(newAR[i:i+2,2], newAR[i:i+2,3], linewidth=0.75, color= mpl.cm.jet(colIDX))
        
    ax1.plot(newAR[startIDX:stopIDX,2], newAR[startIDX:stopIDX,3], linewidth=0.75)
    
   # ax1.plot(newAR[startIDX:stopIDX,0], newAR[startIDX:stopIDX,3], linewidth=0.75)
    
    fig.savefig("aa.pdf")
    
    return 0;
   
########################################################################################
# 
########################################################################################


plot_position(2,-1,-1)

