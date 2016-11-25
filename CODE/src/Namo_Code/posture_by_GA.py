### global import ###
import random
import math
import time
import numpy as np
import scipy
import os.path
from copy import deepcopy
from operator import itemgetter


### local import ###
from utility_function import*

### global variables ###
angle_limit = [[0,135],[-90,0],[-45,45],[0,135],[-90,90],[-50,45],[-45,45]]
score_weight = [1,0.001,0.001]

random_amount = 1000
crossover_amount = 980
mutation_amount = 10
reproduction_amount = 10
GA_loop_amount = 10

### add postures ###
## original posture ##
wai_posture_config =        [25,    -5,     -45,    100,    0,      -40,    45,     207,-54,-105,'close']
respect_posture_config =    [80,    -45,    -10,    135,    45,     0,      0,      85,-207,131,'close']
bye_posture_config =        [25,    -20,    0,      110,    -90,    -50,    -15,    229,-229,-34,'open']
rightInvite_posture_config =[10,    -10,    45,     60,     45,     0,      0,      218,-102,-96,'close']

original_posture_config = []
original_posture_config.append(wai_posture_config)
original_posture_config.append(respect_posture_config)
original_posture_config.append(bye_posture_config)
original_posture_config.append(rightInvite_posture_config)

### cal average angle ###
avg_angle = cal_Avg_Angle(original_posture_config,7)

print 'avg =', avg_angle


print "time start",time.clock()


### random posture ###
random_angle_set = random_Posture_Angles(angle_limit,7,random_amount)

### set fix angle ###  all 7 angles
random_angle_set_fixed =[]
for index in range(len(avg_angle)):
    random_angle_set_fixed.append(set_FixAngleValueToData(random_angle_set,index,avg_angle[index]))
#print random_angle_set_fixed[0]

### cal score ###
random_angle_set_fixed_scored_byRefPosture = []
for i_posture in range(len(original_posture_config)):
    random_angle_set_fixed_scored =[]
    for i_angle in range(len(random_angle_set_fixed)):
        random_angle_set_fixed_scored.append(cal_Posture_Score(random_angle_set_fixed[i_angle],original_posture_config[i_posture],score_weight))

    random_angle_set_fixed_scored_byRefPosture.append(random_angle_set_fixed_scored)


### sort data ###
random_angle_set_fixed_scored_byRefPosture_sorted = deepcopy(random_angle_set_fixed_scored_byRefPosture)
for i_posture in range(len(original_posture_config)):
    for i_angle in range(len(random_angle_set_fixed)):
        random_angle_set_fixed_scored_byRefPosture_sorted[i_posture][i_angle].sort(key=itemgetter(10))
        saveDataToFile('./GA_data/'+str(random_amount)+'_random_angle_set_fixed_scored_byRefPosture_sorted['+str(i_posture)+']['+str(i_angle)+'].txt',random_angle_set_fixed_scored_byRefPosture_sorted[i_posture][i_angle])


data_GA_input = deepcopy(random_angle_set_fixed_scored_byRefPosture_sorted)


print "finished random ",random_amount,time.clock()

# test GA looping ##
for i in range(GA_loop_amount):
    data_GA_output = run_GA_Scored_Sorted(data_GA_input,original_posture_config,angle_limit,score_weight,crossover_amount,mutation_amount,reproduction_amount,i)
    data_GA_input = deepcopy(data_GA_output)
    print "finished generation ",i,time.clock()








print "time finish",time.clock()