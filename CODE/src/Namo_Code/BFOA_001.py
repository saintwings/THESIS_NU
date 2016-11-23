import random
import math    # cos() for Rastrigin
import copy    # array-copying convenience
import sys     # max float
import time
### local import ###
from utility_function import*
from posture_files import*


class Bacteria:
    def __init__(self, problem_size, search_space, joint_fixed, joint_fixed_value, seed = 0,verbal = None):
        self.rnd = random.Random(seed)
        self.joint_fixed = joint_fixed
        self.joint_fixed_value = joint_fixed_value
        self.vector = [None for i in range(problem_size)]
        self.cost = None
        self.inter = None
        self.fitness = None
        self.sum_nutrients = None
        self.transformation_matrix = None
        self.quaternion = None
        self.T_matrix_cell = None
        self.Q_cell = None

        if verbal == 'r':
            ## random only ##
            for i in range(problem_size):
                self.vector[i] = random.randint(search_space[i][0], search_space[i][1])

            self.cal_T_matrix_cell('c')
            self.cal_Q_cell('c')
        elif verbal == 'rf':
            ## random and fix ##
            ## random only ##
            for i in range(problem_size):

                if i == joint_fixed:
                    self.vector[i] = joint_fixed_value
                else:
                    self.vector[i] = random.randint(search_space[i][0], search_space[i][1])

            self.cal_T_matrix_cell('c')
            self.cal_Q_cell('c')


    def fixed_vector_some_value(self):
        self.vector[self.joint_fixed] = self.joint_fixed_value

    def cal_T_matrix_cell(self, verbal = 'c'):
        if verbal == 'c':
            self.T_matrix_cell = calKinematicNamo(self.vector, 'R')

        elif verbal == 'cp':
            self.T_matrix_cell = calKinematicNamo(self.vector, 'R')
            print("T_matric_cell = " + str(self.T_matrix_cell))

        elif verbal == 'p':
            print("T_matric_cell = " + str(self.T_matrix_cell))


    def cal_Q_cell(self, verbal = 'c'):
        if verbal == 'c':
            self.Q_cell = calQuaternion(self.T_matrix_cell[7])

        elif verbal == 'cp':
            self.Q_cell = calQuaternion(self.T_matrix_cell[7])
            print("Q_cell = " + str(self.Q_cell))

        elif verbal == 'p':
            print("Q_cell = " + str(self.Q_cell))


def Search_New_Postures_by_BFOA(ref_postures, joint_fixed, joint_fixed_value,posture_weight,
            problem_size, search_space, pop_size_S,
            elim_disp_steps_Ned, repro_steps_Nre, chem_steps_Nc, swim_length_Ns, step_size_Ci, p_eliminate_Ped,
            d_attr, w_attr, h_rep, w_rep):

    rnd = random.Random(0)
    best_set = []

    ## create n random particles ##
    random_cells = [Bacteria(problem_size, search_space, joint_fixed, joint_fixed_value, rnd, 'rf') for i in range(pop_size_S)]
    ## print cells data ##
    # for cell in random_cells:
    #     print(cell.vector)
    #     print(cell.cal_T_matrix_cell('p'))
    #     print(cell.cal_Q_cell('p'))




    ## for each posture ##
    for posture_count in range(len(ref_postures)):
        print("posture count ="+str(posture_count)+" value="+str(ref_postures[posture_count]))

        cells = deepcopy(random_cells)
        best = Bacteria(problem_size, search_space, joint_fixed, joint_fixed_value, rnd, 'None')
        print("best cost =" + str(best.cost))
        time.sleep(10)

        ## cal reference cell posture value ##
        ref_cell = Bacteria(problem_size, search_space, joint_fixed, joint_fixed_value, rnd, 'None')
        ref_cell.vector = ref_postures(posture_count)
        ref_cell.cal_T_matrix_cell('cp')
        ref_cell.cal_Q_cell('cp')

        T_matrix_ref = calKinematicNamo(ref_postures[posture_count], 'R')
        Q_ref = calQuaternion(T_matrix_ref[7])
        print("T matrix ref =" + str(T_matrix_ref))
        print("Q ref =" + str(Q_ref))


        for l in range(0, elim_disp_steps_Ned):
            for k in range(0, repro_steps_Nre):
                print("l = " + str(l) + " k = " + str(k))
                c_best, cells = ChemotaxisAndSwim(T_matrix_ref, Q_ref, joint_fixed, joint_fixed_value, posture_weight, search_space,
                                                  cells, chem_steps_Nc,swim_length_Ns, step_size_Ci, d_attr, w_attr, h_rep, w_rep)

                if (best.cost == None) or (c_best.cost < best.cost):
                    best = c_best

                print("best fitness = " + str(best.fitness) + ", cost = " + str(best.cost))



def evaluate(T_matrix_ref, Q_ref, posture_weight, cell, cells, d_attr, w_attr, h_rep, w_rep):
    cell.cost = objective_function(T_matrix_ref, Q_ref, posture_weight,cell.vector)
    cell.inter = attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep)
    cell.fitness = cell.cost + cell.inter
    print("cost = " + str(cell.cost) + " inter" + str(cell.inter) + " fitness = " + str(cell.fitness))

def attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep):
    attract = compute_cell_interaction(cell, cells, -d_attr, -w_attr)
    repel = compute_cell_interaction(cell, cells, h_rep, -w_rep)
    return attract + repel

def compute_cell_interaction(cell, cells, d, w):
    sum = 0
    for other in cells:
        diff = 0

        for i in range(len(cell.vector)):
            diff += (cell.vector[i] - other.vector[i])**2

        sum += d * math.exp(w*diff)
        #print("sum = " + str(sum))

    return sum

def objective_function(T_matrix_ref, Q_ref, posture_weight,vector):

    ## cal posture value ##
    T_matrix = calKinematicNamo(vector, 'R')
    Q = calQuaternion(T_matrix[7])

    all_score = cal_Single_Posture_Score(T_matrix_ref, Q_ref, T_matrix, Q, score_weight)
    score = all_score[3]
    return score

def generate_random_direction(problem_size):
    random_vector = [random.uniform(-1,1) for i in range(problem_size)]

    #print("random_vector="+str(random_vector))

    return random_vector

def tumble_cell(joint_fixed, joint_fixed_value, search_space, cell, step_size_Ci):
    new_tumble_cell = Bacteria(len(search_space), search_space, joint_fixed, joint_fixed_value)

    step = generate_random_direction(len(search_space))
    vector = [None for i in range(len(search_space))]

    for i in range(len(vector)):
        vector[i] = cell.vector[i] + step_size_Ci * step[i]
        vector[i] = round(vector[i],0)
        if vector[i] < search_space[i][0]: vector[i] = search_space[i][0]
        if vector[i] > search_space[i][1]: vector[i] = search_space[i][1]

    ## set lock joint ##
    vector[joint_fixed] = joint_fixed_value

    new_tumble_cell.vector = vector

    return new_tumble_cell


def ChemotaxisAndSwim(T_matrix_ref, Q_ref, joint_fixed, joint_fixed_value, posture_weight, search_space,
                        cells, chem_steps_Nc,swim_length_Ns, step_size_Ci, d_attr, w_attr, h_rep, w_rep):

    best = Bacteria(problem_size, search_space, joint_fixed, joint_fixed_value)
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>best = " + str(best.vector))

    for j in range(0, chem_steps_Nc):
        moved_cells = []

        for i, cell in enumerate(cells):
            #print("best.cost = " + str(best.cost))
            sum_nutrients = 0
            evaluate(T_matrix_ref, Q_ref, posture_weight, cell, cells, d_attr, w_attr, h_rep, w_rep)

            if (best.cost == None) or (cell.cost < best.cost): best = cell

            sum_nutrients += cell.fitness

            for m in range(swim_length_Ns):
                print("swim_length m = " + str(m))

                new_cell = tumble_cell(joint_fixed, joint_fixed_value, search_space, cell, step_size_Ci)
                #print("cell vector =    " + str(cell.vector))
                #print("new cell vector =" + str(new_cell.vector))

                evaluate(T_matrix_ref, Q_ref, posture_weight, new_cell, cells, d_attr, w_attr, h_rep, w_rep)

                if (cell.cost < best.cost):
                    best = cell

                if new_cell.fitness > cell.fitness:
                    break

                cell = new_cell
                sum_nutrients += cell.fitness


            cell.sum_nutrients = sum_nutrients
            moved_cells.append(cell)

            print("chemo j = " + str(j) + " f = " + str(best.fitness) + " cost" + str(best.cost))
            cells = moved_cells

    return best, cells



if __name__ == "__main__":



    #initial
    #problem configuration
    ref_postures = copy.copy(original_postures_config)
    search_space = copy.copy(joint_angle_limit)
    posture_weight = copy.copy(score_weight)

    problem_size = 7 #Dimension of the search space


    pop_size_S = 50 #Total number of bacteria in the population
    chem_steps_Nc = 100 #The number of chemo tactic steps
    swim_length_Ns = 4  #The swimming length
    repro_steps_Nre = 4 #Number of reproduction steps
    elim_disp_steps_Ned = 2 #Number of elimination-dispersal event
    p_eliminate_Ped = 0.25 #Elimination-dispersal probability
    step_size_Ci = 5 #The size of the step taken in the random direction specified by the tumble

    d_attr = 0.1 #attraction coefficient
    w_attr = 0.2 #attraction coefficient
    h_rep = d_attr #repulsion coefficient
    w_rep = 10 #repulsion coefficient

    Search_New_Postures_by_BFOA(ref_postures, joint_fixed, joint_fixed_value,posture_weight,
            problem_size, search_space, pop_size_S,
            elim_disp_steps_Ned, repro_steps_Nre, chem_steps_Nc, swim_length_Ns, step_size_Ci, p_eliminate_Ped,
            d_attr, w_attr, h_rep, w_rep)

#########
