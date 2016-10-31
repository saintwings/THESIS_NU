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

score_weight = [1,0.001,0.001]
loop_amount = 10000;
scene.title = "Namo Robot >> Right Side"
scene.height = scene.width = 800

f_armLength = [700,182,206.5,206,130,0.0,65.0]

## original posture ##
wai_posture_config = [25,-5,-45,100,0,-40,45,207,-54,-105,'close']
respect_posture_config = [80,-45,-10,135,45,0,0,85,-207,131,'close']
bye_posture_config = [25,-20,0,110,-90,-50,-15,229,-229,-34,'open']
rightInvite_posture_config = [10,-10,45,60,45,0,0,218,-102,-96,'close']

original_posture_config = []
original_posture_config.append(wai_posture_config)
original_posture_config.append(respect_posture_config)
original_posture_config.append(bye_posture_config)
original_posture_config.append(rightInvite_posture_config)

target_posture0 = respect_posture_config
target_posture1 = [69.2, -45.4, -7.68, 125.83, 47.23, 5.55, 13.23]



def drawArm(target_posture,colorDraw0,colorDraw1):
    #def drawArm(colorDraw,posture):
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
                   #color=color.green)
                   color=colorDraw0)

    main_sphere = sphere(frame=frame0,
                   pos=(0,0,0),
                   radius=30,
                   #color=color.green)
                   color=colorDraw0)

    right_shoulder_sphere = sphere(frame=frame1_R,
                   pos=(0,0,0),
                   radius=25,
                   #color=color.green)
                   color=colorDraw0)

    right_shoulder_axis = cylinder(frame=frame0,
                   pos=(0,0,0),
                   axis=(-f_armLength[1],0,0),
                   radius=20,
                   #color=color.green)
                   color=colorDraw0)
    right_upper_arm_axis = cylinder(frame=frame3_R,
                   pos=(0,0,0),
                   axis=(0,-f_armLength[2],0),
                   radius=20,
                   #color=color.green)
                   color=colorDraw0)
    right_elbow_sphere = sphere(frame=frame4_R,
                   pos=(0,0,0),
                   radius=25,
                   #color=color.green)
                   color=colorDraw0)
    right_lower_arm_axis = cylinder(frame=frame4_R,
                   pos=(0,0,0),
                   axis=(0,-f_armLength[3],0),
                   radius=20,
                   #color=color.green)
                   color=colorDraw0)
    right_wrist_sphere = sphere(frame=frame5_R,
                   pos=(0,0,0),
                   radius=25,
                   #color=color.green)
                   color=colorDraw0)
    right_hand_axis = cylinder(frame=frame7_R,
                   pos=(0,0,0),
                   axis=(0,-f_armLength[4],0),
                   radius=10,
                   #color=color.green)
                   color=colorDraw0)
    right_hand_sphere = sphere(frame=frame7_R,
                   pos=(20,-f_armLength[4]/2,0),
                   radius=10,
                   #color=color.green)
                   color=colorDraw0)
    right_hand_box = box(frame = frame7_R,
                    pos =(10,-f_armLength[4]/2,0),
                    length = 10,
                    height = 100,
                    width = 30,
                    #color=color.green)
                    color=colorDraw1)
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

#scene.autoscale = 0

############################################################################################################################
#drawArm(wai_posture_config,color.red,color.green)
#drawArm([32, -10, -28, 87, 12, -17, 44],color.blue,color.red) #fix a1
#drawArm([35, -10, -28, 87, 12, -17, 44],color.blue,color.green) #fix a1
#([24.68, -0.42, -38.19, 105.16, -23.98, -22.34, 35.64],color.green,color.yellow)
#drawArm([31.35, -12.2, -30.83, 116.61, 4.7, -20.76, 32.83],color.blue,color.red) #fix a1
#drawArm([25.05, -24.53, 6.25, 134.04, 25.97, -16.12, 8.43],color.blue,color.red) #fix a2
#drawArm([27.03, -11.75, -38.79, 123.87, -7.62, -42.96, 9.74],color.blue,color.red) #fix a3
#drawArm([35.92, -14.0, -43.11, 125.01, -1.73, -40.54, 5.06],color.blue,color.red) #fix a4
#drawArm([3.05, -1.64, -28.97, 133.49, -18.4, -6.95, 25.21],color.blue,color.red) #fix a5
#drawArm([30.08, -12.6, -41.94, 122.36, -7.82, -41.27, 17.38],color.blue,color.red) #fix a6
#drawArm([18.22, -9.44, -44.25, 120.11, -1.84, -42.34, 28.84],color.blue,color.red) #fix a7

############################################################################################################################
#drawArm(respect_posture_config,color.red,color.green)
#drawArm([69.2, -45.4, -7.68, 125.83, 47.23, 5.55, 13.23],color.green,color.yellow)
#drawArm([31.36, -72.23, 21.15, 132.38, 55.7, 6.67, 35.35],color.blue,color.red)#fix a1
#drawArm([71.29, -24.54, -19.16, 130.14, 15.49, 2.88, 8.01],color.blue,color.red)#fix a2
#drawArm([91.28, -72.96, -38.79, 134.22, 52.12, -15.59, 30.41],color.blue,color.red) #fix a3
#drawArm([82.04, -47.54, -34.58, 125.01, 23.26, -9.77, 17.63],color.blue,color.red) #fix a4
#drawArm([51.37, -25.44, -37.63, 134.06, -18.4, -0.25, 13.62],color.blue,color.red) #fix a5
#drawArm([95.87, -52.88, -42.66, 131.22, 33.48, -41.27, 27.67],color.blue,color.red) #fix a6
#drawArm([64.8, -42.53, 0.16, 112.14, 31.39, 25.12, 28.84],color.blue,color.red) #fix a7
#
############################################################################################################################
#drawArm(bye_posture_config,color.red,color.green)
#drawArm([40.11, -5.89, 4.73, 107.63, -85.56, -39.04, 13.66],color.green,color.yellow)
#drawArm([31.38, -17.19, 20.28, 102.19, -63.04, -41.46, 19.72],color.blue,color.red)#fix a1
#drawArm([40.86, -24.53, -15.59, 117.65, -84.29, -26.77, -18.24],color.blue,color.red)#fix a2
#drawArm([72.43, -19.19, -38.79, 80.53, -87.16, -38.76, -38.85],color.blue,color.red) #fix a3
#drawArm([16.29, -26.25, 14.15, 125.01, -86.42, -44.1, -12.23],color.blue,color.red) #fix a4
#drawArm([20.93, -46.83, 30.2, 107.48, -18.4, -38.36, 21.03],color.blue,color.red) #fix a5
#drawArm([43.07, -12.15, 23.22, 106.46, -68.18, -41.27, 20.66],color.blue,color.red) #fix a6
#drawArm([21.56, -19.37, 11.72, 115.22, -51.13, -42.59, 28.84],color.blue,color.red) #fix a7
#
############################################################################################################################
#drawArm(handOverHeart_posture_config,color.red,color.green)
#drawArm([32.41, -23.69, -25.71, 117.9, 12.97, 12.2, -10.78],color.green,color.yellow)
#drawArm([31.35, -21.02, -44.04, 92.3, 7.63, 2.65, 8.7],color.blue,color.red)#fix a1
#drawArm([38.2, -24.54, -41.76, 96.86, 6.69, 1.05, 13.33],color.blue,color.red)#fix a2
#drawArm([34.02, -13.3, -38.79, 133.25, 2.4, 9.72, -35.55],color.blue,color.red) #fix a3
#drawArm([27.31, -20.15, -13.23, 125.01, 15.05, 20.57, -20.32],color.blue,color.red) #fix a4
#drawArm([1.43, -11.02, -32.26, 115.71, -18.4, 18.24, 2.67],color.blue,color.red) #fix a5
#drawArm([26.62, -28.07, -44.9, 103.72, -14.83, -41.27, -22.34],color.blue,color.red) #fix a6
#drawArm([21.79, -16.56, -3.94, 88.62, -19.52, 36.84, 28.84],color.blue,color.red) #fix a7

#drawArm(rightInvite_posture_config,color.red,color.green)


drawArm(wai_posture_config,color.red,color.green)
drawArm([25,-3,-45,120,-14,-34,11],color.green,color.yellow)
drawArm([23,-7,-42,119,-12,-33,7.5],color.blue,color.yellow)

