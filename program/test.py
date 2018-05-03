from filehandler import filehandler, parser

test1 = filehandler()
test1.read_all()

test2 = parser(test1)
test2.test()