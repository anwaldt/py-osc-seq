# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 12:11:27 2018

@author: jj
"""

from osc_handler2 import osc_handler
from tkinter import *
from IPython import get_ipython
from subprocess import call

# WHY DOES THIS NOT WORK PROPERLY?
#def ssr_start():
#    call(["ssr-binaural","-vvv"])
    
def initialize(osc):

    osc.activate()
    msg1.config(text="Connected with SSR")
    
def create_sources(osc):
    sn = sourcenumber.get()
    dst = distance.get()
    osc.create_sources(int(sn), int(dst))
    msg2.config(text="Created " + str(sn) +" sources")
def delete_source(osc):
    sID =0
    if sID == 0:
        for i in range(osc.max_sourceID, 1):
            osc.delete_source(i)
    else:
        osc.delete_source(int(sID))
   
    
def record(osc):
    osc.receive_write()
    msg3.config(text="recording...")
    

win = Tk()

win.title("Controlling SSR with OSC")


osc1 = osc_handler()

sourcenumber = Entry(win, bd=5, width=8)
distance = Entry(win, bd=5, width=8)
sourceID = Entry(win, bd=5, width=8)


startssr = Button(win, text="start SSR", command= lambda: ssr_start())
connect = Button(win, text="connect", command= lambda: initialize(osc1))
msg1 = Label(win)
sources = Button(win, text="create sources", command= lambda: create_sources(osc1))
msg2 = Label(win)
labelsn = Label(win, text="how many")
labeldst = Label(win, text="how far away")
recording = Button(win, text="record", command= lambda: record(osc1))
msg3 = Label(win)
deleting = Button(win, text="delete sources", command= lambda: delete_source(osc1))

startssr.grid(row=0, column=0)
connect.grid(row=1, column=0)
msg1.grid(row=1, column=3)
sources.grid(row=3, column=0)
labelsn.grid(row=2, column = 1)
labeldst.grid(row=2, column =2)
sourcenumber.grid(row=3, column=1)
distance.grid(row=3, column = 2)
msg2.grid(row=3, column=3)
recording.grid(row=5,column=0)
msg3.grid(row=4, column=1)
deleting.grid(row=4, column=0)




#win.mainloop()