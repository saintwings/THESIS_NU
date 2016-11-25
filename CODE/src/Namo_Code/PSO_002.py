# particleswarm.py
# python 3.4.3
# demo of particle swarm optimization (PSO)
# solves Rastrigin's function

import random
import math    # cos() for Rastrigin
import copy    # array-copying convenience
import sys     # max float
import time
### local import ###
from utility_function import*

### add postures ###
## original posture ##
respect_posture_config =    [80,    -45,    -10,    135,    45,     0,      0,      85,-207,131,'close']
wai_posture_config =        [25,    -5,     -45,    100,    0,      -40,    45,     207,-54,-105,'close']
bye_posture_config =        [25,    -20,    0,      110,    -90,    -50,    -15,    229,-229,-34,'open']
rightInvite_posture_config =[10,    -10,    45,     60,     45,     0,      0,      218,-102,-96,'close']

original_posture_config = []
original_posture_config.append(respect_posture_config)
original_posture_config.append(wai_posture_config)

original_posture_config.append(bye_posture_config)
original_posture_config.append(rightInvite_posture_config)

avg_angle = cal_Avg_Angle(original_posture_config,7)

score_weight = [1,0.001,0.001]

def show_vector(vector):
  for i in range(len(vector)):
    print vector[i]
  print("\n")

def error(position, ref_pose, score_weight):
  err = 0.0
  pos_set = []
  posture = []
  #print("len position = "+str(len(position)))
  for i in range(len(position)):
    xi = position[i]
    posture.append(int(position[i]))
    #err += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10

  #print("posture ="+str(posture))
  #print("ref_posture ="+str(ref_pose))
  pos_set.append(posture)
  score = cal_Posture_Score(pos_set,ref_pose,score_weight)
  #print("score = "+str(score))
  #print(str(score[0][10]))
  err = score[0][10]
  return err

class Particle:
  def __init__(self, dim, minx, maxx, seed,fixed_joint ,avg_angle,ref_pose):
    self.rnd = random.Random(seed)
    self.position = [0.0 for i in range(dim)]
    self.velocity = [0.0 for i in range(dim)]
    self.best_part_pos = [0.0 for i in range(dim)]

    for i in range(dim):
      if i == fixed_joint:
        self.position[i] = avg_angle[i]
      else:
        self.position[i] = random.randint(minx[i],maxx[i])
      self.velocity[i] = random.randint(minx[i],maxx[i])

      print("i="+str(i)+" p="+str(self.position[i])+" v="+str(self.velocity[i]))

    self.error = error(self.position, ref_pose, score_weight) # curr error
    self.best_part_pos = copy.copy(self.position)
    self.best_part_err = self.error # best error

def Solve(max_epochs, n, dim, minx, maxx, fixed_joint, ref_pose,avg_angle, score_weight):
  rnd = random.Random(0)

  # create n random particles
  swarm = [Particle(dim, minx, maxx, i, fixed_joint ,avg_angle,ref_pose) for i in range(n)]

  best_swarm_pos = [0.0 for i in range(dim)] # not necess.
  best_swarm_err = sys.float_info.max # swarm best
  for i in range(n): # check each particle
    if swarm[i].error < best_swarm_err:
      best_swarm_err = swarm[i].error
      best_swarm_pos = copy.copy(swarm[i].position)

  epoch = 0
  w = 0.729    # inertia
  c1 = 1.49445 # cognitive (particle)
  c2 = 1.49445 # social (swarm)
  w = 1    # inertia
  c1 = 2 # cognitive (particle)
  c2 = 2 # social (swarm)

  while epoch < max_epochs:

    if epoch % 10 == 0 and epoch > 1:
      print("Epoch = " + str(epoch) +
        " best error = %.3f" % best_swarm_err)

    for i in range(n): # process each particle

      # compute new velocity of curr particle
      for k in range(dim):
        r1 = rnd.random()    # randomizations
        r2 = rnd.random()
        #print("r1 " + str(r1) +"r2 "+ str(r2))
        swarm[i].velocity[k] = ( (w * swarm[i].velocity[k]) +
           (c1 * r1 * (swarm[i].best_part_pos[k] -
          swarm[i].position[k])) +
          (c2 * r2 * (best_swarm_pos[k] -
          swarm[i].position[k])) )

        #print("v = " + str(swarm[i].velocity[k]))

        if swarm[i].velocity[k] < minx[k]:
          swarm[i].velocity[k] = minx[k]
        elif swarm[i].velocity[k] > maxx[k]:
          swarm[i].velocity[k] = maxx[k]

      # compute new position using new velocity
      for k in range(dim):
        if k == fixed_joint:
          swarm[i].position[k] = avg_angle[k]
        else:
          swarm[i].position[k] += swarm[i].velocity[k]
          tmp = swarm[i].position[k]
          swarm[i].position[k] = round(swarm[i].position[k],0)
        #print("p = " + str(swarm[i].position[k]))

      # compute error of new position
      swarm[i].error = error(swarm[i].position, ref_pose, score_weight)

      # is new position a new best for the particle?
      if swarm[i].error < swarm[i].best_part_err:
        swarm[i].best_part_err = swarm[i].error
        swarm[i].best_part_pos = copy.copy(swarm[i].position)

      # is new position a new best overall?
      if swarm[i].error < best_swarm_err:
        best_swarm_err = swarm[i].error
        best_swarm_pos = copy.copy(swarm[i].position)

    # for-each particle
    epoch += 1
  # while
  return best_swarm_pos
# end Solve


def loop_PSO():
  for angle in range(7):
    for posture_count in range(4):
      time_start = time.time()
      print time_start

      print("\nBegin particle swarm optimizationusing Python demo\n")
      dim = 7
      angle_limit = [[0, 135], [-90, 0], [-45, 45], [0, 135], [-90, 90], [-50, 45], [-45, 45]]
      angle_min = [0, -90, -45, 0, -90, -50, -45]
      angle_max = [135, 0, 45, 135, 90, 45, 45]
      # angle_min = [-10,-10,-10,-10,-10,-10,-10]
      # angle_max = [10,10,10,10,10,10,10]
      num_particles = 1000
      max_epochs = 10
      fixed_joint = angle
      posture_index = posture_count
      ref_pose = original_posture_config[posture_index]

      print("Setting num_particles = " + str(num_particles))
      print("Setting max_epochs    = " + str(max_epochs))
      print("\nStarting PSO algorithm\n")

      best_position = Solve(max_epochs, num_particles,
                            dim, angle_min, angle_max, fixed_joint, ref_pose, avg_angle, score_weight)

      time_stop = time.time()
      time_diff = time_stop - time_start
      print("time = " + str(time_diff))

      print("\nPSO completed\n")
      print("\nBest solution found:")
      show_vector(best_position)
      err = error(best_position, ref_pose, score_weight)
      print("Error of best solution = %.6f" % err)

      print("\nEnd particle swarm demo\n")

      fileName = "./PSO_data/FixedIndex = " + str(fixed_joint) + "\t posture = " + str(
        posture_index) + "\t Date " + str(
        time.asctime()) + ".txt"
      file_data = open(fileName, 'w')
      file_data.write("ref pos = " + str(ref_pose) + "\n")

      file_data.write("\nbest set" + str(best_position) + "\n")
      file_data.write("\nbest score" + str(err) + "\n")

      file_data.write("\njoint fixed index = " + str(fixed_joint) + "\tvalue = " + str(avg_angle[fixed_joint]) + "\n")
      file_data.write("\ntime = " + str(time_diff) + "\n")

      file_data.close()

  pass


###### Main #######################
if __name__ == "__main__":
    #loop_PSO()

    time_start = time.time()
    print time_start

    print("\nBegin particle swarm optimizationusing Python demo\n")
    dim = 7
    angle_limit = [[0, 135], [-90, 0], [-45, 45], [0, 135], [-90, 90], [-50, 45], [-45, 45]]
    angle_min = [0, -90, -45, 0, -90, -50, -45]
    angle_max = [135, 0, 45, 135, 90, 45, 45]
    # angle_min = [-10,-10,-10,-10,-10,-10,-10]
    # angle_max = [10,10,10,10,10,10,10]
    num_particles = 1000
    max_epochs = 10
    fixed_joint = 5
    posture_index = 0
    ref_pose = original_posture_config[posture_index]

    print("Setting num_particles = " + str(num_particles))
    print("Setting max_epochs    = " + str(max_epochs))
    print("\nStarting PSO algorithm\n")

    best_position = Solve(max_epochs, num_particles,
                          dim, angle_min, angle_max, fixed_joint, ref_pose, avg_angle, score_weight)

    time_stop = time.time()
    time_diff = time_stop - time_start
    print("time = " + str(time_diff))

    print("\nPSO completed\n")
    print("\nBest solution found:")
    show_vector(best_position)
    err = error(best_position, ref_pose, score_weight)
    print("Error of best solution = %.6f" % err)

    print("\nEnd particle swarm demo\n")

    fileName = "./PSO_data/FixedIndex = " + str(fixed_joint) + "\t posture = " + str(
      posture_index) + "\t Date " + str(
      time.asctime()) + ".txt"
    file_data = open(fileName, 'w')
    file_data.write("ref pos = " + str(ref_pose) + "\n")

    file_data.write("\nbest set" + str(best_position) + "\n")
    file_data.write("\nbest score" + str(err) + "\n")

    file_data.write("\njoint fixed index = " + str(fixed_joint) + "\tvalue = " + str(avg_angle[fixed_joint]) + "\n")
    file_data.write("\ntime = " + str(time_diff) + "\n")

    file_data.close()

