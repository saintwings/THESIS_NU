import random
import math    # cos() for Rastrigin
import copy    # array-copying convenience
import sys     # max float
### local import ###
from utility_function import*



# def error(vector, ref_pose, score_weight):
#   err = 0.0
#   pos_set = []
#   posture = []
#   print("len position = "+str(len(position)))
#   for i in range(len(position)):
#     xi = position[i]
#     posture.append(int(position[i]))
#     #err += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10
#
#   #print("posture ="+str(posture))
#   #print("ref_posture ="+str(ref_pose))
#   pos_set.append(posture)
#   score = cal_Posture_Score(pos_set,ref_pose,score_weight)
#   print("score = "+str(score))
#   print(str(score[0][10]))
#   err = score[0][10]
#   return err

def objective_function(vector):
    pass

def attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep):
    pass

class Bacteria:
    def __init__(self, problem_size, search_space, seed, joint_fixed, joint_fixed_value):
        self.rnd = random.Random(seed)
        self.vector = [0.0 for i in range(problem_size)]
        self.cost = [0.0 for i in range(problem_size)]
        self.inter = [0.0 for i in range(problem_size)]
        self.fitness = [0.0 for i in range(problem_size)]
        self.sum_nutrients = [0.0 for i in range(problem_size)]

        for i in range(problem_size):
            if i == joint_fixed:
                self.vector[i] = joint_fixed_value
            else:
                self.vector[i] = random.randint(search_space[i][0], search_space[i][1])

        print self.vector




def Search(original_posture_config, joint_fixed, joint_fixed_value,
            problem_size, search_space, pop_size_S,
            elim_disp_steps_Ned, repro_steps_Nre, chem_steps_Nc, swim_length_Ns, step_size_Ci, p_eliminate_Ped,
            d_attr, w_attr, h_rep, w_rep):

    rnd = random.Random(0)

    # create n random particles
    random_cells = [Bacteria(problem_size, search_space, rnd, joint_fixed, joint_fixed_value) for i in range(pop_size_S)]
    best_set = []
    for posture_count in range(len(original_posture_config)):
        print("posture count ="+str(posture_count)+"value="+str(original_posture_config[posture_count]))
        cells = copy.copy(random_cells)
        best = []
        for l in range(0, elim_disp_steps_Ned):
            for k in range(0, repro_steps_Nre):
                print("l = " + str(l) + " k = " + str(k))
                c_best, cells = ChemotaxisAndSwim(original_posture_config[posture_count], joint_fixed, cells, search_space, chem_steps_Nc,
                                           swim_length_Ns, step_size_Ci, d_attr, w_attr, h_rep, w_rep)





def evaluate(ref_posture_config, score_weight, cell, cells, d_attr, w_attr, h_rep, w_rep):
  cell.cost = objective_function(ref_posture_config, score_weight,cell.vector)
  #cell.inter = attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep)
  #cell.fitness = cell.cost + cell.inter

def ChemotaxisAndSwim(ref_posture_config, joint_fixed, cells, search_space, chem_steps_Nc, score_weight,
                                           swim_length_Ns, step_size_Ci, d_attr, w_attr, h_rep, w_rep):
    best = []
    for j in range(0, chem_steps_Nc):
        print(" j = " + str(j))
        move_cells = []

        for i, cell in enumerate(cells):
            sum_nutrients = 0
            evaluate(ref_posture_config, score_weight, cell, cells, d_attr, w_attr, h_rep, w_rep)

            print("cell="+str(cell))
            print("i ="+str(i))

    return best, cells






if __name__ == "__main__":
    ### add postures ###
    ## original posture ##
    wai_posture_config = [25, -5, -45, 100, 0, -40, 45, 207, -54, -105, 'close']
    respect_posture_config = [80, -45, -10, 135, 45, 0, 0, 85, -207, 131, 'close']
    bye_posture_config = [25, -20, 0, 110, -90, -50, -15, 229, -229, -34, 'open']
    rightInvite_posture_config = [10, -10, 45, 60, 45, 0, 0, 218, -102, -96, 'close']

    original_posture_config = []
    original_posture_config.append(wai_posture_config)
    original_posture_config.append(respect_posture_config)
    original_posture_config.append(bye_posture_config)
    original_posture_config.append(rightInvite_posture_config)
    print("aaaaaaa")


    avg_angle = cal_Avg_Angle(original_posture_config, 7)

    score_weight = [1, 0.001, 0.001]

    joint_fixed = 5
    joint_fixed_value = avg_angle[joint_fixed]

    #initial
    #problem configuration
    problem_size = 7 #Dimension of the search space
    search_space = [[0,135],[-90,0],[-45,45],[0,135],[-90,90],[-50,45],[-45,45]]

    pop_size_S = 50 #Total number of bacteria in the population
    chem_steps_Nc = 100 #The number of chemo tactic steps
    swim_length_Ns = 4  #The swimming length
    repro_steps_Nre = 4 #Number of reproduction steps
    elim_disp_steps_Ned = 2 #Number of elimination-dispersal event
    p_eliminate_Ped = 0.25 #Elimination-dispersal probability
    step_size_Ci = 1 #The size of the step taken in the random direction specified by the tumble

    d_attr = 0.1 #attraction coefficient
    w_attr = 0.2 #attraction coefficient
    h_rep = d_attr #repulsion coefficient
    w_rep = 10 #repulsion coefficient

    Search(original_posture_config, joint_fixed, joint_fixed_value,score_weight,
            problem_size, search_space, pop_size_S,
            elim_disp_steps_Ned, repro_steps_Nre, chem_steps_Nc, swim_length_Ns, step_size_Ci, p_eliminate_Ped,
            d_attr, w_attr, h_rep, w_rep)

#########
