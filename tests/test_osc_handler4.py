# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:06:37 2018

@author: jj
"""

from osc_handler4 import osc_handler
from multiprocessing import Process
import time

def p1(osc1):
	osc1.socket_receive()	
def p2(osc1):
	osc1.socket_alive()
def p3(osc1):
	osc1.socket_read_send()

osc1 = osc_handler()
osc1.act_jack_play()
osc1.udp_socket()
osc1.socket_subscribe()
osc1.socket_message_level(3)
osc1.socket_create_sources(3,1.0)
pp1 = Process(target=p1, args=(osc1,))
pp1.start()
pp2 = Process(target=p2, args=(osc1,))
pp2.start()
pp3 = Process(target=p3, args=(osc1,))
pp3.start()
