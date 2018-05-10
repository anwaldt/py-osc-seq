list1 =[1,3,6,2]
list2 = [1,2,3,4]
list3 = [0,1,2,3]
list1,list2,list3 = (list(k) for k in zip(*sorted(zip(list1,list2,list3))))
print(list1)
print(list2)
print(list3)

list4 = [1,7,8]
if 4 in list4:
	print('la')