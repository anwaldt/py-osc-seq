#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 09:25:19 2017

@author: anwaldt
"""

########################################################################################
# Start Stuff
########################################################################################

import argparse
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

def plot_position_xy(sourceID,startIDX,stopIDX):
        
    mpl.style.use('default')
    fig, ax1 = mpl.subplots()
    
    ax1.set_xlabel('x')
    ax1.set_ylabel('y' ,color = [ 0.3, 0.3, 0.3])
    
     
    
    # Does not work for long trajectories
    #for i in range(N-1):
    #    colIDX = i/N
        
   #     ax1.plot(newAR[i:i+2,2], newAR[i:i+2,3], linewidth=0.75, color= mpl.cm.jet(colIDX))
        
    ax1.plot(newAR[startIDX:stopIDX,2], newAR[startIDX:stopIDX,3], linewidth=0.75)
    
   # ax1.plot(newAR[startIDX:stopIDX,0], newAR[startIDX:stopIDX,3], linewidth=0.75)
    
    fig.savefig(args.infile + '_XY_' + '.pdf')
    
    return 0
   
def plot_position_X(newAR, startIDX,stopIDX):
         
    mpl.style.use('default')
    fig, ax1 = mpl.subplots()
    
    ax1.set_xlabel('t')
    ax1.set_ylabel('x' ,color = [ 0.3, 0.3, 0.3])
    
    
    ax1.plot(newAR[startIDX:stopIDX,0], newAR[startIDX:stopIDX,2], linewidth=0.75)
    
    fig.savefig(args.infile + '_X_' + '.pdf')

    return 0


   
def plot_position_Y(newAR, startIDX,stopIDX):
            
    mpl.style.use('default')
    fig, ax1 = mpl.subplots()
    
    ax1.set_xlabel('t')
    ax1.set_ylabel('x' ,color = [ 0.3, 0.3, 0.3])
    
    
    ax1.plot(newAR[startIDX:stopIDX,0], newAR[startIDX:stopIDX,3], linewidth=0.75)
    
    fig.savefig(args.infile  + '_Y_' + '.pdf')

    return 0
########################################################################################
# 
########################################################################################


if __name__ == "__main__":

    parser = argparse.ArgumentParser()        
    parser.add_argument("--infile",
                      help="filename for plot")
    
    parser.add_argument("--p1")
    parser.add_argument("--p2")
    
    
    args = parser.parse_args()


    posFile     = args.infile
    
    positions   = np.loadtxt(posFile, delimiter='\t', usecols=(1,2,3,4))

    newAR       = positions;   
    #newAR = newAR[startIDX:stopIDX,:]    

    N = len(newAR)
    
    #plot_position_xy(2,-1,-1)

    plot_position_X(newAR, -1,-1)
