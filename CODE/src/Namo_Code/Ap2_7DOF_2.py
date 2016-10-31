"""
code for test find new Namo posture by random method
"""

import random
from sympy import symbols, Matrix, Symbol, exp, sin, cos, sqrt, diff
import math
import time
from visual import *
from visual.controls import *

import numpy as np
from scipy.linalg import norm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from ast import literal_eval
from operator import itemgetter
from copy import deepcopy


## declare variables ##
## limit angle ##
angle1_limit = [0,135]
angle2_limit = [-90,0]
angle3_limit = [-45,45]
angle4_limit = [0,135]
angle5_limit = [-90,90]
angle6_limit = [-45,45]
angle7_limit = [-45,45]

angle6_limit = [0,0]

score_weight = [1,0.001,0.001]
loop_amount = 10000;
scene.title = "Namo Robot >> Right Side"
scene.height = scene.width = 800

f_armLength = [700,182,206.5,206,130,0.0,65.0]

## original posture ##
wai_posture_config = [25,-5,-45,100,0,-40,45,207,-54,-105,'close']
respect_posture_config = [80,-45,-10,135,45,0,0,85,-207,131,'close']
bye_posture_config = [25,-20,0,110,-90,-50,-15,229,-229,-34,'open']
handOverHeart_posture_config = [30,-20,-45,105,0,0,0,218,-102,-96,'close']

original_posture_config = []
original_posture_config.append(wai_posture_config)
original_posture_config.append(respect_posture_config)
original_posture_config.append(bye_posture_config)
original_posture_config.append(handOverHeart_posture_config)

target_posture = bye_posture_config


#def drawArm(color,posture):
#**********************************************
# define frame #
frameworld = frame()
frameworld.pos = (0,-500,0)
frame0 = frame(frame=frameworld)
frame0.pos = (0,f_armLength[0],0)
frame1_R = frame(frame=frame0)
frame1_R.pos = (-f_armLength[1],0,0)
frame2_R = frame(frame=frame1_R)
frame2_R.pos = (0,0,0)
frame3_R = frame(frame=frame2_R)
frame3_R.pos = (0,0,0)
frame4_R = frame(frame=frame3_R)
frame4_R.pos = (0,-f_armLength[2],0)
frame5_R = frame(frame=frame4_R)
frame5_R.pos = (0,-f_armLength[3],0)
frame6_R = frame(frame=frame5_R)
frame6_R.pos = (0,0,0)
frame7_R = frame(frame=frame6_R)
frame7_R.pos = (0,0,0)


base = cylinder(frame=frameworld,
               pos=(0,0,0),
               axis=(0,5,0),
               radius=50,
               color=color.green)

main_sphere = sphere(frame=frame0,
               pos=(0,0,0),
               radius=30,
               color=color.green)

right_shoulder_sphere = sphere(frame=frame1_R,
               pos=(0,0,0),
               radius=25,
               color=color.green)

right_shoulder_axis = cylinder(frame=frame0,
               pos=(0,0,0),
               axis=(-f_armLength[1],0,0),
               radius=20,
               color=color.green)
right_upper_arm_axis = cylinder(frame=frame3_R,
               pos=(0,0,0),
               axis=(0,-f_armLength[2],0),
               radius=20,
               color=color.green)
right_elbow_sphere = sphere(frame=frame4_R,
               pos=(0,0,0),
               radius=25,
               color=color.green)
right_lower_arm_axis = cylinder(frame=frame4_R,
               pos=(0,0,0),
               axis=(0,-f_armLength[3],0),
               radius=20,
               color=color.green)
right_wrist_sphere = sphere(frame=frame5_R,
               pos=(0,0,0),
               radius=25,
               color=color.green)
right_hand_axis = cylinder(frame=frame7_R,
               pos=(0,0,0),
               axis=(0,-f_armLength[4],0),
               radius=10,
               color=color.green)
right_hand_sphere = sphere(frame=frame7_R,
               pos=(20,-f_armLength[4]/2,0),
               radius=10,
               color=color.green)
right_hand_box = box(frame = frame7_R,
                pos =(10,-f_armLength[4]/2,0),
                length = 10,
                height = 100,
                width = 30,
                color=color.red)
############################################################################################
# define angle unit radian
angle_1_R = target_posture[0]
angle_2_R = target_posture[1]
angle_3_R = target_posture[2]
angle_4_R = target_posture[3]
angle_5_R = target_posture[4]
angle_6_R = target_posture[5]
angle_7_R = target_posture[6]
# define angle unit radian

#frame0.rotate(axis = (0, 0, 1), angle = 0)  #main frame
frame1_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_1_R ))  #base frame
frame2_R.rotate(axis = (0, 0, 1), angle = math.radians(angle_2_R ))
frame3_R.rotate(axis = (0, -1, 0), angle = math.radians(angle_3_R ))
frame4_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_4_R ))
frame5_R.rotate(axis = (0, -1, 0), angle = math.radians(angle_5_R ))
frame6_R.rotate(axis = (0, 0, 1), angle = math.radians(angle_6_R ))
frame7_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_7_R ))



scene.autoscale = 0



def loadDataFromFile(fileName):
    with open(fileName) as f:
        data = [list(literal_eval(line)) for line in f]
    return data

def saveDataToFile(fileName,data):
    file_data = open(fileName, 'w')
    for item in data:
        file_data.write("%s\n"% item)
    file_data.close()

def calKinematicNamo_NewFunction(degree7Joint,armSide):
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

def calXYZFixedAngle(Tmatrix):
    beta = math.atan2(Tmatrix[2,0],math.sqrt(math.pow(Tmatrix[0,0],2)+math.pow(Tmatrix[1,0],2)))
    alpha = math.atan2(Tmatrix[1,0]/math.cos(beta),Tmatrix[0,0]/math.cos(beta))
    gamma = math.atan2(Tmatrix[2,1]/math.cos(beta),Tmatrix[2,2]/math.cos(beta))

    return [alpha,beta,gamma]

def calEquivalentAngleAxis(Tmatrix):
    theta = math.acos((Tmatrix[0,0]+Tmatrix[1,1]+Tmatrix[2,2]-1)/2)
    K = (1/(2*math.sin(theta)))*Matrix(([Tmatrix[2,1]-Tmatrix[1,2]],[Tmatrix[0,2]-Tmatrix[2,0]],[Tmatrix[1,0]-Tmatrix[0,1]]))
   # print "mmm"
    #print 1/(2*math.sin(theta))
   # print Matrix(([Tmatrix[2,1]-Tmatrix[1,2]],[Tmatrix[0,2]-Tmatrix[2,0]],[Tmatrix[1,0]-Tmatrix[0,1]]))

    #print K
    return K,theta

def calAngleBetweenVector(Vec1,Vec2):
    a = np.dot(Vec1,Vec2)
    b = norm(Vec1)*norm(Vec2)
    theta = math.acos()
    pass


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





deg7 = [target_posture[0],target_posture[1],target_posture[2],target_posture[3],target_posture[4],target_posture[5],target_posture[6]]

TMatrix_Target_Posture = calKinematicNamo_NewFunction(deg7,'R')
Q_ref = calQuaternion(TMatrix_Target_Posture[7])



dataSet = []
# dataHeader = 'angle1_limit = [0,135]'
# dataSet.append(dataHeader)
# dataHeader = 'angle2_limit = [-90,0]'
# dataSet.append(dataHeader)
# dataHeader = 'angle3_limit = [-45,45]'
# dataSet.append(dataHeader)
# dataHeader = 'angle4_limit = [0,135]'
# dataSet.append(dataHeader)
# dataHeader = ['angle1','angle2','angle3','angle4','posElbowX','posElbowY','posElbowZ','posWristX','posWristY','posWristZ']
# dataSet.append(dataHeader)
print "time start",time.clock()


random_angle = [25,-20,0,110,-90,-50,-13]
T_Matrix = calKinematicNamo_NewFunction(random_angle,'R')
#XYZFixedAngle = calXYZFixedAngle(T_Matrix[7])
print "aaa"
B = calEquivalentAngleAxis(T_Matrix[7])
print B[0]
print B[0][1]
print B[1]

for i in range (0,loop_amount):
     #random_angle = [25,-20,0,110,-90,-50,-13]
     random_angle = [round(random.uniform(angle1_limit[0],angle1_limit[1]),2),
                     round(random.uniform(angle2_limit[0],angle2_limit[1]),2),
                     round(random.uniform(angle3_limit[0],angle3_limit[1]),2),
                     round(random.uniform(angle4_limit[0],angle4_limit[1]),2),
                     round(random.uniform(angle5_limit[0],angle5_limit[1]),2),
                     round(random.uniform(angle6_limit[0],angle6_limit[1]),2),
                     round(random.uniform(angle7_limit[0],angle7_limit[1]),2)
                     ]
     T_Matrix = calKinematicNamo_NewFunction(random_angle,'R')
     #XYZFixedAngle = calXYZFixedAngle(T_Matrix[7])

     Q = calQuaternion(T_Matrix[7])
     Q_diff = [Q_ref[0]-Q[0],Q_ref[1]-Q[1],Q_ref[2]-Q[2],Q_ref[3]-Q[3]]
     norm_Q_diff = math.sqrt((Q_diff[0]*Q_diff[0])+(Q_diff[1]*Q_diff[1])+(Q_diff[2]*Q_diff[2])+(Q_diff[3]*Q_diff[3]))
     elbow_diff = [TMatrix_Target_Posture[3][0,3] - T_Matrix[3][0,3],TMatrix_Target_Posture[3][1,3] - T_Matrix[3][1,3],TMatrix_Target_Posture[3][2,3] - T_Matrix[3][2,3]]
     norm_elbow_diff = math.sqrt(pow(TMatrix_Target_Posture[3][0,3] - T_Matrix[3][0,3],2)+pow(TMatrix_Target_Posture[3][1,3] - T_Matrix[3][1,3],2)+pow(TMatrix_Target_Posture[3][2,3] - T_Matrix[3][2,3],2))
     wrist_diff = [TMatrix_Target_Posture[4][0,3] - T_Matrix[4][0,3],TMatrix_Target_Posture[4][1,3] - T_Matrix[4][1,3],TMatrix_Target_Posture[4][2,3] - T_Matrix[4][2,3]]
     norm_wrist_diff = math.sqrt(pow(TMatrix_Target_Posture[4][0,3] - T_Matrix[4][0,3],2)+pow(TMatrix_Target_Posture[4][1,3] - T_Matrix[4][1,3],2)+pow(TMatrix_Target_Posture[4][2,3] - T_Matrix[4][2,3],2))
     sum_diff =  norm_Q_diff*score_weight[0] +   norm_elbow_diff*score_weight[1] +   norm_wrist_diff*score_weight[2]

     dataAdd = [random_angle[0],random_angle[1],random_angle[2],random_angle[3],random_angle[4],random_angle[5],random_angle[6],
                norm_Q_diff, norm_elbow_diff, norm_wrist_diff,sum_diff]
#
#     #print dataAdd
     dataSet.append(dataAdd)
#     #print random_angle
#
# print dataAdd
# print dataSet[999]
print "time finish",time.clock()
saveDataToFile("7DOF_Q.txt",dataSet)
#dataSet.sort(key=itemgetter(11))
dataSet.sort(key=itemgetter(10))
#dataSet.sort(key=itemgetter(21))
saveDataToFile("7DOFsort_Q.txt",dataSet)


#calEquivalentAngleAxis(0)
#calEquivalentAngleAxis(Tmatrix)
#
# # testA = calKinematicNamo_NewFunction([91.15, -7.14, 11.16, 3.5,0,0,0],'R')
# # print testA

##############################################################################################################################################








#def drawArm(color,posture):
#**********************************************
# define frame #
N_frameworld = frame()
N_frameworld.pos = (0,-500,0)
N_frame0 = frame(frame=N_frameworld)
N_frame0.pos = (0,f_armLength[0],0)
N_frame1_R = frame(frame=N_frame0)
N_frame1_R.pos = (-f_armLength[1],0,0)
N_frame2_R = frame(frame=N_frame1_R)
N_frame2_R.pos = (0,0,0)
N_frame3_R = frame(frame=N_frame2_R)
N_frame3_R.pos = (0,0,0)
N_frame4_R = frame(frame=N_frame3_R)
N_frame4_R.pos = (0,-f_armLength[2],0)
N_frame5_R = frame(frame=N_frame4_R)
N_frame5_R.pos = (0,-f_armLength[3],0)
N_frame6_R = frame(frame=N_frame5_R)
N_frame6_R.pos = (0,0,0)
N_frame7_R = frame(frame=N_frame6_R)
N_frame7_R.pos = (0,0,0)


base = cylinder(frame=N_frameworld,
               pos=(0,0,0),
               axis=(0,5,0),
               radius=50,
               color=color.red)

main_sphere = sphere(frame=N_frame0,
               pos=(0,0,0),
               radius=30,
               color=color.red)

right_shoulder_sphere = sphere(frame=N_frame1_R,
               pos=(0,0,0),
               radius=25,
               color=color.red)

right_shoulder_axis = cylinder(frame=N_frame0,
               pos=(0,0,0),
               axis=(-f_armLength[1],0,0),
               radius=20,
               color=color.red)
right_upper_arm_axis = cylinder(frame=N_frame3_R,
               pos=(0,0,0),
               axis=(0,-f_armLength[2],0),
               radius=20,
               color=color.red)
right_elbow_sphere = sphere(frame=N_frame4_R,
               pos=(0,0,0),
               radius=25,
               color=color.red)
right_lower_arm_axis = cylinder(frame=N_frame4_R,
               pos=(0,0,0),
               axis=(0,-f_armLength[3],0),
               radius=20,
               color=color.red)
right_wrist_sphere = sphere(frame=N_frame5_R,
               pos=(0,0,0),
               radius=25,
               color=color.red)
right_hand_axis = cylinder(frame=N_frame7_R,
               pos=(0,0,0),
               axis=(0,-f_armLength[4],0),
               radius=10,
               color=color.red)
right_hand_sphere = sphere(frame=N_frame7_R,
               pos=(20,-f_armLength[4]/2,0),
               radius=10,
               color=color.red)
right_hand_box = box(frame = N_frame7_R,
                pos =(10,-f_armLength[4]/2,0),
                length = 10,
                height = 100,
                width = 30,
                color=color.green)
############################################################################################
# define angle unit radian

N_angle_1_R = dataSet[0][0]
N_angle_2_R = dataSet[0][1]
N_angle_3_R = dataSet[0][2]
N_angle_4_R = dataSet[0][3]
N_angle_5_R = dataSet[0][4]
N_angle_6_R = dataSet[0][5]
N_angle_7_R = dataSet[0][6]
# define angle unit radian

#frame0.rotate(axis = (0, 0, 1), angle = 0)  #main frame
N_frame1_R.rotate(axis = (-1, 0, 0), angle = math.radians(N_angle_1_R ))  #base frame
N_frame2_R.rotate(axis = (0, 0, 1), angle = math.radians(N_angle_2_R ))
N_frame3_R.rotate(axis = (0, -1, 0), angle = math.radians(N_angle_3_R ))
N_frame4_R.rotate(axis = (-1, 0, 0), angle = math.radians(N_angle_4_R ))
N_frame5_R.rotate(axis = (0, -1, 0), angle = math.radians(N_angle_5_R ))
N_frame6_R.rotate(axis = (0, 0, 1), angle = math.radians(N_angle_6_R ))
N_frame7_R.rotate(axis = (-1, 0, 0), angle = math.radians(N_angle_7_R ))


