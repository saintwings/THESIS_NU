from configobj import ConfigObj
import glob
import os
import numpy as np
from math import pow, sqrt, sin, cos, radians
from scipy.stats import norm

def create_sphere_normaldis_score_array(sphere_radius):

    normal_dis_array_size = sphere_radius + sphere_radius + 1
    normal_dis_sigma_width = 3

    sphere_array = np.zeros((normal_dis_array_size,normal_dis_array_size,normal_dis_array_size))
    for z in range(0,normal_dis_array_size):
        for y in range(0,normal_dis_array_size):
            for x in range(0, normal_dis_array_size):
                distance = sqrt(pow(x-sphere_radius,2) + pow(y-sphere_radius,2) + pow(z-sphere_radius,2))
                distance = distance*normal_dis_sigma_width/sphere_radius
                sphere_array[x, y, z] = round(norm.pdf(distance), 3)

    print(sphere_array)
    return sphere_array

def convert_motorValue_to_cartesianSpace(posture_dataSet):
    int_motorDirection_and_ratio = [0.5, -1, 1, 1, 1, -1, 1,-0.5, -1, 1, -1, 1, -1, -1, 1, -1, 1]

    ### read motor center value ###
    file_center = open('./Postures/motor_center.txt', 'r')
    int_motorCenterValue = file_center.read()
    file_center.close()
    int_motorCenterValue = int_motorCenterValue.split('\n')
    for x in range(17):
        int_motorCenterValue[x] = int(int_motorCenterValue[x])

    ### cal diff ###
    diff_set = []
    for i, item in enumerate(posture_dataSet):
        diff = []
        for j,value in enumerate(item):
            diff.append((value - int_motorCenterValue[j])*int_motorDirection_and_ratio[j])

        diff_set.append(diff)

    #print("diff_set=",diff_set)

    ### convert to degree ###
    motorDegree_set = []
    for i, item in enumerate(diff_set):
        motorDegree = []
        for j, value in enumerate(item):
            motorDegree.append(round(value * 359 / 4095.0,0))

        motorDegree_set.append(motorDegree)

    #print("motor_degree=", motorDegree_set)

    return motorDegree_set

def calculate_stat_all_joint(posture_dataSet):

    mean = np.mean(posture_dataSet, axis = 0)
    std = np.std(posture_dataSet, axis = 0)
    var = np.var(posture_dataSet, axis = 0)

    return [mean, std, var]

def collect_data(postureName):

    posture_dataset = []
    path = './Postures/posture_set_' + str(postureName)
    for i, filename in enumerate(glob.glob(os.path.join(path, '*.ini'))):
        config = ConfigObj(filename)
        main_index = [index for index, x in enumerate(config['Keyframe_Posture_Type']) if x == 'main']
        for index in main_index:
            posture_dataset.append(list(map(int, config['Keyframe_Value']['Keyframe_' + str(index)])))

    data_set = convert_motorValue_to_cartesianSpace(posture_dataset)
    return data_set

def extract_arm_data(posture_dataSet,armSide):

    if armSide == 'right':
        index_range = [7, 14]
    elif armSide == 'left':
        index_range = [0, 7]
    else:
        index_range = [14, 17]
    data_set = np.asarray(posture_dataSet)

    new_data_set = data_set[:,index_range[0]:index_range[1]]

    return new_data_set

def collect_kinematics_data(joint7dof_dataSet):
    kinematics_dataSet = []

    for i, jointSet in enumerate(joint7dof_dataSet):
        kinematics_dataSet.append(cal_kinematics_namo_numpy(jointSet,'right'))

    return kinematics_dataSet

def cal_kinematics_namo_numpy(degree7Joint,armSide):
    """ calculate Namo robot kinematic 7DOF Arm
    :param degree7Joint: input [degree0,1,2,3,4,5,6]
    :param armSide: input arm side 'L' for Left side, 'R' for Right side
    :return: Transformation Matrix List [T01,T02,T03,T04,T05,T06,T07,T0E]
    """
    ## DH parameter >> alpha[0,1,...6,end effector]
    alpha = [radians(90),radians(90),radians(-90),radians(-90),radians(90),radians(90),
             radians(-90),radians(0)]
    ## DH parameter >> a[0,1,...6,end effector]
    a = [0,0,0,0,0,0,0,-140]
    ## DH parameter >> d[1,2,...7,end effector]
    d = [182,0,206.5,0,206,0,0,0]
    if armSide == 'left':
        d[0] = d[0]*(-1)
    elif armSide == 'right':
        d[0] = d[0]*1
    #print("7dof ="+str(degree7Joint))
    ## DH parameter >> theta[1,2,...7,end effector]
    theta = [radians(degree7Joint[0] + 90),radians(degree7Joint[1] + 90),radians(degree7Joint[2] - 90),
             radians(degree7Joint[3]),radians(degree7Joint[4] + 90),radians(degree7Joint[5] - 90),
             radians(degree7Joint[6]),radians(0)]
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

def cal_quaternion(Tmatrix):
    #print Tmatrix
    tr = Tmatrix[0,0] + Tmatrix[1,1] + Tmatrix[2,2]
    if(tr>0):
        S = sqrt(tr+1.0)*2 ## S=4*qw
        qw = 0.25*S
        qx = (Tmatrix[2,1]-Tmatrix[1,2])/S
        qy = (Tmatrix[0,2]-Tmatrix[2,0])/S
        qz = (Tmatrix[1,0]-Tmatrix[0,1])/S
        #print "case1"
    elif((Tmatrix[0,0]>Tmatrix[1,1]) and (Tmatrix[0,0]>Tmatrix[2,2])):
        S = sqrt(1.0 + Tmatrix[0,0] - Tmatrix[1,1] - Tmatrix[2,2])*2 ## S=4*qx
        qw = (Tmatrix[2,1]-Tmatrix[1,2])/S
        qx = 0.25*S
        qy = (Tmatrix[0,1]+Tmatrix[1,0])/S
        qz = (Tmatrix[0,2]+Tmatrix[2,0])/S
        #print "case2"
    elif(Tmatrix[1,1]>Tmatrix[2,2]):
        S = sqrt(1.0 + Tmatrix[1,1] - Tmatrix[0,0] - Tmatrix[2,2])*2 ## S=4*qy
        qw = (Tmatrix[0,2]-Tmatrix[2,0])/S
        qx = (Tmatrix[0,1]+Tmatrix[1,0])/S
        qy = 0.25*S
        qz = (Tmatrix[1,2]+Tmatrix[2,1])/S
        #print "case3"
    else:
        S = sqrt(1.0 + Tmatrix[2,2] - Tmatrix[0,0] - Tmatrix[1,1])*2 ## S=4*qz
        qw = (Tmatrix[1,0]-Tmatrix[0,1])/S
        qx = (Tmatrix[0,2]+Tmatrix[2,0])/S
        qy = (Tmatrix[1,2]+Tmatrix[2,1])/S
        qz = 0.25*S
        #print "case4"

    norm = sqrt((qw*qw) + (qx*qx) + (qy*qy) + (qz*qz))
    return [qw,qx,qy,qz,norm]


if __name__ == "__main__":

    #create_sphere_normaldis_score_array(3) ### @param(sphere_radius)

    jointAngle_degree_bye_set = collect_data('bye') ### @param(postureName)
    jointAngle_degree_salute_set = collect_data('salute')  ### @param(postureName)
    jointAngle_degree_sinvite_set = collect_data('side_invite')  ### @param(postureName)
    jointAngle_degree_wai_set = collect_data('wai')  ### @param(postureName)

    print("bye",jointAngle_degree_bye_set)
    print("salute", jointAngle_degree_salute_set)
    print("sinvite", jointAngle_degree_sinvite_set)
    print("wai", jointAngle_degree_wai_set)

    right_side_bye_set = extract_arm_data( jointAngle_degree_bye_set,'right')
    right_side_salute_set = extract_arm_data(jointAngle_degree_salute_set, 'right')
    right_side_sinvite_set = extract_arm_data(jointAngle_degree_sinvite_set, 'right')
    right_side_wai_set = extract_arm_data(jointAngle_degree_wai_set, 'right')

    right_side_bye_stat = calculate_stat_all_joint(right_side_bye_set)
    right_side_salute_stat = calculate_stat_all_joint(right_side_salute_set)
    right_side_sinvite_stat = calculate_stat_all_joint(right_side_sinvite_set)
    right_side_wai_stat = calculate_stat_all_joint(right_side_wai_set)

    print('bye stat =', right_side_bye_stat[0])
    print('salute stat =', right_side_salute_stat[0])
    print('sinvite stat =', right_side_sinvite_stat[0])
    print('wai stat =', right_side_wai_stat[0])

    bye_kinematics_set = collect_kinematics_data(right_side_bye_stat)
    print(bye_kinematics_set[0][3])
    print(bye_kinematics_set[0][4])
    print(bye_kinematics_set[0][7])
    # right_side_all_set = np.concatenate((right_side_bye_set,right_side_salute_set,right_side_sinvite_set,right_side_wai_set), axis = 0)
    # print(right_side_all_set,len(right_side_all_set))