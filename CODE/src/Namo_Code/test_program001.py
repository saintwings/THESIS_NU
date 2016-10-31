__author__ = 'SaintWingZ'
from operator import itemgetter
b=[[1,4,7],[4,3,2],[9,5,1]]
b.sort(key=itemgetter(0))
print b

b.sort(key=itemgetter(1))
print b
b.sort(key=itemgetter(2))
print b

a=[1,2,3]

b.append(a)
print b
print b[1][1]