# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:06:37 2018

@author: jj
"""

from osc_handler3 import osc_handler
from multiprocessing import Process
import time

def p1(osc1):
	osc1.alive()
def p2(osc1):
	osc1.read_send()
def p3(osc1):
	osc1.create_sources(3,1.0)
def p4(osc1):
	osc1.receive_write()

osc1 = osc_handler()
osc1.act_send()
osc1.act_jack_play()
osc1.act_dispatcher()
osc1.subscribe()
osc1.message_level(3)

pp1 = Process(target=p1, args=(osc1,))
pp1.start()
pp3 = Process(target=p3, args=(osc1,))
pp3.start()
pp2 = Process(target=p2, args=(osc1,))
#time.sleep(2)
pp2.start()
#pp4 = Process(target=p4, args=(osc1,))
#pp4.start()

pp1.join()
pp3.join()
pp2.join()
#pp4.join()






#osc1.alive()
#osc1.read_send()
#osc1.poll()
#osc2 = osc_handler("127.0.0.1", 54533, 50002)
#osc2.act_send()
#osc2.alive()