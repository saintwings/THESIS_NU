
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

scene.title = "Namo Robot >> Right Side"
scene.height = scene.width = 800

f_armLength = [700,182,206.5,206,130,0.0,65.0]



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

def calQuaternion2(Tmatrix):
    print Tmatrix
    qw = (math.sqrt(Tmatrix[0,0] + Tmatrix[1,1] + Tmatrix[2,2]+1.0))/2
    qx = (Tmatrix[2,1]-Tmatrix[1,2])/(qw*4)
    qy = (Tmatrix[0,2]-Tmatrix[2,0])/(qw*4)
    qz = (Tmatrix[1,0]-Tmatrix[0,1])/(qw*4)


    #norm = math.sqrt((qw*qw) + (qx*qx) + (qy*qy) + (qz*qz))
    norm1 = math.sqrt((qx*qx) + (qy*qy) + (qz*qz))
    return [qw,qx,qy,qz,norm]

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
    norm1 = math.sqrt((qx*qx) + (qy*qy) + (qz*qz))
    return [qw,qx,qy,qz,norm,norm1]


angle_1_R = [0,0,0,0,0,45,0]
angle_2_R = [50,50,50,0,0,0,0]
angle_3_R = [0,0,0,0,0,0,0]

Q_ref = calQuaternion(calKinematicNamo_NewFunction(angle_1_R,'R')[7])

print calQuaternion(calKinematicNamo_NewFunction(angle_1_R,'R')[7])
print calQuaternion(calKinematicNamo_NewFunction(angle_2_R,'R')[7])
print calQuaternion(calKinematicNamo_NewFunction(angle_3_R,'R')[7])

# dataSet = []
#
# for i in range (0,361,10):
#     for j in range (0,361,10):
#         for k in range (0,361,10):
#             T = calKinematicNamo_NewFunction([i,j,k,0,0,0,0],'R')
#             Q = calQuaternion(T[7])
#             Q_diff = [Q_ref[0]-Q[0],Q_ref[1]-Q[1],Q_ref[2]-Q[2],Q_ref[3]-Q[3]]
#             norm_Q_diff = math.sqrt((Q_diff[0]*Q_diff[0])+(Q_diff[1]*Q_diff[1])+(Q_diff[2]*Q_diff[2])+(Q_diff[3]*Q_diff[3]))
#             dataAdd = [i,j,k,Q,norm_Q_diff]
#             dataSet.append(dataAdd)
#
# saveDataToFile("cal Quaternion_with_Qref.txt",dataSet)
# dataSet.sort(key=itemgetter(4))
# saveDataToFile("cal Quaternion_with_Qref1.txt",dataSet)

#def drawArm(color,posture):
#**********************************************
# define frame #
frameworld = frame()
frameworld.pos = (500,-500,0)
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

# define angle unit radian

#frame0.rotate(axis = (0, 0, 1), angle = 0)  #main frame
frame1_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_1_R[0]))  #base frame
frame2_R.rotate(axis = (0, 0, 1), angle = math.radians(angle_1_R[1]))
frame3_R.rotate(axis = (0, -1, 0), angle = math.radians(angle_1_R[2]))
frame4_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_1_R[3]))
frame5_R.rotate(axis = (0, -1, 0), angle = math.radians(angle_1_R[4]))
frame6_R.rotate(axis = (0, 0, 1), angle = math.radians(angle_1_R[5]))
frame7_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_1_R[6]))

# define frame #
N_frameworld = frame()
N_frameworld.pos = (-500,-500,0)
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


# define angle unit radian

#frame0.rotate(axis = (0, 0, 1), angle = 0)  #main frame
N_frame1_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_2_R[0]))  #base frame
N_frame2_R.rotate(axis = (0, 0, 1), angle = math.radians(angle_2_R[1]))
N_frame3_R.rotate(axis = (0, -1, 0), angle = math.radians(angle_2_R[2]))
N_frame4_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_2_R[3]))
N_frame5_R.rotate(axis = (0, -1, 0), angle = math.radians(angle_2_R[4]))
N_frame6_R.rotate(axis = (0, 0, 1), angle = math.radians(angle_2_R[5]))
N_frame7_R.rotate(axis = (-1, 0, 0), angle = math.radians(angle_2_R[6]))



scene.autoscale = 0