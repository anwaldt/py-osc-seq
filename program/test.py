from filehandler import filehandler, parser
from multiprocessing import Process


def p1(t):
	t.send_alive_messages()
def p2(t):
	t.play()



test1 = filehandler()
test1.read_all()

print(test1.x)


test2 = parser(test1)
test2.change_renderer(1)
test2.connect()

pp1 = Process(target=p1, args=(test2,))
pp1.start() #send alive messages

test2.create_sources()
test2.start_jack()

pp2=Process(target=p2, args=(test2,))
pp2.start()


