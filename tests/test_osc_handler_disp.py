
from osc_handler3 import osc_handler
from multiprocessing import Process
import time

osc1 = osc_handler()
osc1.set_sendport(41811)
osc1.act_dispatcher()