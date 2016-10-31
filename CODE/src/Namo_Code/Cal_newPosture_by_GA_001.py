"""
code for test generate new Namo's posture by GA method
"""

import random
from sympy import symbols, Matrix, Symbol, exp, sin, cos, sqrt, diff
import math
import time
#from visual import *
#from visual.controls import *

import numpy as np
#from scipy.linalg import norm
#from scipy import linalg as LA
import scipy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from operator import itemgetter
from copy import deepcopy
from utility_function import*

import os.path


def Cal_posture_by_random(prefix_file_name,loop_amount):
    TMatrix_Target_Posture = []
    Q_ref = []
    dataAll = []
    dataSet = []
    for i in range(0,len(original_posture_config)):
        TMatrix_Target_Posture.append(calKinematicNamo(original_posture_config[i],'R'))
        Q_ref.append(calQuaternion(TMatrix_Target_Posture[i][7]))
        dataSet.append([])
    print len(original_posture_config)
    print len(TMatrix_Target_Posture)
    print len(Q_ref)



    print "time start",time.clock()


    for i in range (0,loop_amount):
        #if i%1000 == 0:
        #    print i
        random_angle = [random.randint(angle1_limit[0],angle1_limit[1]),
                          random.randint(angle2_limit[0],angle2_limit[1]),
                          random.randint(angle3_limit[0],angle3_limit[1]),
                          random.randint(angle4_limit[0],angle4_limit[1]),
                          random.randint(angle5_limit[0],angle5_limit[1]),
                          random.randint(angle6_limit[0],angle6_limit[1]),
                          random.randint(angle7_limit[0],angle7_limit[1])
                          ]
        T_Matrix = calKinematicNamo(random_angle,'R')
        Q = calQuaternion(T_Matrix[7])
        Q_diff =[]
        norm_Q_diff = []
        elbow_diff =[]
        norm_elbow_diff =[]
        wrist_diff = []
        norm_wrist_diff = []
        sum_diff =  []
        diff_all_post = []
        for j in range(0,len(original_posture_config)):
            Q_diff.append([Q_ref[j][0]-Q[0],Q_ref[j][1]-Q[1],Q_ref[j][2]-Q[2],Q_ref[j][3]-Q[3]])
            norm_Q_diff.append(math.sqrt((Q_diff[j][0]*Q_diff[j][0])+(Q_diff[j][1]*Q_diff[j][1])+(Q_diff[j][2]*Q_diff[j][2])+(Q_diff[j][3]*Q_diff[j][3])))
            elbow_diff.append([TMatrix_Target_Posture[j][3][0,3] - T_Matrix[3][0,3],TMatrix_Target_Posture[j][3][1,3] - T_Matrix[3][1,3],TMatrix_Target_Posture[j][3][2,3] - T_Matrix[3][2,3]])
            norm_elbow_diff.append(math.sqrt(pow(TMatrix_Target_Posture[j][3][0,3] - T_Matrix[3][0,3],2)+pow(TMatrix_Target_Posture[j][3][1,3] - T_Matrix[3][1,3],2)+pow(TMatrix_Target_Posture[j][3][2,3] - T_Matrix[3][2,3],2)))
            wrist_diff.append([TMatrix_Target_Posture[j][4][0,3] - T_Matrix[4][0,3],TMatrix_Target_Posture[j][4][1,3] - T_Matrix[4][1,3],TMatrix_Target_Posture[j][4][2,3] - T_Matrix[4][2,3]])
            norm_wrist_diff.append(math.sqrt(pow(TMatrix_Target_Posture[j][4][0,3] - T_Matrix[4][0,3],2)+pow(TMatrix_Target_Posture[j][4][1,3] - T_Matrix[4][1,3],2)+pow(TMatrix_Target_Posture[j][4][2,3] - T_Matrix[4][2,3],2)))
            sum_diff.append(norm_Q_diff[j]*score_weight[0] +   norm_elbow_diff[j]*score_weight[1] +   norm_wrist_diff[j]*score_weight[2])

            dataAdd=[random_angle[0],random_angle[1],random_angle[2],random_angle[3],random_angle[4],random_angle[5],random_angle[6],
                     norm_Q_diff[j], norm_elbow_diff[j], norm_wrist_diff[j],sum_diff[j]]

            dataSet[j].append(dataAdd)
            diff_all_post.append(sum_diff[j])

        dataAdd_to_All = [random_angle[0],random_angle[1],random_angle[2],random_angle[3],random_angle[4],random_angle[5],random_angle[6],
                            diff_all_post,sum(diff_all_post)]
        dataAll.append(dataAdd_to_All)

    print "time finish",time.clock()
    saveDataToFile(str(prefix_file_name)+"7DOF_Q_All.txt",dataAll)
    dataAll.sort(key=itemgetter(8))
    saveDataToFile(str(prefix_file_name)+"7DOF_Q_All_sorted.txt",dataAll)
    for i in range(0,len(original_posture_config)):
        saveDataToFile(str(prefix_file_name)+"7DOF_Q" + str(i) +".txt",dataSet[i])
        dataSet[i].sort(key=itemgetter(10))
        saveDataToFile(str(prefix_file_name)+"7DOF_Q" + str(i) +"_sorted.txt",dataSet[i])

def Cal_posture_by_random(angle_fixed,angle_fixed_value,prefix_file_name,loop_amount,original_posture_config):
    TMatrix_Target_Posture = []
    Q_ref = []
    dataAll = []
    dataSet = []
    for i in range(0,len(original_posture_config)):
        TMatrix_Target_Posture.append(calKinematicNamo(original_posture_config[i],'R'))
        Q_ref.append(calQuaternion(TMatrix_Target_Posture[i][7]))
        dataSet.append([])
    print len(original_posture_config)
    print len(TMatrix_Target_Posture)
    print len(Q_ref)

    print "time start",time.clock()

    for i in range (0,loop_amount):
        #if i%1000 == 0:
        #    print i
        random_angle = [random.randint(angle_limit[0][0],angle_limit[0][1]),
                          random.randint(angle_limit[1][0],angle_limit[1][1]),
                          random.randint(angle_limit[2][0],angle_limit[2][1]),
                          random.randint(angle_limit[3][0],angle_limit[3][1]),
                          random.randint(angle_limit[4][0],angle_limit[4][1]),
                          random.randint(angle_limit[5][0],angle_limit[5][1]),
                          random.randint(angle_limit[6][0],angle_limit[6][1])
                          ]

        random_angle[angle_fixed] = angle_fixed_value

        #print random_angle

        T_Matrix = calKinematicNamo(random_angle,'R')
        Q = calQuaternion(T_Matrix[7])
        Q_diff =[]
        norm_Q_diff = []
        elbow_diff =[]
        norm_elbow_diff =[]
        wrist_diff = []
        norm_wrist_diff = []
        sum_diff =  []
        diff_all_post = []
        for j in range(0,len(original_posture_config)):
            Q_diff.append([Q_ref[j][0]-Q[0],Q_ref[j][1]-Q[1],Q_ref[j][2]-Q[2],Q_ref[j][3]-Q[3]])
            norm_Q_diff.append(math.sqrt((Q_diff[j][0]*Q_diff[j][0])+(Q_diff[j][1]*Q_diff[j][1])+(Q_diff[j][2]*Q_diff[j][2])+(Q_diff[j][3]*Q_diff[j][3])))
            elbow_diff.append([TMatrix_Target_Posture[j][3][0,3] - T_Matrix[3][0,3],TMatrix_Target_Posture[j][3][1,3] - T_Matrix[3][1,3],TMatrix_Target_Posture[j][3][2,3] - T_Matrix[3][2,3]])
            norm_elbow_diff.append(math.sqrt(pow(TMatrix_Target_Posture[j][3][0,3] - T_Matrix[3][0,3],2)+pow(TMatrix_Target_Posture[j][3][1,3] - T_Matrix[3][1,3],2)+pow(TMatrix_Target_Posture[j][3][2,3] - T_Matrix[3][2,3],2)))
            wrist_diff.append([TMatrix_Target_Posture[j][4][0,3] - T_Matrix[4][0,3],TMatrix_Target_Posture[j][4][1,3] - T_Matrix[4][1,3],TMatrix_Target_Posture[j][4][2,3] - T_Matrix[4][2,3]])
            norm_wrist_diff.append(math.sqrt(pow(TMatrix_Target_Posture[j][4][0,3] - T_Matrix[4][0,3],2)+pow(TMatrix_Target_Posture[j][4][1,3] - T_Matrix[4][1,3],2)+pow(TMatrix_Target_Posture[j][4][2,3] - T_Matrix[4][2,3],2)))
            sum_diff.append(norm_Q_diff[j]*score_weight[0] +   norm_elbow_diff[j]*score_weight[1] +   norm_wrist_diff[j]*score_weight[2])

            dataAdd=[random_angle[0],random_angle[1],random_angle[2],random_angle[3],random_angle[4],random_angle[5],random_angle[6],
                     norm_Q_diff[j], norm_elbow_diff[j], norm_wrist_diff[j],sum_diff[j]]

            dataSet[j].append(dataAdd)
            diff_all_post.append(sum_diff[j])

        dataAdd_to_All = [random_angle[0],random_angle[1],random_angle[2],random_angle[3],random_angle[4],random_angle[5],random_angle[6],
                            diff_all_post,sum(diff_all_post)]
        dataAll.append(dataAdd_to_All)

    print "time finish",time.clock()
    saveDataToFile(str(prefix_file_name)+"7DOF_Q_All.txt",dataAll)
    dataAll.sort(key=itemgetter(8))
    saveDataToFile(str(prefix_file_name)+"7DOF_Q_All_sorted.txt",dataAll)
    for i in range(0,len(original_posture_config)):
        saveDataToFile(str(prefix_file_name)+"7DOF_Q" + str(i) +".txt",dataSet[i])
        dataSet[i].sort(key=itemgetter(10))
        saveDataToFile(str(prefix_file_name)+"7DOF_Q" + str(i) +"_sorted.txt",dataSet[i])



def random_each_posture(ref_posture,flie_load,error_allowance_percentage,loop_amount,prefix_file_name,jointfixed_value):

    data = loadDataFromFile(flie_load)

    angle_limit = [[ref_posture[0],ref_posture[0]],
                   [ref_posture[1],ref_posture[1]],
                   [ref_posture[2],ref_posture[2]],
                   [ref_posture[3],ref_posture[3]],
                   [ref_posture[4],ref_posture[4]],
                   [ref_posture[5],ref_posture[5]],
                   [ref_posture[6],ref_posture[6]]]
    for i in range(7):
        print angle_limit[i]
    print "###"
    not_finished_loop = True
    loop = 0
    score_ref = data[loop][10]
    while(not_finished_loop):

        if((data[loop][10] - score_ref)/score_ref*100 > error_allowance_percentage):
            not_finished_loop = False
        else:
            for i in range(7):
                if(data[loop][i]<angle_limit[i][0]):
                    angle_limit[i][0] = data[loop][i]

                elif(data[loop][i]>angle_limit[i][1]):
                    angle_limit[i][1] = data[loop][i]


            loop = loop+1


    for i in range(7):
        if(jointfixed_value[0] == i):
            angle_limit[i][0] = jointfixed_value[1]
            angle_limit[i][1] = jointfixed_value[1]

    for i in range(7):
        print angle_limit[i]


    original_posture_config = []
    original_posture_config.append(ref_posture)


    TMatrix_Target_Posture = []
    Q_ref = []
    dataAll = []
    dataSet = []
    for i in range(0,len(original_posture_config)):
        TMatrix_Target_Posture.append(calKinematicNamo(original_posture_config[i],'R'))
        Q_ref.append(calQuaternion(TMatrix_Target_Posture[i][7]))
        dataSet.append([])
    print len(original_posture_config)
    print len(TMatrix_Target_Posture)
    print len(Q_ref)


    print "time start",time.clock()

    for i in range (0,loop_amount+1):
        #if i%1000 == 0:
        #    print i
        random_angle = [random.randint(int(round(angle_limit[0][0],0)),int(round(angle_limit[0][1],0))),
                          random.randint(int(round(angle_limit[1][0],0)),int(round(angle_limit[1][1],0))),
                          random.randint(int(round(angle_limit[2][0],0)),int(round(angle_limit[2][1],0))),
                          random.randint(int(round(angle_limit[3][0],0)),int(round(angle_limit[3][1],0))),
                          random.randint(int(round(angle_limit[4][0],0)),int(round(angle_limit[4][1],0))),
                          random.randint(int(round(angle_limit[5][0],0)),int(round(angle_limit[5][1],0))),
                          random.randint(int(round(angle_limit[6][0],0)),int(round(angle_limit[6][1],0)))
                          ]
        if(i == 0):
            random_angle = [ref_posture[0],ref_posture[1],ref_posture[2],ref_posture[3],ref_posture[4],ref_posture[5],ref_posture[6]]
            for j in range(7):
                if(jointfixed_value[0] == j):
                    random_angle[j] = jointfixed_value[1]

        for i in range(7):
            if(jointfixed_value[0] == i):
                random_angle[i] = jointfixed_value[1]





        T_Matrix = calKinematicNamo(random_angle,'R')
        Q = calQuaternion(T_Matrix[7])
        Q_diff =[]
        norm_Q_diff = []
        elbow_diff =[]
        norm_elbow_diff =[]
        wrist_diff = []
        norm_wrist_diff = []
        sum_diff =  []
        diff_all_post = []

        for j in range(0,len(original_posture_config)):
            Q_diff.append([Q_ref[j][0]-Q[0],Q_ref[j][1]-Q[1],Q_ref[j][2]-Q[2],Q_ref[j][3]-Q[3]])
            norm_Q_diff.append(math.sqrt((Q_diff[j][0]*Q_diff[j][0])+(Q_diff[j][1]*Q_diff[j][1])+(Q_diff[j][2]*Q_diff[j][2])+(Q_diff[j][3]*Q_diff[j][3])))
            elbow_diff.append([TMatrix_Target_Posture[j][3][0,3] - T_Matrix[3][0,3],TMatrix_Target_Posture[j][3][1,3] - T_Matrix[3][1,3],TMatrix_Target_Posture[j][3][2,3] - T_Matrix[3][2,3]])
            norm_elbow_diff.append(math.sqrt(pow(TMatrix_Target_Posture[j][3][0,3] - T_Matrix[3][0,3],2)+pow(TMatrix_Target_Posture[j][3][1,3] - T_Matrix[3][1,3],2)+pow(TMatrix_Target_Posture[j][3][2,3] - T_Matrix[3][2,3],2)))
            wrist_diff.append([TMatrix_Target_Posture[j][4][0,3] - T_Matrix[4][0,3],TMatrix_Target_Posture[j][4][1,3] - T_Matrix[4][1,3],TMatrix_Target_Posture[j][4][2,3] - T_Matrix[4][2,3]])
            norm_wrist_diff.append(math.sqrt(pow(TMatrix_Target_Posture[j][4][0,3] - T_Matrix[4][0,3],2)+pow(TMatrix_Target_Posture[j][4][1,3] - T_Matrix[4][1,3],2)+pow(TMatrix_Target_Posture[j][4][2,3] - T_Matrix[4][2,3],2)))
            sum_diff.append(norm_Q_diff[j]*score_weight[0] +   norm_elbow_diff[j]*score_weight[1] +   norm_wrist_diff[j]*score_weight[2])

            dataAdd=[random_angle[0],random_angle[1],random_angle[2],random_angle[3],random_angle[4],random_angle[5],random_angle[6],
                     norm_Q_diff[j], norm_elbow_diff[j], norm_wrist_diff[j],sum_diff[j]]

            dataSet[j].append(dataAdd)
            diff_all_post.append(sum_diff[j])

        dataAdd_to_All = [random_angle[0],random_angle[1],random_angle[2],random_angle[3],random_angle[4],random_angle[5],random_angle[6],
                            diff_all_post,sum(diff_all_post)]
        dataAll.append(dataAdd_to_All)

    print "time finish",time.clock()
    saveDataToFile(str(prefix_file_name)+"_7DOF_All.txt",dataAll)
    dataAll.sort(key=itemgetter(8))
    saveDataToFile(str(prefix_file_name)+"_7DOF_All_sorted.txt",dataAll)
    for i in range(0,len(original_posture_config)):
        saveDataToFile(str(prefix_file_name)+"_7DOF.txt",dataSet[i])
        dataSet[i].sort(key=itemgetter(10))
        saveDataToFile(str(prefix_file_name)+"_7DOF_sorted.txt",dataSet[i])



def crossOver(prefix_file_name,original_posture_config,percent_reserve_data):

    for i in range (len(original_posture_config)):
        new_data =[]
        data = loadDataFromFile(str(prefix_file_name)+"7DOF_Q" + str(i) +"_sorted.txt")
        new_data = data[:len(data)*percent_reserve_data/100]


    print data
    print len(data)
    print new_data
    print len(new_data)


#def random_posture(angle_limit,)
############################################################################################################################################


## declare variables ##
## limit angle ##
angle1_limit = [0,135]
angle2_limit = [-90,0]
angle3_limit = [-45,45]
angle4_limit = [0,135]
angle5_limit = [-90,90]
angle6_limit = [-50,45]
angle7_limit = [-45,45]

angle_limit = [[0,135],[-90,0],[-45,45],[0,135],[-90,90],[-50,45],[-45,45]]

#angle7_limit = [28.84,28.84]

#angle6_limit = [0,0]

score_weight = [1,0.001,0.001]
loop_amount = 1000
prefix_file_name = "nothing"

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


## 1 ## random 1st generation ##
avg_angle = cal_Avg_Angle(original_posture_config,7)
for i in range(1): ##loop for each angle##
#    Cal_posture_by_random(i,avg_angle[i],'.\\testdata\\1st_gen_fixed'+str(i)+'_',2000,original_posture_config)  ### cal first gen ###

    for j in range(1):
        data = loadDataFromFile('.\\testdata\\1st_gen_fixed'+str(i)+'_7DOF_Q'+str(j)+'_sorted.txt')
        print data
        print len(data)
        data_1900 = data[:1900]
        print data_1900
        print len(data_1900)

        #crossOver('.\\testdata\\1st_gen_fixed'+str(i)+'_',original_posture_config,90)







