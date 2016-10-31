"""
code for test find new Namo posture by random method
"""

import random
from sympy import symbols, Matrix, Symbol, exp, sin, cos, sqrt, diff
import math
import time

import numpy as np
from scipy.linalg import norm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from ast import literal_eval
from operator import itemgetter
from copy import deepcopy



def loadDataFromFile(fileName):
    with open(fileName) as f:
        data = [list(literal_eval(line)) for line in f]
    return data

def saveDataToFile(fileName,data):
    file_data = open(fileName, 'w')
    for item in data:
        file_data.write("%s\n"% item)
    file_data.close()

def calKinematicNamo(degree7Joint,armSide):
    """ calculate Namo robot kinematic 7DOF Arm
    :param degree7Joint: input [degree0,1,2,3,4,5,6]
    :param armSide: input arm side 'L' for Left side, 'R' for Right side
    :return: Transformation Matrix List [T01,T02,T03,T04,T05,T06,T07,T0E]
    """
    ## DH parameter >> alpha[0,1,...6,end effector]
    alpha = [math.radians(90),math.radians(90),math.radians(-90),math.radians(-90),math.radians(90),math.radians(90),
             math.radians(-90),math.radians(0)]
    ## DH parameter >> a[0,1,...6,end effector]
    a = [0,0,0,0,0,0,0,-140]
    ## DH parameter >> d[1,2,...7,end effector]
    d = [182,0,206.5,0,206,0,0,0]
    if armSide == 'L':
        d[0] = d[0]*(-1)
    elif armSide == 'R':
        d[0] = d[0]*1

    ## DH parameter >> theta[1,2,...7,end effector]
    theta = [math.radians(degree7Joint[0] + 90),math.radians(degree7Joint[1] + 90),math.radians(degree7Joint[2] - 90),
             math.radians(degree7Joint[3]),math.radians(degree7Joint[4] + 90),math.radians(degree7Joint[5] - 90),
             math.radians(degree7Joint[6]),math.radians(0)]
    T = {}
    for i in range(0,8):
        #print i
        T[i] = Matrix((    [(cos(theta[i])), (-sin(theta[i])), 0, a[i]],
                        [(sin(theta[i]) * (cos(alpha[i]))), (cos(theta[i])) * (cos(alpha[i])), (-sin(alpha[i])),
                         (-sin(alpha[i])) * d[i]],
                        [(sin(theta[i]) * (sin(alpha[i]))), (cos(theta[i])) * (sin(alpha[i])), (cos(alpha[i])),
                         (cos(alpha[i])) * d[i]],
                        [0, 0, 0, 1]))

    T01 = T[0]
    T02 = T01*T[1]
    T03 = T02*T[2]
    T04 = T03*T[3]
    T05 = T04*T[4]
    T06 = T05*T[5]
    T07 = T06*T[6]
    T0E = T07*T[7]
    return [T01,T02,T03,T04,T05,T06,T07,T0E]

def calQuaternion(Tmatrix):
    #print Tmatrix
    tr = Tmatrix[0,0] + Tmatrix[1,1] + Tmatrix[2,2]
    if(tr>0):
        S = math.sqrt(tr+1.0)*2 ## S=4*qw
        qw = 0.25*S
        qx = (Tmatrix[2,1]-Tmatrix[1,2])/S
        qy = (Tmatrix[0,2]-Tmatrix[2,0])/S
        qz = (Tmatrix[1,0]-Tmatrix[0,1])/S
        #print "case1"
    elif((Tmatrix[0,0]>Tmatrix[1,1]) and (Tmatrix[0,0]>Tmatrix[2,2])):
        S = math.sqrt(1.0 + Tmatrix[0,0] - Tmatrix[1,1] - Tmatrix[2,2])*2 ## S=4*qx
        qw = (Tmatrix[2,1]-Tmatrix[1,2])/S
        qx = 0.25*S
        qy = (Tmatrix[0,1]+Tmatrix[1,0])/S
        qz = (Tmatrix[0,2]+Tmatrix[2,0])/S
        #print "case2"
    elif(Tmatrix[1,1]>Tmatrix[2,2]):
        S = math.sqrt(1.0 + Tmatrix[1,1] - Tmatrix[0,0] - Tmatrix[2,2])*2 ## S=4*qy
        qw = (Tmatrix[0,2]-Tmatrix[2,0])/S
        qx = (Tmatrix[0,1]+Tmatrix[1,0])/S
        qy = 0.25*S
        qz = (Tmatrix[1,2]+Tmatrix[2,1])/S
        #print "case3"
    else:
        S = math.sqrt(1.0 + Tmatrix[2,2] - Tmatrix[0,0] - Tmatrix[1,1])*2 ## S=4*qz
        qw = (Tmatrix[1,0]-Tmatrix[0,1])/S
        qx = (Tmatrix[0,2]+Tmatrix[2,0])/S
        qy = (Tmatrix[1,2]+Tmatrix[2,1])/S
        qz = 0.25*S
        #print "case4"

    norm = math.sqrt((qw*qw) + (qx*qx) + (qy*qy) + (qz*qz))
    return [qw,qx,qy,qz,norm]

def Cal_posture_by_random():
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

#angle7_limit = [28.84,28.84]

#angle6_limit = [0,0]

score_weight = [1,0.001,0.001]
loop_amount = 1000
prefix_file_name = "nothing"

## original posture ##
wai_posture_config = [25,-5,-45,100,0,-40,45,207,-54,-105,'close']
respect_posture_config = [80,-45,-10,135,45,0,0,85,-207,131,'close']
bye_posture_config = [25,-20,0,110,-90,-50,-15,229,-229,-34,'open']
rightInvite_posture_config = [10,-10,45,60,45,0,0,218,-102,-96,'close']

original_posture_config = []
original_posture_config.append(wai_posture_config)
original_posture_config.append(respect_posture_config)
original_posture_config.append(bye_posture_config)
original_posture_config.append(rightInvite_posture_config)


# ##############################################################################################################################################

#Cal_posture_by_random()

#random_each_posture(wai_posture_config,"fixedangle1_32_test_random_7DOF_Q0_sorted.txt",20,10000,"test_angle1_32_random_pos1",[0,32])
#random_each_posture(wai_posture_config,"fixedangle1_35_test_random_Avg7DOF_Q_20_sorted.txt",20,10000,"test_angle1_35_avg_pos1",[0,35])

#random_each_posture(wai_posture_config,"fixedangle2_-10_test_random_7DOF_Q0_sorted.txt",20,10000,"test_angle2_-10_random_pos1",[1,-10])
#random_each_posture(wai_posture_config,"fixedangle2_-15_test_random_Avg7DOF_Q_20_sorted.txt",20,10000,"test_angle2_-15_avg_pos1",[1,-15])

#random_each_posture(wai_posture_config,"fixedangle3_2_test_random_7DOF_Q0_sorted.txt",20,10000,"test_angle3_2_random_pos1",[2,2])
#random_each_posture(wai_posture_config,"fixedangle3_-2.5_test_random_Avg7DOF_Q_20_sorted.txt",20,10000,"test_angle3_-2.5_avg_pos1",[2,-2.5])

#random_each_posture(wai_posture_config,"fixedangle3_2_solve_w2_7DOF_Q0_sorted.txt",20,10000,"test_angle3_2_solve_w2_pos1",[2,2])
#random_each_posture(wai_posture_config,"fixedangle3_-2.5_solve_w2_Avg_7DOF_Q_20_sorted.txt",20,10000,"test_angle3_-2.5_solve_w2_Avg_pos1",[2,-2.5])

#random_each_posture(wai_posture_config,"fixedangle4_132_test_random_7DOF_Q0_sorted.txt",20,10000,"test_angle4_132_random_pos1",[3,132])
#random_each_posture(wai_posture_config,"fixedangle4_101.25_test_random_Avg7DOF_Q_20_sorted.txt",20,10000,"test_angle4_101.25_avg_pos1",[3,101.25])

#random_each_posture(wai_posture_config,"fixedangle5_14_test_random_7DOF_Q0_sorted.txt",20,10000,"test_angle5_14_random_pos1",[4,14])
#random_each_posture(wai_posture_config,"fixedangle5_0_test_random_Avg7DOF_Q_20_sorted.txt",20,10000,"test_angle5_0_avg_pos1",[4,0])

#random_each_posture(wai_posture_config,"fixedangle6_-4_test_random_7DOF_Q0_sorted.txt",20,10000,"test_angle6_-4_random_pos1",[5,-4])
#random_each_posture(wai_posture_config,"fixedangle6_-22.5_test_random_Avg7DOF_Q_20_sorted.txt",20,10000,"test_angle6_-22.5_avg_pos1",[5,-22.5])

#random_each_posture(wai_posture_config,"fixedangle6_-4_solve_w2_7DOF_Q0_sorted.txt",20,10000,"test_angle6_-4_solve_w2_pos1",[5,-4])
#random_each_posture(wai_posture_config,"fixedangle6_-22.5_solve_w2_Avg_7DOF_Q_20_sorted.txt",20,10000,"test_angle6_-22.5_solve_w2_avg_pos1",[5,-22.5])

#random_each_posture(wai_posture_config,"fixedangle7_11_test_random_7DOF_Q0_sorted.txt",20,10000,"test_angle7_11_random_pos1",[6,11])
#random_each_posture(wai_posture_config,"fixedangle7_7.5_test_random_Avg7DOF_Q_20_sorted.txt",20,10000,"test_angle7_7.5_avg_pos1",[6,7.5])

random_each_posture(wai_posture_config,"fixedangle7_11_solve_w2_7DOF_Q0_sorted.txt",20,10000,"test_angle7_11_solve_w2_pos1",[6,11])
random_each_posture(wai_posture_config,"fixedangle7_7.5_solve_w2_Avg_7DOF_Q_20_sorted.txt",20,10000,"test_angle7_7.5_solve_w2_avg_pos1",[6,7.5])

#random_each_posture(respect_posture_config,"fixedangle1_32_test_random_7DOF_Q1_sorted.txt",20,10000,"test_angle1_32_random_pos2",[0,32])
#random_each_posture(respect_posture_config,"fixedangle1_35_test_random_Avg7DOF_Q_21_sorted.txt",20,10000,"test_angle1_35_avg_pos2",[0,35])



print "finished"

