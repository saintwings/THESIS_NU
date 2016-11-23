from utility_function import*
import time
wai_posture_config = [25, -5, -45, 100, 0, -40, 45, 207, -54, -105, 'close']
for i in range(20):
    t1 = time.clock()
    a = calKinematicNamo_numpy(wai_posture_config ,'R')
    t2 = time.clock()
    b = calKinematicNamo(wai_posture_config ,'R')
    t3 = time.clock()
    print a[1]
    print ("numpy t =" +str(t2 -t1))
    print b[1]
    print ("sympy t =" +str(t3 -t2))