import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
from sympy import symbols, Matrix, Symbol, exp, sin, cos, sqrt, diff
import time
from ast import literal_eval
from operator import itemgetter
from copy import deepcopy

## declare variables ##

angle1_limit = [0,135]
angle2_limit = [-90,0]
angle3_limit = [-45,45]
angle4_limit = [0,135]
position_x_index = 7
position_y_index = 8
position_z_index = 9

def kinematic(str_fileName, plotKeyframe):
    # str_fileName = "p1"
    #int_numberOfKeyframe = 0
    int_motorDirection = [1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1]

    # read motor center value #
    file_center = open('motor_center.txt', 'r')
    int_motorCenterValue = file_center.read()
    file_center.close()
    int_motorCenterValue = int_motorCenterValue.split('\n')
    print "motor center"
    print  int_motorCenterValue
    for x in range(17):
        int_motorCenterValue[x] = int(int_motorCenterValue[x])
    int_motorValue = [[int_motorCenterValue[x] for x in range(17)] for y in range(30)]


    # read motor value #
    namePosture = str_fileName + '.txt'
    print namePosture
    file_posture = open(namePosture, 'r')
    str_load_data = file_posture.read()
    file_posture.close()
    str_load_data = str_load_data.split('\n')
    int_numberOfKeyframe = int(str_load_data[0])
    int_count_data = 1
    for x in range(int_numberOfKeyframe):
        for y in range(17):
            int_motorValue[x][y] = int(str_load_data[int_count_data])
            int_count_data = int_count_data + 1
    print"key frame amount"
    print int_numberOfKeyframe
    print"motor value all keyframe"
    print int_motorValue


    # cal diff from center value #
    int_motorValueDiff = [[(int_motorValue[y][x] - int_motorCenterValue[x]) for x in range(17)] for y in
                          range(int_numberOfKeyframe)]
    print"motor value diff all keyframe"
    print int_motorValueDiff

    # convert to degree #
    float_motorValueDiff_degree = [[(int_motorValueDiff[y][x] * 359 / 4095.0) for x in range(17)] for y in
                                   range(int_numberOfKeyframe)]
    print"motor value diff all keyframe in degree"
    print float_motorValueDiff_degree
    print float_motorValueDiff_degree[int_numberOfKeyframe - 1]

    # convert motor direction #
    float_motorValueDiff_degree = [[(float_motorValueDiff_degree[y][x] * int_motorDirection[x]) for x in range(17)] for
                                   y in range(int_numberOfKeyframe)]
    print"motor value diff all keyframe in degree"
    print float_motorValueDiff_degree
    print float_motorValueDiff_degree[int_numberOfKeyframe - 1]

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
    a7_r = -140

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

    #float_motorValueDiff_degree[int_numberOfKeyframe-1]

    if plotKeyframe == "first":
        theta1_l = math.radians((float_motorValueDiff_degree[0][0]) / 3.0 + 90)
        theta2_l = math.radians(float_motorValueDiff_degree[0][1] + 90)
        theta3_l = math.radians(float_motorValueDiff_degree[0][2] - 90)
        theta4_l = math.radians(float_motorValueDiff_degree[0][3])
        theta5_l = math.radians(float_motorValueDiff_degree[0][4] + 90)
        theta6_l = math.radians(float_motorValueDiff_degree[0][5] - 90)
        theta7_l = math.radians(float_motorValueDiff_degree[0][6])
        theta8_l = math.radians(0)

        theta1_r = math.radians((float_motorValueDiff_degree[0][7]) / 3.0 + 90)
        theta2_r = math.radians(float_motorValueDiff_degree[0][8] + 90)
        theta3_r = math.radians(float_motorValueDiff_degree[0][9] - 90)
        theta4_r = math.radians(float_motorValueDiff_degree[0][10])
        theta5_r = math.radians(float_motorValueDiff_degree[0][11] + 90)
        theta6_r = math.radians(float_motorValueDiff_degree[0][12] - 90)
        theta7_r = math.radians(float_motorValueDiff_degree[0][13])
        theta8_r = math.radians(0)

    elif plotKeyframe == "last":

        theta1_l = math.radians((float_motorValueDiff_degree[int_numberOfKeyframe - 1][0]) / 3.0 + 90)
        theta2_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][1] + 90)
        theta3_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][2] - 90)
        theta4_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][3])
        theta5_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][4] + 90)
        theta6_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][5] - 90)
        theta7_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][6])
        theta8_l = math.radians(0)

        theta1_r = math.radians((float_motorValueDiff_degree[int_numberOfKeyframe - 1][7]) / 3.0 + 90)
        theta2_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][8] + 90)
        theta3_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][9] - 90)
        theta4_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][10])
        theta5_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][11] + 90)
        theta6_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][12] - 90)
        theta7_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe - 1][13])
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

    pointSet_r = [[t01_r[0, 3], t01_r[1, 3], t01_r[2, 3]],
                  [t02_r[0, 3], t02_r[1, 3], t02_r[2, 3]],
                  [t03_r[0, 3], t03_r[1, 3], t03_r[2, 3]],
                  [t04_r[0, 3], t04_r[1, 3], t04_r[2, 3]],
                  [t05_r[0, 3], t05_r[1, 3], t05_r[2, 3]],
                  [t06_r[0, 3], t06_r[1, 3], t06_r[2, 3]],
                  [t07_r[0, 3], t07_r[1, 3], t07_r[2, 3]],
                  [t08_r[0, 3], t08_r[1, 3], t08_r[2, 3]], ]
    print "pointset R = "
    print pointSet_r

    t01_l = Matrix((    [(cos(theta1_l)), (-sin(theta1_l)), 0, a0_l],
                        [(sin(theta1_l) * (cos(alpha0_l))), (cos(theta1_l)) * (cos(alpha0_l)), (-sin(alpha0_l)),
                         (-sin(alpha0_l)) * d1_l],
                        [(sin(theta1_l) * (sin(alpha0_l))), (cos(theta1_l)) * (sin(alpha0_l)), (cos(alpha0_l)),
                         (cos(alpha0_l)) * d1_l],
                        [0, 0, 0, 1]))

    t12_l = Matrix((    [(cos(theta2_l)), (-sin(theta2_l)), 0, a1_l],
                        [(sin(theta2_l) * (cos(alpha1_l))), (cos(theta2_l)) * (cos(alpha1_l)), (-sin(alpha1_l)),
                         (-sin(alpha1_l)) * d2_l],
                        [(sin(theta2_l) * (sin(alpha1_l))), (cos(theta2_l)) * (sin(alpha1_l)), (cos(alpha1_l)),
                         (cos(alpha1_l)) * d2_l],
                        [0, 0, 0, 1]))

    t23_l = Matrix((    [(cos(theta3_l)), (-sin(theta3_l)), 0, a2_l],
                        [(sin(theta3_l) * (cos(alpha2_l))), (cos(theta3_l)) * (cos(alpha2_l)), (-sin(alpha2_l)),
                         (-sin(alpha2_l)) * d3_l],
                        [(sin(theta3_l) * (sin(alpha2_l))), (cos(theta3_l)) * (sin(alpha2_l)), (cos(alpha2_l)),
                         (cos(alpha2_l)) * d3_l],
                        [0, 0, 0, 1]))

    t34_l = Matrix((    [(cos(theta4_l)), (-sin(theta4_l)), 0, a3_l],
                        [(sin(theta4_l) * (cos(alpha3_l))), (cos(theta4_l)) * (cos(alpha3_l)), (-sin(alpha3_l)),
                         (-sin(alpha3_l)) * d4_l],
                        [(sin(theta4_l) * (sin(alpha3_l))), (cos(theta4_l)) * (sin(alpha3_l)), (cos(alpha3_l)),
                         (cos(alpha3_l)) * d4_l],
                        [0, 0, 0, 1]))

    t45_l = Matrix((    [(cos(theta5_l)), (-sin(theta5_l)), 0, a4_l],
                        [(sin(theta5_l) * (cos(alpha4_l))), (cos(theta5_l)) * (cos(alpha4_l)), (-sin(alpha4_l)),
                         (-sin(alpha4_l)) * d5_l],
                        [(sin(theta5_l) * (sin(alpha4_l))), (cos(theta5_l)) * (sin(alpha4_l)), (cos(alpha4_l)),
                         (cos(alpha4_l)) * d5_l],
                        [0, 0, 0, 1]))

    t56_l = Matrix((    [(cos(theta6_l)), (-sin(theta6_l)), 0, a5_l],
                        [(sin(theta6_l) * (cos(alpha5_l))), (cos(theta6_l)) * (cos(alpha5_l)), (-sin(alpha5_l)),
                         (-sin(alpha5_l)) * d6_l],
                        [(sin(theta6_l) * (sin(alpha5_l))), (cos(theta6_l)) * (sin(alpha5_l)), (cos(alpha5_l)),
                         (cos(alpha5_l)) * d6_l],
                        [0, 0, 0, 1]))

    t67_l = Matrix((    [(cos(theta7_l)), (-sin(theta7_l)), 0, a6_l],
                        [(sin(theta7_l) * (cos(alpha6_l))), (cos(theta7_l)) * (cos(alpha6_l)), (-sin(alpha6_l)),
                         (-sin(alpha6_l)) * d7_l],
                        [(sin(theta7_l) * (sin(alpha6_l))), (cos(theta7_l)) * (sin(alpha6_l)), (cos(alpha6_l)),
                         (cos(alpha6_l)) * d7_l],
                        [0, 0, 0, 1]))

    t78_l = Matrix((    [(cos(theta8_l)), (-sin(theta8_l)), 0, a7_l],
                        [(sin(theta8_l) * (cos(alpha7_l))), (cos(theta8_l)) * (cos(alpha7_l)), (-sin(alpha7_l)),
                         (-sin(alpha7_l)) * d8_l],
                        [(sin(theta8_l) * (sin(alpha7_l))), (cos(theta8_l)) * (sin(alpha7_l)), (cos(alpha7_l)),
                         (cos(alpha7_l)) * d8_l],
                        [0, 0, 0, 1]))

    t02_l = t01_l * t12_l
    t03_l = t02_l * t23_l
    t04_l = t03_l * t34_l
    t05_l = t04_l * t45_l
    t06_l = t05_l * t56_l
    t07_l = t06_l * t67_l
    t08_l = t07_l * t78_l

    pointSet_l = [[t01_l[0, 3], t01_l[1, 3], t01_l[2, 3]],
                  [t02_l[0, 3], t02_l[1, 3], t02_l[2, 3]],
                  [t03_l[0, 3], t03_l[1, 3], t03_l[2, 3]],
                  [t04_l[0, 3], t04_l[1, 3], t04_l[2, 3]],
                  [t05_l[0, 3], t05_l[1, 3], t05_l[2, 3]],
                  [t06_l[0, 3], t06_l[1, 3], t06_l[2, 3]],
                  [t07_l[0, 3], t07_l[1, 3], t07_l[2, 3]],
                  [t08_l[0, 3], t08_l[1, 3], t08_l[2, 3]], ]
    print "pointset L = "
    print pointSet_l

    data_x_l = [pointSet_l[0][0], pointSet_l[1][0], pointSet_l[2][0], pointSet_l[3][0], pointSet_l[4][0],
                pointSet_l[5][0], pointSet_l[6][0], pointSet_l[7][0]]
    data_y_l = [pointSet_l[0][1], pointSet_l[1][1], pointSet_l[2][1], pointSet_l[3][1], pointSet_l[4][1],
                pointSet_l[5][1], pointSet_l[6][1], pointSet_l[7][1]]
    data_z_l = [pointSet_l[0][2], pointSet_l[1][2], pointSet_l[2][2], pointSet_l[3][2], pointSet_l[4][2],
                pointSet_l[5][2], pointSet_l[6][2], pointSet_l[7][2]]

    data_x_r = [pointSet_r[0][0], pointSet_r[1][0], pointSet_r[2][0], pointSet_r[3][0], pointSet_r[4][0],
                pointSet_r[5][0], pointSet_r[6][0], pointSet_r[7][0]]
    data_y_r = [pointSet_r[0][1], pointSet_r[1][1], pointSet_r[2][1], pointSet_r[3][1], pointSet_r[4][1],
                pointSet_r[5][1], pointSet_r[6][1], pointSet_r[7][1]]
    data_z_r = [pointSet_r[0][2], pointSet_r[1][2], pointSet_r[2][2], pointSet_r[3][2], pointSet_r[4][2],
                pointSet_r[5][2], pointSet_r[6][2], pointSet_r[7][2]]

    data = [data_x_l, data_y_l, data_z_l, data_x_r, data_y_r, data_z_r]

    return data

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

def calWorkspaceNamo(boundAngle1, boundAngle2, boundAngle3, boundAngle4, boundAngle5, boundAngle6, boundAngle7, prefix):
    dataSet = []
    dataAdd = []
    # file_data_l = open("kinematic_data_l.txt", 'w')
    for angle1 in range(boundAngle1[0], boundAngle1[1], boundAngle1[2]):
        timeStart = time.clock()
        file_data_r = open(prefix + str(angle1) + ".txt", 'w')

        for angle2 in range(boundAngle2[0], boundAngle2[1], boundAngle2[2]):
            for angle3 in range(boundAngle3[0], boundAngle3[1], boundAngle3[2]):
                for angle4 in range(boundAngle4[0], boundAngle4[1], boundAngle4[2]):
                    for angle5 in range(boundAngle5[0], boundAngle5[1], boundAngle5[2]):
                        for angle6 in range(boundAngle6[0], boundAngle6[1], boundAngle6[2]):
                            for angle7 in range(boundAngle7[0], boundAngle7[1], boundAngle7[2]):
                                angleInput_r = [angle1, angle2, angle3, angle4, angle5, angle6, angle7]
                                #angleInput_l = [angle1,angle2,angle3,angle4,angle5,angle6,angle7]
                                a = calKinematicNamo_Step(angleInput_r)
                                dataAdd = [angleInput_r[0], angleInput_r[1], angleInput_r[2], angleInput_r[3],
                                           angleInput_r[4], angleInput_r[5], angleInput_r[6], (round(a[0][0, 3])),
                                           (round(a[0][1, 3])), (round(a[0][2, 3]))]
                                dataSet.append(dataAdd)
                                for inputIndex in range(7):
                                    file_data_r.write(str(angleInput_r[inputIndex]) + '\t')
                                    #file_data_l.write(str(angleInput_l[inputIndex])+'\t')

                                for z in range(3):
                                    file_data_r.write(str(round(a[0][z, 3])) + '\t')
                                    #file_data_l.write(str(a[1][z,3])+'\t')

                                for x in range(3):
                                    for y in range(3):
                                        file_data_r.write(str(round(a[0][x, y], 2)) + '\t')
                                        #file_data_l.write(str(a[1][x,y])+'\t')

                                file_data_r.write('\n')
                                #file_data_l.write('\n')


                                print angle1, angle2, angle3, angle4, angle5, angle6, angle7

        timeStop = time.clock()
        timediff = timeStop - timeStart
        file_data_r.write('\n' + 'time = ' + str(timediff) + '\t')
        file_data_r.close()
        #print dataSet
        #print len(dataSet)

    #saveDataToFile("test002.txt",dataSet)

    return dataSet

def loadDataFromFile(fileName):
    with open(fileName) as f:
        data = [list(literal_eval(line)) for line in f]
    return data

def saveDataToFile(fileName,data):
    file_data = open(fileName, 'w')
    for item in data:
        file_data.write("%s\n"% item)
    file_data.close()

def searchDataIndex(data,searchData,searchIndex):
#(data = data set for search, searchData = range of data for search, search index on data set)
    countIndex = 0
    firstIndex = None
    lastIndex = None
    firstTime = True
    for sublist in data:
        countIndex +=1
        if sublist[searchIndex] == searchData[0] and firstTime == True:
            firstIndex = countIndex
            firstTime = False
        if sublist[searchIndex] == searchData[1]:
            lastIndex = countIndex
        if sublist[searchIndex] > searchData[1]:
            break

    return [firstIndex,lastIndex]

def copySpecificData(dataBase,copyIndex):
    newData = []
    #print dataBase[0]
    #print copyIndex[0]
    #print copyIndex[1]
    for copyIndex in range((copyIndex[0]-1),copyIndex[1]):
        newData.append(dataBase[copyIndex])
    return newData

def calTFMatrix7DOF(angle1,angle2,angle3,angle4,angle5,angle6,angle7):
    pass


#####################################################################################################################

#calWorkspaceNamo([0,135,5],[0,-90,-5],[-45,45,5],[0,135,5],[0,90,10],[-45,45,10],[-45,45,10])
#calWorkspaceNamo([0, 136, 10], [0, -91, -10], [-45, 46, 10], [0, 136, 10], [0, 1, 10], [0, 1, 10], [0, 1, 10],'test001')

print "time start",time.clock()
dataAll = calWorkspaceNamo([0, 136, 5], [0, -91, -5], [-45, 46, 5], [0, 136, 5], [0, 1, 5], [0, 1, 5], [0, 1, 5],'test001')
saveDataToFile("AllData.txt",dataAll)
print "time finish",time.clock()


# dataAll_sort_9 = loadDataFromFile('AllData.txt')
# print "time load",time.clock()
#
# dataAll_sort_9.sort(key=itemgetter(9))
# print "time sort",time.clock()
# saveDataToFile("AllData_sort9.txt",dataAll_sort_9)
# dataAll_sort_9.sort(key=itemgetter(8))
# print "time sort",time.clock()
# saveDataToFile("AllData_sort8.txt",dataAll_sort_9)
# dataAll_sort_9.sort(key=itemgetter(7))
# print "time sort",time.clock()
# saveDataToFile("AllData_sort7.txt",dataAll_sort_9)

#allData = loadDataFromFile('aaa.txt')
# allData.sort(key=itemgetter(9
# saveDataToFile("testsort.txt",allData)
# indexData = searchDataIndex(allData,[0,0],9)
# print indexData
# filterData = copySpecificData(allData,indexData)
#
# saveDataToFile("testcopy.txt",filterData)
#
# filterData.sort(key=itemgetter(0))
# indexData = searchDataIndex(filterData,[70,90],0)
# filterData2 = copySpecificData(filterData,indexData)
# saveDataToFile("testcopy2.txt",filterData2)
# print indexData

########################################################################################################################
# # cal lock angle section ##
# failure_joint_No = 4
# failure_joint_index = failure_joint_No -1
#
# target_config_posture =[]
# target_config_wai=[25,-5,-45,100,0,0,0,207,-54,-105,'close']
# target_config_upstanding=[0,0,0,0,0,0,0,0,-182,-413,'open']
# target_config_respect=[80,-45,-10,135,0,0,0,85,-207,131,'close']
# target_config_bye=[25,-20,0,110,0,0,0,229,-229,-34,'open']
# target_config_handOverHeart=[30,-20,-45,105,0,0,0,218,-102,-96,'close']
#
# weight_for_calScore = [0.8,1,0.9,0.8,1]
#
# target_config_posture.append(target_config_wai)
# target_config_posture.append(target_config_upstanding)
# target_config_posture.append(target_config_respect)
# target_config_posture.append(target_config_bye)
# target_config_posture.append(target_config_handOverHeart)
# #target_config_posture.append(target_config_3)
# print target_config_posture
#
# print "time start",time.clock()
# dataAll = loadDataFromFile('AllData.txt')
# print "time load",time.clock()
#
# posture_score = []
#
# dataAll.sort(key=itemgetter(failure_joint_index))
#
# for angle in range(eval('angle'+str(failure_joint_No)+'_limit[0]'),eval('angle'+str(failure_joint_No)+'_limit[1]')+1,5):
#     indexData = searchDataIndex(dataAll,[angle,angle],failure_joint_index)
#     filterData = copySpecificData(dataAll,indexData)
#
#     qualified_posture_set_by_angle =[]
#
#     for postureNo in range(0,len(target_config_posture)):
#         filterData_byPosture = deepcopy(filterData)
#         for i in range(0,len(filterData_byPosture)):
#             filterData_byPosture[i].append(target_config_posture[postureNo][position_x_index]-filterData_byPosture[i][position_x_index])
#             filterData_byPosture[i].append(target_config_posture[postureNo][position_y_index]-filterData_byPosture[i][position_y_index])
#             filterData_byPosture[i].append(target_config_posture[postureNo][position_z_index]-filterData_byPosture[i][position_z_index])
#             filterData_byPosture[i].append(round(math.sqrt(math.pow(filterData_byPosture[i][position_x_index+3],2)+math.pow(filterData_byPosture[i][position_y_index+3],2)+math.pow(filterData_byPosture[i][position_z_index+3],2))))
#
#         filterData_byPosture.sort(key=itemgetter(13))
#         saveDataToFile("posture "+str(postureNo)+" failure joint="+str(failure_joint_No)+"angle="+str(angle)+".txt",filterData_byPosture)
#
#         ## screen by min distance ##
#         if len(filterData_byPosture) > 1:
#             indexData_byMinDis = searchDataIndex(filterData_byPosture,[filterData_byPosture[0][13],filterData_byPosture[0][13]],13)
#             filterData_byMinDis = copySpecificData(filterData_byPosture,indexData_byMinDis)
#             filterData_byPosture = deepcopy(filterData_byMinDis)
#
#         for angleNo in range(0,4):
#             ## screen by min diff angle ##
#             if len(filterData_byPosture) > 1:
#                 for j in range(0,len(filterData_byPosture)):
#                     filterData_byPosture[j].append(abs(target_config_posture[postureNo][angleNo]-filterData_byPosture[j][angleNo]))
#                 filterData_byPosture.sort(key=itemgetter(14+angleNo))
#                 indexData_byMinDiffAngle = searchDataIndex(filterData_byPosture,[filterData_byPosture[0][14+angleNo],filterData_byPosture[0][14+angleNo]],14+angleNo)
#                 filterData_byMinDiffAngle = copySpecificData(filterData_byPosture,indexData_byMinDiffAngle)
#                 filterData_byPosture = deepcopy(filterData_byMinDiffAngle)
#             else:
#                 break
#
#         qualified_posture_set_by_angle.append(filterData_byPosture[0])
#         saveDataToFile("posture "+str(postureNo)+"failure joint="+str(failure_joint_No)+"angle="+str(angle)+"_min.txt",filterData_byPosture)
#
#     saveDataToFile("posture Set failure joint = "+str(failure_joint_No)+" angle = "+str(angle)+".txt",qualified_posture_set_by_angle)
#
#     score = []
#     score.append(angle)
#     for calPointCount in range(0,len(qualified_posture_set_by_angle)):
#         score.append(qualified_posture_set_by_angle[calPointCount][13]*weight_for_calScore[calPointCount])
#
#     sumScore = 0
#     for sumScoreCount in range(1,len(score)):
#         sumScore += score[sumScoreCount]
#     score.append(sumScore)
#     posture_score.append(score)
#
# print "time finish",time.clock()
# posture_score.sort(key=itemgetter(len(posture_score[0])-1))
# saveDataToFile("score for failure joint = "+str(failure_joint_No)+".txt",posture_score)
#################################################################################################################################################################
