from classes import filehandler, parser
from multiprocessing import Process
import time


def p1(t):
	t.send_alive_messages()
def p2(t):
	t.play()



test1 = filehandler()
test1.read_all()



test2 = parser(test1)
#test2.change_renderer(1)
#test2.connect()
#pp1 = Process(target=p1, args=(test2,))
#pp1.start() #send alive messages

#test2.create_sources()
test2.start_jack()
#print(test2.jclient.transport_frame)
#test2.jclient.transport_start()
#time.sleep(0.5)
#print(test2.jclient.transport_frame)


#pp2=Process(target=p2, args=(test2,))
#pp2.start()
test2.sources_to_play = [1,1,1]
test2.prepare_play()
test2.play()


