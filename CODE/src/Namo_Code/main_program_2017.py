from configobj import ConfigObj
import glob
import os
import numpy as np
from math import pow, sqrt, sin, cos, radians
from scipy.stats import norm
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn.utils import shuffle

import time
import pickle


def create_3dim_normalize_score_array(radius):

    normal_dis_array_size = radius + radius + 1
    normal_dis_sigma_width = 3

    array = np.zeros((normal_dis_array_size,normal_dis_array_size,normal_dis_array_size))
    for z in range(0,normal_dis_array_size):
        for y in range(0,normal_dis_array_size):
            for x in range(0, normal_dis_array_size):
                distance = sqrt(pow(x-radius,2) + pow(y-radius,2) + pow(z-radius,2))
                distance = distance*normal_dis_sigma_width/radius
                array[x, y, z] = round(norm.pdf(distance), 3)

    #print(array)
    return array

def create_4dim_normalize_score_array(radius):

    normal_dis_array_size = radius + radius + 1
    normal_dis_sigma_width = 3

    array = np.zeros((normal_dis_array_size,normal_dis_array_size,normal_dis_array_size,normal_dis_array_size))
    for z in range(0,normal_dis_array_size):
        for y in range(0,normal_dis_array_size):
            for x in range(0, normal_dis_array_size):
                for w in range(0, normal_dis_array_size):
                    distance = sqrt(pow(w-radius,2) + pow(x-radius,2) + pow(y-radius,2) + pow(z-radius,2))
                    distance = distance*normal_dis_sigma_width/radius
                    array[w, x, y, z] = round(norm.pdf(distance), 3)

    #print(array)
    return array

def add_value_to_index(n):
    array = []
    if n == 0:
        array.append(0)
    else:
        array.append(n-1)
        add_value_to_index(n-1)

    print("aaa=",array)

def create_ndim_normalize_score_array(radius, ndim):

    normal_dis_array_size = radius + radius + 1
    normal_dis_sigma_width = 3

    array_dim = []
    for i in range(ndim):
        array_dim.append(normal_dis_array_size)
    print("array_dim=",array_dim)
    sphere_array = np.zeros(array_dim)
    print(sphere_array)
    # sphere_array[0, 0, 0, 0, 0, 0] = 1
    #
    # print("value",sphere_array[0,0,0,0,0,0])

    index = []

    for dim in range(ndim):
        sub_index = []
        n = normal_dis_array_size

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

def collect_cartesian_position_data(kinematics_dataSet, position_index):

    cartesian_dataSet = []
    #print("len=",len(kinematics_data_set))
    for kinematics_data in kinematics_dataSet:
         cartesian_dataSet.append([round(kinematics_data[position_index][0][3],0), round(kinematics_data[position_index][1][3],0), round(kinematics_data[position_index][2][3],0)])
    #print("len=", len(cartesian_dataSet))
    #print(cartesian_dataSet)

    return cartesian_dataSet

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

def collect_quaternion_data(kinematics_dataSet):
    quaternion_dataSet = []

    for i, kinetics in enumerate(kinematics_dataSet):
        quaternion_dataSet.append(cal_quaternion(kinetics[7]))

    return quaternion_dataSet

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

def find_avg_joint_angle(all_posture_stat_list, weight_type):
    posture_amount = len(all_posture_stat_list)
    joint_amount = len(all_posture_stat_list[0][0])

    all_posture_mean = []

    for i in range(posture_amount):
        all_posture_mean.append(all_posture_stat_list[i][0])


    #print("all_posture_mean=",all_posture_mean)

    if weight_type == 'std':
        all_joint_std = []
        all_joint_std_inv = []
        all_joint_weight = []

        for joint_num in range(joint_amount):
            joint_std = []
            joint_std_inv = []

            #print("joint_num=",joint_num)
            for posture_num in range(posture_amount):
                joint_std.append(all_posture_stat_list[posture_num][1][joint_num])
                joint_std_inv.append(1/all_posture_stat_list[posture_num][1][joint_num])

            all_joint_std.append(joint_std)

            all_joint_std_inv.append(joint_std_inv)
            all_joint_weight.append([float(i)/sum(joint_std_inv) for i in joint_std_inv])

        # print("all_joint_std=",all_joint_std)
        # print("all_joint_std_inv=", all_joint_std_inv)
        # print("all_joint_weight=", all_joint_weight)
        #
        # print("transpose_mean", np.transpose(all_posture_mean))

        all_posture_mean_T = np.transpose(all_posture_mean)

        joint_avg = []
        for joint_num in range(joint_amount):
            joint_avg.append(float(round(np.average(all_posture_mean_T[joint_num], weights=all_joint_weight[joint_num]),1)))

    elif weight_type == 'equl':
        #print("all_posture_mean=", all_posture_mean)
        joint_avg = np.round(np.mean(all_posture_mean, axis = 0),2)


    return joint_avg

def add_score(main_score_array, score_array, index_to_add_score_set, offset_index):
    accumulate_score_array = np.copy(main_score_array)
    print("accumulate_score_array_shape",np.shape(accumulate_score_array))

    print("score_array_shape", np.shape(score_array))
    lower_bound = int((np.shape(score_array)[0] - 1)/2)
    upper_bound = int((np.shape(score_array)[0] + 1) / 2)

    print("lower_bound",lower_bound)
    print("upper_bound", upper_bound)


    for index in index_to_add_score_set:
        index_after_offset = index - offset_index
        #print(index, offset_index, index_after_offset)
        accumulate_score_array[int((index_after_offset[0] - lower_bound)):int((index_after_offset[0] + upper_bound)),
                                int((index_after_offset[1] - lower_bound)):int((index_after_offset[1] + upper_bound)),
                                int((index_after_offset[2] - lower_bound)):int((index_after_offset[2] + upper_bound))] += score_array

    #print(accumulate_score_array)
    return accumulate_score_array



##################################################################################################
if __name__ == "__main__":

    workspace_radius = round((182 + 206.5 + 206 + 130),0)
    workspace_radius = 725
    workspace_diameter = workspace_radius*2
    print("workspace_diameter",workspace_diameter)

    #bye_elbow_score_workspace = np.zeros([1300, 1300, 1300])
    #print(bye_elbow_score_workspace)



    base_score_3dim = create_3dim_normalize_score_array(3) ### @param(sphere_radius)
    base_score_4dim = create_4dim_normalize_score_array(3)  ### @param(sphere_radius)


    ### load data ###
    jointAngle_degree_bye_set = collect_data('bye') ### @param(postureName)
    jointAngle_degree_salute_set = collect_data('salute')  ### @param(postureName)
    jointAngle_degree_sinvite_set = collect_data('side_invite')  ### @param(postureName)
    jointAngle_degree_wai_set = collect_data('wai')  ### @param(postureName)

    ### extract right arm data ###
    right_side_bye_set = extract_arm_data( jointAngle_degree_bye_set,'right')
    right_side_salute_set = extract_arm_data(jointAngle_degree_salute_set, 'right')
    right_side_sinvite_set = extract_arm_data(jointAngle_degree_sinvite_set, 'right')
    right_side_wai_set = extract_arm_data(jointAngle_degree_wai_set, 'right')

    ### calculate each posture stat ###
    right_side_bye_stat = calculate_stat_all_joint(right_side_bye_set)
    right_side_salute_stat = calculate_stat_all_joint(right_side_salute_set)
    right_side_sinvite_stat = calculate_stat_all_joint(right_side_sinvite_set)
    right_side_wai_stat = calculate_stat_all_joint(right_side_wai_set)

    ### calculate average join angle from all posture ###
    all_posture_stat_list = [right_side_bye_stat, right_side_salute_stat, right_side_sinvite_stat, right_side_wai_stat]
    ### type :: 'std' = standard_deviation, 'equl' = all weight equal
    avg_joint_angle_std = find_avg_joint_angle(all_posture_stat_list, 'std')
    avg_joint_angle_equl = find_avg_joint_angle(all_posture_stat_list, 'equl')

    print("avg M:std", avg_joint_angle_std)
    print("avg M:equl", avg_joint_angle_equl)

    ### calculate kinematics ###
    bye_kinematics_set = collect_kinematics_data(right_side_bye_set)
    salute_kinematics_set = collect_kinematics_data(right_side_salute_set)
    sinvite_kinematics_set = collect_kinematics_data(right_side_sinvite_set)
    wai_kinematics_set = collect_kinematics_data(right_side_wai_set)

    ##### bye posture #####
    ### collect bye catesian position and quaternion ###
    bye_elbow_position = np.asarray(collect_cartesian_position_data(bye_kinematics_set, 3))  ### 3 = elbow position
    bye_wrist_position = np.asarray(collect_cartesian_position_data(bye_kinematics_set, 4))  ### 4 = wrist position
    bye_quaternion = np.asarray(collect_quaternion_data(bye_kinematics_set))
    bye_quaternion_mean = np.mean(bye_quaternion,axis=0)
    print("quaternion=",bye_quaternion)
    print("mean=", bye_quaternion_mean)

    min_elbow = np.min(bye_elbow_position, axis=0)
    max_elbow = np.max(bye_elbow_position, axis=0)
    diff_elbow = max_elbow - min_elbow
    add_boundary = 20
    index_offset_elbow = [int(min_elbow[0]-(add_boundary/2)), int(min_elbow[1]-(add_boundary/2)), int(min_elbow[2]-(add_boundary/2))]

    print("min", min_elbow)
    print("max", max_elbow)
    print(diff_elbow)
    print("index_offset_elbow", index_offset_elbow)

    elbow_score_array = np.zeros([int(diff_elbow[0] + add_boundary), int(diff_elbow[1] + add_boundary), int(diff_elbow[2] + add_boundary)])

    elbow_score_array = np.copy(add_score(elbow_score_array, base_score_3dim, bye_elbow_position, index_offset_elbow))
    elbow_score_array_shape = np.shape(elbow_score_array)

    #############
    min_wrist = np.min(bye_wrist_position, axis=0)
    max_wrist = np.max(bye_wrist_position, axis=0)
    diff_wrist = max_wrist - min_wrist
    add_boundary = 20
    index_offset_wrist = [int(min_wrist[0] - (add_boundary / 2)), int(min_wrist[1] - (add_boundary / 2)),
                          int(min_wrist[2] - (add_boundary / 2))]

    print("min", min_wrist)
    print("max", max_wrist)
    print(diff_wrist)
    print("index_offset_wrist", index_offset_wrist)

    wrist_score_array = np.zeros(
        [int(diff_wrist[0] + add_boundary), int(diff_wrist[1] + add_boundary), int(diff_wrist[2] + add_boundary)])

    wrist_score_array = np.copy(add_score(wrist_score_array, base_score_3dim, bye_wrist_position, index_offset_wrist))
    wrist_score_array_shape = np.shape(wrist_score_array)

    ####################################################################################################################
    posture_score_array = np.copy(elbow_score_array)
    posture_score_array_shape = np.shape(posture_score_array)
    posture_index_offset = np.copy(index_offset_elbow)
    posture_name = str(elbow_score_array)

    data = []
    ### convert to data ###
    for z in range(posture_score_array_shape[0]):
        for y in range(posture_score_array_shape[1]):
            for x in range(posture_score_array_shape[2]):
                if posture_score_array[z][y][x] != 0:
                    if (z + posture_index_offset[0]) == 121 and (y + posture_index_offset[1]) == -178:
                        print([(z + posture_index_offset[0]), (y + posture_index_offset[1]), (x + posture_index_offset[2]), posture_score_array[z][y][x]])
                    data.append([(z + posture_index_offset[0]), (y + posture_index_offset[1]), (x + posture_index_offset[2]), posture_score_array[z][y][x]])
    #print(data, len(data))
    data = np.asarray(data)
    X, y = data[:,:-1], data[:,-1]

    print(X[0])
    print(y[0])

    num_training = int(0.8 * len(X))
    X_train, y_train = X[:num_training], y[:num_training]
    X_test, y_test = X[num_training:], y[num_training:]

    # print("time start")
    # print(time.time())
    # print(time.ctime())
    #
    # # Create Support Vector Regression model
    # sv_regressor = SVR(kernel='linear', C=1.0, epsilon=0.1)
    # # Train Support Vector Regressor
    # sv_regressor.fit(X_train, y_train)
    #
    # print("time stop")
    # print(time.time())
    # print(time.ctime())
    #
    # # Evaluate performance of Support Vector Regressor
    # y_test_pred = sv_regressor.predict(X_test)
    # mse = mean_squared_error(y_test, y_test_pred)
    # evs = explained_variance_score(y_test, y_test_pred)
    # print("\n#### Performance ####")
    # print("Mean squared error =", round(mse, 2))
    # print("Explained variance score =", round(evs, 2))
    #
    # # Evaluate performance of Support Vector Regressor
    # y_test_pred = sv_regressor.predict(X_test)
    # mse = mean_squared_error(y_test, y_test_pred)
    # evs = explained_variance_score(y_test, y_test_pred)
    # print("\n#### Performance ####")
    # print("Mean squared error =", round(mse, 2))
    # print("Explained variance score =", round(evs, 2))
    #
    # # Test the regressor on test datapoint
    # test_data = [121, -178, -167]
    # print("\nPredicted price:", sv_regressor.predict([test_data])[0])
    #
    # print("time stop")
    # print(time.time())
    # print(time.ctime())
    # filename = posture_name
    # pickle.dump(sv_regressor,open(filename, 'wb'))







