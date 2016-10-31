__author__ = 'SaintWingZ'

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
from sympy import symbols, Matrix, Symbol, exp, sin, cos, sqrt, diff
import time
from ast import literal_eval
from operator import itemgetter
from copy import deepcopy
import matplotlib as mpl


def calKinematicNamo_Step(degreeJoint):
    int_motorDirection = [1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1]

    alpha0_r = math.radians(90)
    alpha1_r = math.radians(90)
    alpha2_r = math.radians(-90)
    alpha3_r = math.radians(-90)
    alpha4_r = math.radians(90)
    alpha5_r = math.radians(90)
    alpha6_r = math.radians(-90)
    alpha7_r = math.radians(0)

    alpha0_l = math.radians(90)
    alpha1_l = math.radians(90)
    alpha2_l = math.radians(-90)
    alpha3_l = math.radians(-90)
    alpha4_l = math.radians(90)
    alpha5_l = math.radians(90)
    alpha6_l = math.radians(-90)
    alpha7_l = math.radians(0)

    a0_r = 0
    a1_r = 0
    a2_r = 0
    a3_r = 0
    a4_r = 0
    a5_r = 0
    a6_r = 0
    ##a7_r = -140
    a7_r = 0

    a0_l = 0
    a1_l = 0
    a2_l = 0
    a3_l = 0
    a4_l = 0
    a5_l = 0
    a6_l = 0
    a7_l = -140

    d1_r = 182
    d2_r = 0
    d3_r = 206.5
    d4_r = 0
    d5_r = 206
    d6_r = 0
    d7_r = 0
    d8_r = 0

    d1_l = -182
    d2_l = 0
    d3_l = 206.5
    d4_l = 0
    d5_l = 206
    d6_l = 0
    d7_l = 0
    d8_l = 0

    # theta1_l = math.radians(degreeJointL[0]+90)
    # theta2_l = math.radians(degreeJointL[1]+90)
    # theta3_l = math.radians(degreeJointL[2]-90)
    # theta4_l = math.radians(degreeJointL[3])
    # theta5_l = math.radians(degreeJointL[4]+90)
    # theta6_l = math.radians(degreeJointL[5]-90)
    # theta7_l = math.radians(degreeJointL[6])
    # theta8_l = math.radians(0)

    theta1_r = math.radians(degreeJoint[0] + 90)
    theta2_r = math.radians(degreeJoint[1] + 90)
    theta3_r = math.radians(degreeJoint[2] - 90)
    theta4_r = math.radians(degreeJoint[3])
    theta5_r = math.radians(degreeJoint[4] + 90)
    theta6_r = math.radians(degreeJoint[5] - 90)
    theta7_r = math.radians(degreeJoint[6])
    theta8_r = math.radians(0)

    t01_r = Matrix((    [(cos(theta1_r)), (-sin(theta1_r)), 0, a0_r],
                        [(sin(theta1_r) * (cos(alpha0_r))), (cos(theta1_r)) * (cos(alpha0_r)), (-sin(alpha0_r)),
                         (-sin(alpha0_r)) * d1_r],
                        [(sin(theta1_r) * (sin(alpha0_r))), (cos(theta1_r)) * (sin(alpha0_r)), (cos(alpha0_r)),
                         (cos(alpha0_r)) * d1_r],
                        [0, 0, 0, 1]))

    t12_r = Matrix((    [(cos(theta2_r)), (-sin(theta2_r)), 0, a1_r],
                        [(sin(theta2_r) * (cos(alpha1_r))), (cos(theta2_r)) * (cos(alpha1_r)), (-sin(alpha1_r)),
                         (-sin(alpha1_r)) * d2_r],
                        [(sin(theta2_r) * (sin(alpha1_r))), (cos(theta2_r)) * (sin(alpha1_r)), (cos(alpha1_r)),
                         (cos(alpha1_r)) * d2_r],
                        [0, 0, 0, 1]))

    t23_r = Matrix((    [(cos(theta3_r)), (-sin(theta3_r)), 0, a2_r],
                        [(sin(theta3_r) * (cos(alpha2_r))), (cos(theta3_r)) * (cos(alpha2_r)), (-sin(alpha2_r)),
                         (-sin(alpha2_r)) * d3_r],
                        [(sin(theta3_r) * (sin(alpha2_r))), (cos(theta3_r)) * (sin(alpha2_r)), (cos(alpha2_r)),
                         (cos(alpha2_r)) * d3_r],
                        [0, 0, 0, 1]))

    t34_r = Matrix((    [(cos(theta4_r)), (-sin(theta4_r)), 0, a3_r],
                        [(sin(theta4_r) * (cos(alpha3_r))), (cos(theta4_r)) * (cos(alpha3_r)), (-sin(alpha3_r)),
                         (-sin(alpha3_r)) * d4_r],
                        [(sin(theta4_r) * (sin(alpha3_r))), (cos(theta4_r)) * (sin(alpha3_r)), (cos(alpha3_r)),
                         (cos(alpha3_r)) * d4_r],
                        [0, 0, 0, 1]))

    t45_r = Matrix((    [(cos(theta5_r)), (-sin(theta5_r)), 0, a4_r],
                        [(sin(theta5_r) * (cos(alpha4_r))), (cos(theta5_r)) * (cos(alpha4_r)), (-sin(alpha4_r)),
                         (-sin(alpha4_r)) * d5_r],
                        [(sin(theta5_r) * (sin(alpha4_r))), (cos(theta5_r)) * (sin(alpha4_r)), (cos(alpha4_r)),
                         (cos(alpha4_r)) * d5_r],
                        [0, 0, 0, 1]))

    t56_r = Matrix((    [(cos(theta6_r)), (-sin(theta6_r)), 0, a5_r],
                        [(sin(theta6_r) * (cos(alpha5_r))), (cos(theta6_r)) * (cos(alpha5_r)), (-sin(alpha5_r)),
                         (-sin(alpha5_r)) * d6_r],
                        [(sin(theta6_r) * (sin(alpha5_r))), (cos(theta6_r)) * (sin(alpha5_r)), (cos(alpha5_r)),
                         (cos(alpha5_r)) * d6_r],
                        [0, 0, 0, 1]))

    t67_r = Matrix((    [(cos(theta7_r)), (-sin(theta7_r)), 0, a6_r],
                        [(sin(theta7_r) * (cos(alpha6_r))), (cos(theta7_r)) * (cos(alpha6_r)), (-sin(alpha6_r)),
                         (-sin(alpha6_r)) * d7_r],
                        [(sin(theta7_r) * (sin(alpha6_r))), (cos(theta7_r)) * (sin(alpha6_r)), (cos(alpha6_r)),
                         (cos(alpha6_r)) * d7_r],
                        [0, 0, 0, 1]))

    t78_r = Matrix((    [(cos(theta8_r)), (-sin(theta8_r)), 0, a7_r],
                        [(sin(theta8_r) * (cos(alpha7_r))), (cos(theta8_r)) * (cos(alpha7_r)), (-sin(alpha7_r)),
                         (-sin(alpha7_r)) * d8_r],
                        [(sin(theta8_r) * (sin(alpha7_r))), (cos(theta8_r)) * (sin(alpha7_r)), (cos(alpha7_r)),
                         (cos(alpha7_r)) * d8_r],
                        [0, 0, 0, 1]))

    t02_r = t01_r * t12_r
    t03_r = t02_r * t23_r
    t04_r = t03_r * t34_r
    t05_r = t04_r * t45_r
    t06_r = t05_r * t56_r
    t07_r = t06_r * t67_r
    t08_r = t07_r * t78_r

    #return [t08_r]
    return [t01_r,t02_r,t03_r,t04_r,t05_r,t06_r,t07_r,t08_r]

#jointPositionBase = calKinematicNamo_Step([25,-5,-45,100,0,0,0])
#jointPositionBase = calKinematicNamo_Step([0,0,0,0,0,0,0,0,-182,-413])
#jointPositionBase = calKinematicNamo_Step([80,-45,-10,135,0,0,0])
#jointPositionBase = calKinematicNamo_Step([25,-20,0,110,0,0,0])
jointPositionBase = calKinematicNamo_Step([30,-20,-45,105,0,0,0])
position_x_setBase = [jointPositionBase[0][0,3],jointPositionBase[1][0,3],jointPositionBase[2][0,3],jointPositionBase[3][0,3],jointPositionBase[4][0,3],jointPositionBase[5][0,3],jointPositionBase[6][0,3],jointPositionBase[7][0,3]]
position_y_setBase = [jointPositionBase[0][1,3],jointPositionBase[1][1,3],jointPositionBase[2][1,3],jointPositionBase[3][1,3],jointPositionBase[4][1,3],jointPositionBase[5][1,3],jointPositionBase[6][1,3],jointPositionBase[7][1,3]]
position_z_setBase = [jointPositionBase[0][2,3],jointPositionBase[1][2,3],jointPositionBase[2][2,3],jointPositionBase[3][2,3],jointPositionBase[4][2,3],jointPositionBase[5][2,3],jointPositionBase[6][2,3],jointPositionBase[7][2,3]]



#jointPosition = calKinematicNamo_Step([20,-5,-40,105,0,0,0])
#jointPosition = calKinematicNamo_Step([0,-40,-45,105,0,0,0])
#jointPosition = calKinematicNamo_Step([110,-50,-40,105,0,0,0])
#jointPosition = calKinematicNamo_Step([30,-5,10,105,0,0,0])
jointPosition = calKinematicNamo_Step([30,-20,-45,105,0,0,0])
position_x_set = [jointPosition[0][0,3],jointPosition[1][0,3],jointPosition[2][0,3],jointPosition[3][0,3],jointPosition[4][0,3],jointPosition[5][0,3],jointPosition[6][0,3],jointPosition[7][0,3]]
position_y_set = [jointPosition[0][1,3],jointPosition[1][1,3],jointPosition[2][1,3],jointPosition[3][1,3],jointPosition[4][1,3],jointPosition[5][1,3],jointPosition[6][1,3],jointPosition[7][1,3]]
position_z_set = [jointPosition[0][2,3],jointPosition[1][2,3],jointPosition[2][2,3],jointPosition[3][2,3],jointPosition[4][2,3],jointPosition[5][2,3],jointPosition[6][2,3],jointPosition[7][2,3]]


print jointPosition
print position_x_set
print position_y_set
print position_z_set


mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(position_x_setBase,position_y_setBase, position_z_setBase, label='Original Posture',c='r')
ax.scatter(position_x_setBase,position_y_setBase, position_z_setBase,c='r')
ax.plot(position_x_set,position_y_set, position_z_set, label='New Posture',c='b')
ax.scatter(position_x_set,position_y_set, position_z_set,c='b')
ax.legend()

plt.show()