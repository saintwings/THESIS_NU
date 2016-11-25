from utility_function import*

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

joint_angle_limit = [[0,135],[-90,0],[-45,45],[0,135],[-90,90],[-50,45],[-45,45]]