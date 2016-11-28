from utility_function import*
from configobj import ConfigObj
import math
import numpy
import copy
import csv

## postures ##
respect_posture_config = [80, -45, -10, 135, 45, 0, 0, 85, -207, 131, 'close']
wai_posture_config = [25, -5, -45, 100, 0, -40, 45, 207, -54, -105, 'close']
bye_posture_config = [25, -20, 0, 110, -90, -50, -15, 229, -229, -34, 'open']
rightInvite_posture_config = [10, -10, 45, 60, 45, 0, 0, 218, -102, -96, 'close']


original_postures_config = []
original_postures_config.append(respect_posture_config)
original_postures_config.append(wai_posture_config)
original_postures_config.append(bye_posture_config)
original_postures_config.append(rightInvite_posture_config)


avg_angle = cal_Avg_Angle(original_postures_config, 7)


score_weight = [1, 0.001, 0.001]

joint_fixed = 6
joint_fixed_value = avg_angle[joint_fixed]
joint_fixed_value_right_arm = [-44.3, 13.7, -8.4, -95.7, -6.3, 13.2, -19.3, 2.5]

joint_angle_limit = [[0,135],[-90,0],[-45,45],[0,135],[-90,90],[-50,45],[-45,45]]
joint_angle_limit_right_arm = [[-135,45],[-20,90],[-90,90],[-135,0],[-115,90],[-45,45],[-15,15]]

## motor value ##
motor_left_arm_center = [527, 3285, 2344, 1760, 2370, 2276, 1793]
motor_right_arm_center = [3534, 820, 2511, 2271, 2320, 1914, 1809]
moto_head_center = [579, 485, 376]





def load_posture_namo_right_arm():
    posture_list = ["Salute", "Wai", "Bye", "SideInvite"]
    num_of_posture = 10

    postures_pack = []


    for index, posture in enumerate(posture_list):

        for i in range(num_of_posture):

            config = ConfigObj('./Postures/'+ posture + str(i+1))
            #print './Postures/' + posture + str(i+1)
            data = map(int, config['Keyframe_Value']['Keyframe_' + str(2)][7:14])
            data.append(index+1)
            postures_pack.append(data)

    return postures_pack

def convert_motor_to_degree_namo_right_arm(data,center):
    data[0][0] = 1517
    for j in range(len(data)):
        for i in range(len(center)):
            data[j][i] = data[j][i] - center[i]
            data[j][i] = int(round(data[j][i] * 360.0 / 4095.0, 0))
            if i == 0:
                data[j][i] = data[j][i]/2
    #print data
    return data

def find_max_min_avg(data):
    newdata = map(list, zip(*data))
    #print len(newdata)
    max_value = []
    min_value = []
    avg_value = []
    for i in range(len(newdata)):
        #print newdata[i]
        max_value.append(max(newdata[i]))
        min_value.append(min(newdata[i]))
        avg_value.append(round(numpy.mean(newdata[i]),1))

    data_min_max_set = []
    for i in range(len(max_value)):
        data_min_max = []
        data_min_max.append(min_value[i])
        data_min_max.append(max_value[i])

        data_min_max_set.append(data_min_max)



    print data_min_max_set
    print avg_value

def save_CSV_file(filename,data):
    myfile = open(filename, 'wb')
    wr = csv.writer(myfile, dialect='excel')
    wr.writerows(data)

if __name__ == "__main__":
    pack = load_posture_namo_right_arm()
    data = convert_motor_to_degree_namo_right_arm(pack, motor_right_arm_center)
    save_CSV_file("./Postures/posture_test.csv", data)
    #find_max_min_avg(data)