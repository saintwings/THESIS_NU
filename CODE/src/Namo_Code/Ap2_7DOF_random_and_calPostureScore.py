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
    print Tmatrix
    tr = Tmatrix[0,0] + Tmatrix[1,1] + Tmatrix[2,2]
    if(tr>0):
        S = math.sqrt(tr+1.0)*2 ## S=4*qw
        qw = 0.25*S
        qx = (Tmatrix[2,1]-Tmatrix[1,2])/S
        qy = (Tmatrix[0,2]-Tmatrix[2,0])/S
        qz = (Tmatrix[1,0]-Tmatrix[0,1])/S
        print "case1"
    elif((Tmatrix[0,0]>Tmatrix[1,1]) and (Tmatrix[0,0]>Tmatrix[2,2])):
        S = math.sqrt(1.0 + Tmatrix[0,0] - Tmatrix[1,1] - Tmatrix[2,2])*2 ## S=4*qx
        qw = (Tmatrix[2,1]-Tmatrix[1,2])/S
        qx = 0.25*S
        qy = (Tmatrix[0,1]+Tmatrix[1,0])/S
        qz = (Tmatrix[0,2]+Tmatrix[2,0])/S
        print "case2"
    elif(Tmatrix[1,1]>Tmatrix[2,2]):
        S = math.sqrt(1.0 + Tmatrix[1,1] - Tmatrix[0,0] - Tmatrix[2,2])*2 ## S=4*qy
        qw = (Tmatrix[0,2]-Tmatrix[2,0])/S
        qx = (Tmatrix[0,1]+Tmatrix[1,0])/S
        qy = 0.25*S
        qz = (Tmatrix[1,2]+Tmatrix[2,1])/S
        print "case3"
    else:
        S = math.sqrt(1.0 + Tmatrix[2,2] - Tmatrix[0,0] - Tmatrix[1,1])*2 ## S=4*qz
        qw = (Tmatrix[1,0]-Tmatrix[0,1])/S
        qx = (Tmatrix[0,2]+Tmatrix[2,0])/S
        qy = (Tmatrix[1,2]+Tmatrix[2,1])/S
        qz = 0.25*S
        print "case4"

    norm = math.sqrt((qw*qw) + (qx*qx) + (qy*qy) + (qz*qz))
    return [qw,qx,qy,qz,norm]
############################################################################################################################################


## declare variables ##
## limit angle ##
angle1_limit = [0,135]
angle2_limit = [-90,0]
angle3_limit = [-45,45]
angle4_limit = [0,135]
angle5_limit = [-90,90]
angle6_limit = [-45,45]
angle7_limit = [-45,45]

angle7_limit = [28.84,28.84]

#angle6_limit = [0,0]

score_weight = [1,0.001,0.001]
loop_amount = 10000
prefix_file_name = "fixA7_28.84_"

## original posture ##
wai_posture_config = [25,-5,-45,100,0,-40,45,207,-54,-105,'close']
respect_posture_config = [80,-45,-10,135,45,0,0,85,-207,131,'close']
bye_posture_config = [25,-20,0,110,-90,-50,-15,229,-229,-34,'open']
rightInvite_posture_config = [10,10,45,60,45,0,0,218,-102,-96,'close']

original_posture_config = []
original_posture_config.append(wai_posture_config)
original_posture_config.append(respect_posture_config)
original_posture_config.append(bye_posture_config)
original_posture_config.append(rightInvite_posture_config)

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
    random_angle = [round(random.uniform(angle1_limit[0],angle1_limit[1]),2),
                      round(random.uniform(angle2_limit[0],angle2_limit[1]),2),
                      round(random.uniform(angle3_limit[0],angle3_limit[1]),2),
                      round(random.uniform(angle4_limit[0],angle4_limit[1]),2),
                      round(random.uniform(angle5_limit[0],angle5_limit[1]),2),
                      round(random.uniform(angle6_limit[0],angle6_limit[1]),2),
                      round(random.uniform(angle7_limit[0],angle7_limit[1]),2)
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

# ##############################################################################################################################################
