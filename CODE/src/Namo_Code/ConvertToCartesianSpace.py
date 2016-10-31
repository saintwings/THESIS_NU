import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
from sympy import symbols, Matrix , Symbol , exp , sin ,cos , sqrt , diff

# def randrange(n, vmin, vmax):
#     return (vmax-vmin)*np.random.rand(n) + vmin
# 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# n = 100
# for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#     xs = randrange(n, 23, 32)
#     ys = randrange(n, 0, 100)
#     zs = randrange(n, zl, zh)
#     ax.scatter(xs, ys, zs, c=c, marker=m)
# 
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# 
# plt.show()
def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

## declare variables ##
def kinematic(str_fileName,plotKeyframe):
    #str_fileName = "p1"
    #int_numberOfKeyframe = 0
    int_motorDirection = [1,-1,1,-1,1,-1,-1   ,-1,-1,1,1,1,-1,1   ,1,-1,1]
    
    # read motor center value #
    file_center = open('motor_center.txt', 'r')
    int_motorCenterValue = file_center.read()
    file_center.close()
    int_motorCenterValue = int_motorCenterValue.split('\n')
    print "motor center"
    print  int_motorCenterValue
    for x in range (17):
        int_motorCenterValue[x] = int(int_motorCenterValue[x])
    int_motorValue = [[int_motorCenterValue[x] for x in range (17)] for y in range (30)]
    
    
    # read motor value #
    namePosture = str_fileName + '.txt'
    print namePosture
    file_posture = open(namePosture, 'r')
    str_load_data = file_posture.read()
    file_posture.close()
    str_load_data = str_load_data.split('\n')
    int_numberOfKeyframe = int(str_load_data[0])
    int_count_data = 1
    for x in range (int_numberOfKeyframe):
        for y in range (17):
            int_motorValue[x][y] = int(str_load_data[int_count_data])
            int_count_data = int_count_data + 1
    print"key frame amount"
    print int_numberOfKeyframe
    print"motor value all keyframe"
    print int_motorValue
    
    
    # cal diff from center value #
    int_motorValueDiff = [[(int_motorValue[y][x]-int_motorCenterValue[x]) for x in range (17)] for y in range (int_numberOfKeyframe)]
    print"motor value diff all keyframe"
    print int_motorValueDiff
    
    # convert to degree #
    float_motorValueDiff_degree = [[(int_motorValueDiff[y][x]*359/4095.0) for x in range (17)] for y in range (int_numberOfKeyframe)]
    print"motor value diff all keyframe in degree"
    print float_motorValueDiff_degree
    print float_motorValueDiff_degree[int_numberOfKeyframe-1]
    
    # convert motor direction #
    float_motorValueDiff_degree = [[(float_motorValueDiff_degree[y][x]*int_motorDirection[x]) for x in range (17)] for y in range (int_numberOfKeyframe)]
    print"motor value diff all keyframe in degree"
    print float_motorValueDiff_degree
    print float_motorValueDiff_degree[int_numberOfKeyframe-1]
    
    
    
    
    alpha0_r = math.radians(90)
    alpha1_r = math.radians(90)
    alpha2_r = math.radians(-90)
    alpha3_r = math.radians(90)
    alpha4_r = math.radians(-90)
    alpha5_r = math.radians(90)
    alpha6_r = math.radians(90)
    alpha7_r = math.radians(0)
    
    alpha0_l = math.radians(90)
    alpha1_l = math.radians(90)
    alpha2_l = math.radians(-90)
    alpha3_l = math.radians(90)
    alpha4_l = math.radians(-90)
    alpha5_l = math.radians(90)
    alpha6_l = math.radians(90)
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
        theta1_l = math.radians((float_motorValueDiff_degree[0][0])/3.0+90)
        theta2_l = math.radians(float_motorValueDiff_degree[0][1]+90)
        theta3_l = math.radians(float_motorValueDiff_degree[0][2]-90)
        theta4_l = math.radians(float_motorValueDiff_degree[0][3])
        theta5_l = math.radians(float_motorValueDiff_degree[0][4]+90)
        theta6_l = math.radians(float_motorValueDiff_degree[0][5]-90)
        theta7_l = math.radians(float_motorValueDiff_degree[0][6])
        theta8_l = math.radians(0)
         
        theta1_r = math.radians((float_motorValueDiff_degree[0][7])/3.0+90)
        theta2_r = math.radians(float_motorValueDiff_degree[0][8]+90)
        theta3_r = math.radians(float_motorValueDiff_degree[0][9]-90)
        theta4_r = math.radians(float_motorValueDiff_degree[0][10])
        theta5_r = math.radians(float_motorValueDiff_degree[0][11]+90)
        theta6_r = math.radians(float_motorValueDiff_degree[0][12]-90)
        theta7_r = math.radians(float_motorValueDiff_degree[0][13])
        theta8_r = math.radians(0)
    
    elif plotKeyframe == "last":
    
        theta1_l = math.radians((float_motorValueDiff_degree[int_numberOfKeyframe-1][0])/3.0+90)
        theta2_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][1]+90)
        theta3_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][2]-90)
        theta4_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][3])
        theta5_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][4]+90)
        theta6_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][5]-90)
        theta7_l = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][6])
        theta8_l = math.radians(0)
         
        theta1_r = math.radians((float_motorValueDiff_degree[int_numberOfKeyframe-1][7])/3.0+90)
        theta2_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][8]+90)
        theta3_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][9]-90)
        theta4_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][10])
        theta5_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][11]+90)
        theta6_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][12]-90)
        theta7_r = math.radians(float_motorValueDiff_degree[int_numberOfKeyframe-1][13])
        theta8_r = math.radians(0)
    
    
    # theta1_l = math.radians(0+90)
    # theta2_l = math.radians(0+90)
    # theta3_l = math.radians(0-90)
    # theta4_l = math.radians(0)
    # theta5_l = math.radians(0+90)
    # theta6_l = math.radians(0-90)
    # theta7_l = math.radians(0)
    # theta8_l = math.radians(0)
    #  
    # theta1_r = math.radians(90+90)
    # theta2_r = math.radians(0+90)
    # theta3_r = math.radians(0-90)
    # theta4_r = math.radians(0)
    # theta5_r = math.radians(0+90)
    # theta6_r = math.radians(0-90)
    # theta7_r = math.radians(0)
    # theta8_r = math.radians(0)
    
    t01_r = Matrix ((    [(cos(theta1_r))                  , (-sin(theta1_r))                 , 0                    , a0_r                  ],
                         [(sin(theta1_r)*(cos(alpha0_r)))  , (cos(theta1_r))*(cos(alpha0_r))  , (-sin(alpha0_r))     , (-sin(alpha0_r))*d1_r ],
                         [(sin(theta1_r)*(sin(alpha0_r)))  , (cos(theta1_r))*(sin(alpha0_r))  , (cos(alpha0_r))      , (cos(alpha0_r))*d1_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t12_r = Matrix ((    [(cos(theta2_r))                  , (-sin(theta2_r))                 , 0                    , a1_r                  ],
                         [(sin(theta2_r)*(cos(alpha1_r)))  , (cos(theta2_r))*(cos(alpha1_r))  , (-sin(alpha1_r))     , (-sin(alpha1_r))*d2_r ],
                         [(sin(theta2_r)*(sin(alpha1_r)))  , (cos(theta2_r))*(sin(alpha1_r))  , (cos(alpha1_r))      , (cos(alpha1_r))*d2_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t23_r = Matrix ((    [(cos(theta3_r))                  , (-sin(theta3_r))                 , 0                    , a2_r                  ],
                         [(sin(theta3_r)*(cos(alpha2_r)))  , (cos(theta3_r))*(cos(alpha2_r))  , (-sin(alpha2_r))     , (-sin(alpha2_r))*d3_r ],
                         [(sin(theta3_r)*(sin(alpha2_r)))  , (cos(theta3_r))*(sin(alpha2_r))  , (cos(alpha2_r))      , (cos(alpha2_r))*d3_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t34_r = Matrix ((    [(cos(theta4_r))                  , (-sin(theta4_r))                 , 0                    , a3_r                  ],
                         [(sin(theta4_r)*(cos(alpha3_r)))  , (cos(theta4_r))*(cos(alpha3_r))  , (-sin(alpha3_r))     , (-sin(alpha3_r))*d4_r ],
                         [(sin(theta4_r)*(sin(alpha3_r)))  , (cos(theta4_r))*(sin(alpha3_r))  , (cos(alpha3_r))      , (cos(alpha3_r))*d4_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t45_r = Matrix ((    [(cos(theta5_r))                  , (-sin(theta5_r))                 , 0                    , a4_r                  ],
                         [(sin(theta5_r)*(cos(alpha4_r)))  , (cos(theta5_r))*(cos(alpha4_r))  , (-sin(alpha4_r))     , (-sin(alpha4_r))*d5_r ],
                         [(sin(theta5_r)*(sin(alpha4_r)))  , (cos(theta5_r))*(sin(alpha4_r))  , (cos(alpha4_r))      , (cos(alpha4_r))*d5_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t56_r = Matrix ((    [(cos(theta6_r))                  , (-sin(theta6_r))                 , 0                    , a5_r                  ],
                         [(sin(theta6_r)*(cos(alpha5_r)))  , (cos(theta6_r))*(cos(alpha5_r))  , (-sin(alpha5_r))     , (-sin(alpha5_r))*d6_r ],
                         [(sin(theta6_r)*(sin(alpha5_r)))  , (cos(theta6_r))*(sin(alpha5_r))  , (cos(alpha5_r))      , (cos(alpha5_r))*d6_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t67_r = Matrix ((    [(cos(theta7_r))                  , (-sin(theta7_r))                 , 0                    , a6_r                  ],
                         [(sin(theta7_r)*(cos(alpha6_r)))  , (cos(theta7_r))*(cos(alpha6_r))  , (-sin(alpha6_r))     , (-sin(alpha6_r))*d7_r ],
                         [(sin(theta7_r)*(sin(alpha6_r)))  , (cos(theta7_r))*(sin(alpha6_r))  , (cos(alpha6_r))      , (cos(alpha6_r))*d7_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t78_r = Matrix ((    [(cos(theta8_r))                  , (-sin(theta8_r))                 , 0                    , a7_r                  ],
                         [(sin(theta8_r)*(cos(alpha7_r)))  , (cos(theta8_r))*(cos(alpha7_r))  , (-sin(alpha7_r))     , (-sin(alpha7_r))*d8_r ],
                         [(sin(theta8_r)*(sin(alpha7_r)))  , (cos(theta8_r))*(sin(alpha7_r))  , (cos(alpha7_r))      , (cos(alpha7_r))*d8_r  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    
    
    t02_r = t01_r * t12_r
    t03_r = t02_r * t23_r
    t04_r = t03_r * t34_r
    t05_r = t04_r * t45_r
    t06_r = t05_r * t56_r
    t07_r = t06_r * t67_r
    t08_r = t07_r * t78_r
    #t08_r = t01_r * t12_r * t23_r * t34_r * t45_r * t56_r * t67_r * t78_r 
    #print t08_r
    #print t08_r[0,3]
    #print t08_r[1,3]
    #print t08_r[2,3]
    #print t08_r[3,3]
    
    pointSet_r = [[t01_r[0,3],t01_r[1,3],t01_r[2,3]],
                  [t02_r[0,3],t02_r[1,3],t02_r[2,3]],
                  [t03_r[0,3],t03_r[1,3],t03_r[2,3]],
                  [t04_r[0,3],t04_r[1,3],t04_r[2,3]],
                  [t05_r[0,3],t05_r[1,3],t05_r[2,3]],
                  [t06_r[0,3],t06_r[1,3],t06_r[2,3]],
                  [t07_r[0,3],t07_r[1,3],t07_r[2,3]],
                  [t08_r[0,3],t08_r[1,3],t08_r[2,3]],]
    print "pointset R = "
    print pointSet_r
    
    t01_l = Matrix ((    [(cos(theta1_l))                  , (-sin(theta1_l))                 , 0                    , a0_l                  ],
                         [(sin(theta1_l)*(cos(alpha0_l)))  , (cos(theta1_l))*(cos(alpha0_l))  , (-sin(alpha0_l))     , (-sin(alpha0_l))*d1_l ],
                         [(sin(theta1_l)*(sin(alpha0_l)))  , (cos(theta1_l))*(sin(alpha0_l))  , (cos(alpha0_l))      , (cos(alpha0_l))*d1_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t12_l = Matrix ((    [(cos(theta2_l))                  , (-sin(theta2_l))                 , 0                    , a1_l                  ],
                         [(sin(theta2_l)*(cos(alpha1_l)))  , (cos(theta2_l))*(cos(alpha1_l))  , (-sin(alpha1_l))     , (-sin(alpha1_l))*d2_l ],
                         [(sin(theta2_l)*(sin(alpha1_l)))  , (cos(theta2_l))*(sin(alpha1_l))  , (cos(alpha1_l))      , (cos(alpha1_l))*d2_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t23_l = Matrix ((    [(cos(theta3_l))                  , (-sin(theta3_l))                 , 0                    , a2_l                  ],
                         [(sin(theta3_l)*(cos(alpha2_l)))  , (cos(theta3_l))*(cos(alpha2_l))  , (-sin(alpha2_l))     , (-sin(alpha2_l))*d3_l ],
                         [(sin(theta3_l)*(sin(alpha2_l)))  , (cos(theta3_l))*(sin(alpha2_l))  , (cos(alpha2_l))      , (cos(alpha2_l))*d3_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t34_l = Matrix ((    [(cos(theta4_l))                  , (-sin(theta4_l))                 , 0                    , a3_l                  ],
                         [(sin(theta4_l)*(cos(alpha3_l)))  , (cos(theta4_l))*(cos(alpha3_l))  , (-sin(alpha3_l))     , (-sin(alpha3_l))*d4_l ],
                         [(sin(theta4_l)*(sin(alpha3_l)))  , (cos(theta4_l))*(sin(alpha3_l))  , (cos(alpha3_l))      , (cos(alpha3_l))*d4_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t45_l = Matrix ((    [(cos(theta5_l))                  , (-sin(theta5_l))                 , 0                    , a4_l                  ],
                         [(sin(theta5_l)*(cos(alpha4_l)))  , (cos(theta5_l))*(cos(alpha4_l))  , (-sin(alpha4_l))     , (-sin(alpha4_l))*d5_l ],
                         [(sin(theta5_l)*(sin(alpha4_l)))  , (cos(theta5_l))*(sin(alpha4_l))  , (cos(alpha4_l))      , (cos(alpha4_l))*d5_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t56_l = Matrix ((    [(cos(theta6_l))                  , (-sin(theta6_l))                 , 0                    , a5_l                  ],
                         [(sin(theta6_l)*(cos(alpha5_l)))  , (cos(theta6_l))*(cos(alpha5_l))  , (-sin(alpha5_l))     , (-sin(alpha5_l))*d6_l ],
                         [(sin(theta6_l)*(sin(alpha5_l)))  , (cos(theta6_l))*(sin(alpha5_l))  , (cos(alpha5_l))      , (cos(alpha5_l))*d6_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t67_l = Matrix ((    [(cos(theta7_l))                  , (-sin(theta7_l))                 , 0                    , a6_l                  ],
                         [(sin(theta7_l)*(cos(alpha6_l)))  , (cos(theta7_l))*(cos(alpha6_l))  , (-sin(alpha6_l))     , (-sin(alpha6_l))*d7_l ],
                         [(sin(theta7_l)*(sin(alpha6_l)))  , (cos(theta7_l))*(sin(alpha6_l))  , (cos(alpha6_l))      , (cos(alpha6_l))*d7_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    t78_l = Matrix ((    [(cos(theta8_l))                  , (-sin(theta8_l))                 , 0                    , a7_l                  ],
                         [(sin(theta8_l)*(cos(alpha7_l)))  , (cos(theta8_l))*(cos(alpha7_l))  , (-sin(alpha7_l))     , (-sin(alpha7_l))*d8_l ],
                         [(sin(theta8_l)*(sin(alpha7_l)))  , (cos(theta8_l))*(sin(alpha7_l))  , (cos(alpha7_l))      , (cos(alpha7_l))*d8_l  ],
                         [0                                ,  0                               , 0                    , 1                     ]))
    
    
    
    t02_l = t01_l * t12_l
    t03_l = t02_l * t23_l
    t04_l = t03_l * t34_l
    t05_l = t04_l * t45_l
    t06_l = t05_l * t56_l
    t07_l = t06_l * t67_l
    t08_l = t07_l * t78_l
    #t08_l = t01_l * t12_l * t23_l * t34_l * t45_l * t56_l * t67_l * t78_l 
    #print t08_l
    #print t08_l[0,3]
    #print t08_l[1,3]
    #print t08_l[2,3]
    #print t08_l[3,3]
    
    pointSet_l = [[t01_l[0,3],t01_l[1,3],t01_l[2,3]],
                  [t02_l[0,3],t02_l[1,3],t02_l[2,3]],
                  [t03_l[0,3],t03_l[1,3],t03_l[2,3]],
                  [t04_l[0,3],t04_l[1,3],t04_l[2,3]],
                  [t05_l[0,3],t05_l[1,3],t05_l[2,3]],
                  [t06_l[0,3],t06_l[1,3],t06_l[2,3]],
                  [t07_l[0,3],t07_l[1,3],t07_l[2,3]],
                  [t08_l[0,3],t08_l[1,3],t08_l[2,3]],]
    print "pointset L = "
    print pointSet_l
    
    
    #data_x = [1 ,2, 3 ,4]
    #data_y = [1 ,2, 3, 4]
    #data_z = [1, 2, 3, 4]
    data_x_l = [pointSet_l[0][0],pointSet_l[1][0],pointSet_l[2][0],pointSet_l[3][0],pointSet_l[4][0],pointSet_l[5][0],pointSet_l[6][0],pointSet_l[7][0]]
    data_y_l = [pointSet_l[0][1],pointSet_l[1][1],pointSet_l[2][1],pointSet_l[3][1],pointSet_l[4][1],pointSet_l[5][1],pointSet_l[6][1],pointSet_l[7][1]]
    data_z_l = [pointSet_l[0][2],pointSet_l[1][2],pointSet_l[2][2],pointSet_l[3][2],pointSet_l[4][2],pointSet_l[5][2],pointSet_l[6][2],pointSet_l[7][2]]
    
    data_x_r = [pointSet_r[0][0],pointSet_r[1][0],pointSet_r[2][0],pointSet_r[3][0],pointSet_r[4][0],pointSet_r[5][0],pointSet_r[6][0],pointSet_r[7][0]]
    data_y_r = [pointSet_r[0][1],pointSet_r[1][1],pointSet_r[2][1],pointSet_r[3][1],pointSet_r[4][1],pointSet_r[5][1],pointSet_r[6][1],pointSet_r[7][1]]
    data_z_r = [pointSet_r[0][2],pointSet_r[1][2],pointSet_r[2][2],pointSet_r[3][2],pointSet_r[4][2],pointSet_r[5][2],pointSet_r[6][2],pointSet_r[7][2]]
    
    data = [data_x_l,data_y_l,data_z_l,data_x_r,data_y_r,data_z_r]

    return data 













data_p1 = kinematic("p1","last")
data_p2 = kinematic("p2","last")
data_p3 = kinematic("p3","last")
data_p4 = kinematic("p4","last")
data_p5 = kinematic("p5","last")

data_p5_f = kinematic("p5","first")


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zl, zh)
   
    ax.plot(data_p1[0],data_p1[1], data_p1[2], c=u'b', marker=u's')
    ax.plot(data_p1[3],data_p1[4], data_p1[5], c=u'b', marker=u'p')
    
    ax.plot(data_p2[0],data_p2[1], data_p2[2], c=u'r', marker=u's')
    ax.plot(data_p2[3],data_p2[4], data_p2[5], c=u'r', marker=u'p')
    
    ax.plot(data_p3[0],data_p3[1], data_p3[2], c=u'g', marker=u's')
    ax.plot(data_p3[3],data_p3[4], data_p3[5], c=u'g', marker=u'p')
    
    ax.plot(data_p4[0],data_p4[1], data_p4[2], c=u'y', marker=u's')
    ax.plot(data_p4[3],data_p4[4], data_p4[5], c=u'y', marker=u'p')
    
    ax.plot(data_p5[0],data_p5[1], data_p5[2], c=u'c', marker=u's')
    ax.plot(data_p5[3],data_p5[4], data_p5[5], c=u'c', marker=u'p')
    
    ax.plot(data_p5_f[0],data_p5_f[1], data_p5_f[2], c=u'c', marker=u's')
    ax.plot(data_p5_f[3],data_p5_f[4], data_p5_f[5], c=u'c', marker=u'p')
  
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

plt.show()





