from ast import literal_eval
import random
from copy import deepcopy
import math
from sympy import symbols, Matrix, Symbol, exp, sin, cos, sqrt, diff
from operator import itemgetter
import copy
import numpy as np

def loadDataFromFile(fileName):
    with open(fileName) as f:
        data = [list(literal_eval(line)) for line in f]
    return data

def saveDataToFile(fileName,data):
    file_data = open(fileName, 'w')
    for item in data:
        file_data.write("%s\n"% item)
    file_data.close()

def calKinematicNamo_numpy(degree7Joint,armSide):
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
    #print("7dof ="+str(degree7Joint))
    ## DH parameter >> theta[1,2,...7,end effector]
    theta = [math.radians(degree7Joint[0] + 90),math.radians(degree7Joint[1] + 90),math.radians(degree7Joint[2] - 90),
             math.radians(degree7Joint[3]),math.radians(degree7Joint[4] + 90),math.radians(degree7Joint[5] - 90),
             math.radians(degree7Joint[6]),math.radians(0)]
    T = {}
    for i in range(0,8):
        #print i

        T[i] = np.array([[(cos(theta[i])), (-sin(theta[i])), 0, a[i]],
                       [(sin(theta[i]) * (cos(alpha[i]))), (cos(theta[i])) * (cos(alpha[i])), (-sin(alpha[i])),
                        (-sin(alpha[i])) * d[i]],
                       [(sin(theta[i]) * (sin(alpha[i]))), (cos(theta[i])) * (sin(alpha[i])), (cos(alpha[i])),
                        (cos(alpha[i])) * d[i]],
                       [0, 0, 0, 1]])


    T01 = T[0]
    T02 = np.dot(T01,T[1])
    T03 = np.dot(T02,T[2])
    T04 = np.dot(T03,T[3])
    T05 = np.dot(T04,T[4])
    T06 = np.dot(T05,T[5])
    T07 = np.dot(T06,T[6])
    T0E = np.dot(T07,T[7])
    return [T01,T02,T03,T04,T05,T06,T07,T0E]


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
    #print("7dof ="+str(degree7Joint))
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

def cal_Avg_Angle(ref_posture,angle_Amount):
    angle_avg = []
    for i in range(0,angle_Amount):
        #print "angle No. = ",i
        temp = 0
        for j in range(0,len(ref_posture)):
            #print "angle Value = ",ref_posture[j][i]
            temp = temp + ref_posture[j][i]

        temp_avg = float(temp)/len(ref_posture)
        angle_avg.append(temp_avg)
    #print angle_avg

    return angle_avg


def add_fixed_jointAngle_to_vector(joint_fixed, joint_fixed_value,vector):
    new_vector = copy.copy(vector)
    new_vector.insert(joint_fixed, joint_fixed_value)
    return new_vector

def random_Posture_Angles(angle_limit,angle_amount,random_amount):
    data = []
    for i in range(random_amount):
        angle_random_set = []
        for j in range(angle_amount):
            angle = random.randint(angle_limit[j][0],angle_limit[j][1])
            angle_random_set.append(angle)

        data.append(angle_random_set)

    return data

def set_FixAngleValueToData(data,angle_fixed_index,fixed_value):
    data_fixed = deepcopy(data)
    for i in range(len(data)):
        data_fixed[i][angle_fixed_index] = fixed_value

    return data_fixed


def cal_Single_Posture_Quaternion(posture, T_matrix_posture):
    quaternion = calQuaternion(T_matrix_posture[7])
    return quaternion

def cal_Single_Posture_Score(T_matrix_ref, Q_ref, T_matrix, Q, score_weight):
    score = []

    Q_diff = [Q_ref[0] - Q[0], Q_ref[1] - Q[1], Q_ref[2] - Q[2], Q_ref[3] - Q[3]]

    norm_Q_diff = math.sqrt(
        (Q_diff[0] * Q_diff[0]) + (Q_diff[1] * Q_diff[1]) + (Q_diff[2] * Q_diff[2]) + (Q_diff[3] * Q_diff[3]))
    # elbow_diff =[TMatrix_Target_Posture[3][0,3] - T_Matrix[3][0,3], TMatrix_Target_Posture[3][1,3] - T_Matrix[3][1,3], TMatrix_Target_Posture[3][2,3] - T_Matrix[3][2,3]]
    norm_elbow_diff = math.sqrt(pow(T_matrix_ref[3][0, 3] - T_matrix[3][0, 3], 2) + pow(
        T_matrix_ref[3][1, 3] - T_matrix[3][1, 3], 2) + pow(
        T_matrix_ref[3][2, 3] - T_matrix[3][2, 3], 2))
    # wrist_diff =[TMatrix_Target_Posture[4][0,3] - T_Matrix[4][0,3], TMatrix_Target_Posture[4][1,3] - T_Matrix[4][1,3], TMatrix_Target_Posture[4][2,3] - T_Matrix[4][2,3]]
    norm_wrist_diff = math.sqrt(pow(T_matrix_ref[4][0, 3] - T_matrix[4][0, 3], 2) + pow(
        T_matrix_ref[4][1, 3] - T_matrix[4][1, 3], 2) + pow(
        T_matrix_ref[4][2, 3] - T_matrix[4][2, 3], 2))
    sum_diff = norm_Q_diff * score_weight[0] + norm_elbow_diff * score_weight[1] + norm_wrist_diff * score_weight[2]

    #score.append(Q_diff)
    score.append(norm_Q_diff)
    score.append(norm_elbow_diff)
    score.append(norm_wrist_diff)
    score.append(sum_diff)

    return score


def cal_Posture_Score(set_of_posture,reference_posture,score_weight):
    set_of_posture_scored = deepcopy(set_of_posture)
    TMatrix_Target_Posture = calKinematicNamo(reference_posture,'R')
    Q_ref = calQuaternion(TMatrix_Target_Posture[7])

    for i in range(len(set_of_posture_scored)):

        T_Matrix = calKinematicNamo(set_of_posture_scored[i],'R')
        Q = calQuaternion(T_Matrix[7])
        Q_diff =[Q_ref[0]-Q[0], Q_ref[1]-Q[1], Q_ref[2]-Q[2], Q_ref[3]-Q[3]]
        norm_Q_diff = math.sqrt((Q_diff[0]*Q_diff[0])+(Q_diff[1]*Q_diff[1])+(Q_diff[2]*Q_diff[2])+(Q_diff[3]*Q_diff[3]))
        #elbow_diff =[TMatrix_Target_Posture[3][0,3] - T_Matrix[3][0,3], TMatrix_Target_Posture[3][1,3] - T_Matrix[3][1,3], TMatrix_Target_Posture[3][2,3] - T_Matrix[3][2,3]]
        norm_elbow_diff = math.sqrt(pow(TMatrix_Target_Posture[3][0,3] - T_Matrix[3][0,3],2) + pow(TMatrix_Target_Posture[3][1,3] - T_Matrix[3][1,3],2) + pow(TMatrix_Target_Posture[3][2,3] - T_Matrix[3][2,3],2))
        #wrist_diff =[TMatrix_Target_Posture[4][0,3] - T_Matrix[4][0,3], TMatrix_Target_Posture[4][1,3] - T_Matrix[4][1,3], TMatrix_Target_Posture[4][2,3] - T_Matrix[4][2,3]]
        norm_wrist_diff = math.sqrt(pow(TMatrix_Target_Posture[4][0,3] - T_Matrix[4][0,3],2) + pow(TMatrix_Target_Posture[4][1,3] - T_Matrix[4][1,3],2) + pow(TMatrix_Target_Posture[4][2,3] - T_Matrix[4][2,3],2))
        sum_diff =  norm_Q_diff*score_weight[0] + norm_elbow_diff*score_weight[1] + norm_wrist_diff*score_weight[2]

        set_of_posture_scored[i].append(norm_Q_diff)
        set_of_posture_scored[i].append(norm_elbow_diff)
        set_of_posture_scored[i].append(norm_wrist_diff)
        set_of_posture_scored[i].append(sum_diff)

    return set_of_posture_scored

def cal_Posture_Score_2(set_of_posture,reference_posture,score_weight):
    set_of_posture_scored = deepcopy(set_of_posture)
    TMatrix_Target_Posture = calKinematicNamo(reference_posture,'R')
    Q_ref = calQuaternion(TMatrix_Target_Posture[7])

    for i in range(len(set_of_posture_scored)):

        T_Matrix = calKinematicNamo(set_of_posture_scored[i],'R')
        Q = calQuaternion(T_Matrix[7])
        Q_diff =[Q_ref[0]-Q[0], Q_ref[1]-Q[1], Q_ref[2]-Q[2], Q_ref[3]-Q[3]]
        norm_Q_diff = math.sqrt((Q_diff[0]*Q_diff[0])+(Q_diff[1]*Q_diff[1])+(Q_diff[2]*Q_diff[2])+(Q_diff[3]*Q_diff[3]))
        #elbow_diff =[TMatrix_Target_Posture[3][0,3] - T_Matrix[3][0,3], TMatrix_Target_Posture[3][1,3] - T_Matrix[3][1,3], TMatrix_Target_Posture[3][2,3] - T_Matrix[3][2,3]]
        norm_elbow_diff = math.sqrt(pow(TMatrix_Target_Posture[3][0,3] - T_Matrix[3][0,3],2) + pow(TMatrix_Target_Posture[3][1,3] - T_Matrix[3][1,3],2) + pow(TMatrix_Target_Posture[3][2,3] - T_Matrix[3][2,3],2))
        #wrist_diff =[TMatrix_Target_Posture[4][0,3] - T_Matrix[4][0,3], TMatrix_Target_Posture[4][1,3] - T_Matrix[4][1,3], TMatrix_Target_Posture[4][2,3] - T_Matrix[4][2,3]]
        norm_wrist_diff = math.sqrt(pow(TMatrix_Target_Posture[4][0,3] - T_Matrix[4][0,3],2) + pow(TMatrix_Target_Posture[4][1,3] - T_Matrix[4][1,3],2) + pow(TMatrix_Target_Posture[4][2,3] - T_Matrix[4][2,3],2))
        sum_diff =  norm_Q_diff*score_weight[0] + norm_elbow_diff*score_weight[1] + norm_wrist_diff*score_weight[2]

        set_of_posture_scored[i].append(norm_Q_diff)
        set_of_posture_scored[i].append(norm_elbow_diff)
        set_of_posture_scored[i].append(norm_wrist_diff)
        set_of_posture_scored[i].append(sum_diff)

    return set_of_posture_scored

def weighted_random(weights):
    number = random.random() * sum(weights.values())
    for k,v in weights.iteritems():
        if number < v:
            break
        number -= v
    return k

def run_GA(data,angle_limit,crossOver_amount,mutation_amount,reproduction_amount,fixed_angle_index):



    ### define random weight ###
    rand_weight ={}
    n = crossOver_amount
    n_amount = n*(n+1)/2
    for i in range(n) :
        rand_weight[i] = (float(n-i))/n_amount

    ### cross over section ###
    temp_data = deepcopy(data)
    crossOver_data = []
    while (len(crossOver_data) < crossOver_amount) :
        rand_index = random.randint(1,(len(angle_limit)-1))
        rand_data0_index = weighted_random(rand_weight)
        rand_data1_index = weighted_random(rand_weight)

        rand_data0 = temp_data[rand_data0_index]
        rand_data1 = temp_data[rand_data1_index]

        frag_cross_data0_0 = rand_data0[:rand_index]
        frag_cross_data0_1 = rand_data0[rand_index:len(angle_limit)]

        frag_cross_data1_0 = rand_data1[:rand_index]
        frag_cross_data1_1 = rand_data1[rand_index:len(angle_limit)]

        cross_data0 = deepcopy(frag_cross_data0_0)
        for i in range(len(frag_cross_data1_1)):
            cross_data0.append(frag_cross_data1_1[i])

        cross_data1 = deepcopy(frag_cross_data1_0)
        for i in range(len(frag_cross_data0_1)):
            cross_data1.append(frag_cross_data0_1[i])

        crossOver_data.append(cross_data0)
        crossOver_data.append(cross_data1)
        # print "cross in dex =",rand_index
        # print "rand_data0 = ",rand_data0
        # print "rand_data1 = ",rand_data1
        # print "frag_cross_data0_0 = ",frag_cross_data0_0
        # print "frag_cross_data0_1 = ",frag_cross_data0_1
        # print "frag_cross_data1_0 = ",frag_cross_data1_0
        # print "frag_cross_data1_1 = ",frag_cross_data1_1
        # print "cross data 0 =",cross_data0
        # print "cross data 1 =",cross_data1

    ### mutation section ###
    mutation_data =[]
    selected_for_mutate_data = deepcopy(data[:mutation_amount])
    for i in range(len(selected_for_mutate_data)):
        mutation_data.append(selected_for_mutate_data[i][:len(angle_limit)])
        #print "mutation_data = ",mutation_data[i]

    for mutation_i in range(mutation_amount):
        while(1):
            mutate_index = random.randint(0,(len(angle_limit)-1))
            #print "mutate index = ",mutate_index
            if (mutate_index != fixed_angle_index):
                break

        mutate_value = random.randint(angle_limit[mutate_index][0],angle_limit[mutate_index][1])
        mutation_data[mutation_i][mutate_index] = mutate_value
        #print 'mutation_data[mutation_i][mutate_index]=',mutation_data[mutation_i][mutate_index]

    #for i in range(len(mutation_data)):
        #print "mutation_data = ",mutation_data[i]

    ### reproduction section ###
    reproduction_data =[]
    selected_for_reproduction_data = deepcopy(data[:reproduction_amount])
    for i in range(len(selected_for_reproduction_data)):
        reproduction_data.append(selected_for_reproduction_data[i][:len(angle_limit)])

   # print reproduction_data

    ga_data = []
    for i in range(len(crossOver_data)):
        ga_data.append(crossOver_data[i])
    for i in range(len(mutation_data)):
        ga_data.append(mutation_data[i])
    for i in range(len(reproduction_data)):
        ga_data.append(reproduction_data[i])
    return ga_data

def run_GA_Scored_Sorted(data,original_posture_config,angle_limit,score_weight,crossover_amount,mutation_amount,reproduction_amount,generation_count):
        ### GA ###

    data_posture_joint_scored_sorted = deepcopy(data)

    GA_data_posture=[]
    for i_posture in range(len(original_posture_config)):
        GA_data_posture_joint =[]
        for i_angle in range(len(angle_limit)):
            GA_data_posture_joint.append(run_GA(data_posture_joint_scored_sorted[i_posture][i_angle],angle_limit,crossover_amount,mutation_amount,reproduction_amount,i_angle))

        GA_data_posture.append(GA_data_posture_joint)


    #print 'GA_data_posture',len(GA_data_posture)
    #print 'GA_data_posture[0]',len(GA_data_posture[0])

    ### cal score GA###
    GA_data_posture_scored_byRefPosture = []
    for i_posture in range(len(original_posture_config)):
        GA_data_posture_scored_byRefPosture_joint =[]
        for i_angle in range(len(angle_limit)):
            GA_data_posture_scored_byRefPosture_joint.append(cal_Posture_Score(GA_data_posture[i_posture][i_angle],original_posture_config[i_posture],score_weight))

        GA_data_posture_scored_byRefPosture.append(GA_data_posture_scored_byRefPosture_joint)

    #print 'GA_data_posture_scored_byRefPosture',len(GA_data_posture_scored_byRefPosture)
    #print 'GA_data_posture_scored_byRefPosture[0]',len(GA_data_posture_scored_byRefPosture[0])


    ### sort data GA ###
    GA_data_posture_scored_byRefPosture_sorted = deepcopy(GA_data_posture_scored_byRefPosture)
    for i_posture in range(len(original_posture_config)):
        for i_angle in range(len(angle_limit)):
            GA_data_posture_scored_byRefPosture_sorted[i_posture][i_angle].sort(key=itemgetter(10))
            saveDataToFile('./GA_data/gen'+str(generation_count)+'GA_data_posture_scored_byRefPosture_sorted['+str(i_posture)+']['+str(i_angle)+'].txt',GA_data_posture_scored_byRefPosture_sorted[i_posture][i_angle])
    ###

    return GA_data_posture_scored_byRefPosture_sorted












# ### GA ###
# GA_data_posture=[]
# for i_posture in range(len(original_posture_config)):
#     GA_data_posture_joint =[]
#     for i_angle in range(len(random_angle_set_fixed)):
#         GA_data_posture_joint.append(run_GA(random_angle_set_fixed_scored_byRefPosture_sorted[i_posture][i_angle],angle_limit,crossover_amount,mutation_amount,reproduction_amount,i_angle))
#
#     GA_data_posture.append(GA_data_posture_joint)
#
#
# print 'GA_data_posture',len(GA_data_posture)
# print 'GA_data_posture[0]',len(GA_data_posture[0])
#
# ### cal score GA###
# GA_data_posture_scored_byRefPosture = []
# for i_posture in range(len(original_posture_config)):
#     GA_data_posture_scored_byRefPosture_joint =[]
#     for i_angle in range(len(angle_limit)):
#         GA_data_posture_scored_byRefPosture_joint.append(cal_Posture_Score(GA_data_posture[i_posture][i_angle],original_posture_config[i_posture],score_weight))
#
#     GA_data_posture_scored_byRefPosture.append(GA_data_posture_scored_byRefPosture_joint)
#
# print 'GA_data_posture_scored_byRefPosture',len(GA_data_posture_scored_byRefPosture)
# print 'GA_data_posture_scored_byRefPosture[0]',len(GA_data_posture_scored_byRefPosture[0])
#
#
# ### sort data GA ###
# GA_data_posture_scored_byRefPosture_sorted = deepcopy(GA_data_posture_scored_byRefPosture)
# for i_posture in range(len(original_posture_config)):
#     for i_angle in range(len(angle_limit)):
#         GA_data_posture_scored_byRefPosture_sorted[i_posture][i_angle].sort(key=itemgetter(10))
#         saveDataToFile('.\\testdata\\GA_data_posture_scored_byRefPosture_sorted['+str(i_posture)+']['+str(i_angle)+'].txt',GA_data_posture_scored_byRefPosture_sorted[i_posture][i_angle])
# ###



