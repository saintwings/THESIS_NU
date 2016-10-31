import random
def weighted_random(weights):
    number = random.random() * sum(weights.values())
    for k,v in weights.iteritems():
        if number < v:
            break
        number -= v
    return k

# # the following values can be any non-negative numbers, no need of sum=100
# weights = {1: (0.16),
#            2: (0.33),
#            3: (0.5)}
#
# for i in xrange(12):
#     print weighted_random(weights),
#
# # n(n+1)/2
# print "\n", 10*(10+1)/2
#
# print weights
#
# weights.clear()
ww ={}
n = 100
n_amount = n*(n+1)/2
print n_amount
for i in range(n) :
    print i
    ww[i] = (float(n-i))/n_amount

print ww
print len(ww)
print ww[1]

for i in xrange(12):
     print weighted_random(ww),