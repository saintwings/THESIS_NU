import random
import time


print str(time.asctime())

fileName = "./BFOA_data/"+str(time.asctime())+"aaa2222test.txt"
print fileName
file_data = open(fileName, 'w')
file_data.write("aaaaaa")
file_data.close()