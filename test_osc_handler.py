# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:06:37 2018

@author: jj
"""

from osc_handler3 import osc_handler
import time

osc1 = osc_handler()
osc1.act_send()
osc1.poll()
time.sleep(1)
osc1.create_sources(3,1.0)
#osc1.subscribe()
#osc1.alive()

#osc1.create_sources(3,1.0)
#osc2 = osc_handler("127.0.0.1", 50002, 50002)
#osc2.act_send()
#osc2.alive()