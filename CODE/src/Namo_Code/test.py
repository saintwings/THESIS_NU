import random
p = 0.25
j=0
for i in range(1000):
    if(random.random() <= p):
        j += 1

print j