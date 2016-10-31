"""
ACO to solve TSP ry48p Assymetric travelling salesman problem
"""

import random,csv
import timeit

# Algorithm paramters
ant_count = 10
iterations = 500
PheromoneConstant = 1.0
DecayConstant = 0.2
Alpha = 1	# Pheromone constant
Beta = 1	# Heuristic constant

RANDOM = 1
CITY0 = 0
initialization = RANDOM


# Creates an emplty path matrix for movemet between each and every city
def emptyPath(city_count):
    path = []
    for from_city in range(city_count):
        path1 = []
        for to_city in range(city_count):
             path1.append(0)
	path.append(path1)
    return path

# Returns the total cost of the tour for one ant
def pathLength(cities, path):
    path_with_next_city = path[1:] + [path[0]]
    pairs = zip(path, path_with_next_city)
    return sum([cities[r][c] for (r,c) in pairs])

# Initialize the ants to a random city or specific city
def initialize_ants(ant_count,cities_count):
	path = []

	for ant in range(ant_count):
		if initialization == RANDOM:
			path.append([random.randint(0,cities_count-1)])
		elif initialization == CITY0:
			path.append([CITY0])
	return path

# Check if all ant have completed tour
def isAllCompletedTour(paths,cities_count):

	for ant in range(len(paths)):
		if len(paths[ant]) < cities_count:
			return False
	return True

# Calculate sum total of the probability distribution to unvisited cities
def sumTotal(cities_matrix,pheromone_trail,visited_path):

	total = 0.0
	current_city = visited_path[-1]
	for city in range(len(cities_matrix)):
		if city not in visited_path:
			total = total + pow(pheromone_trail[current_city][city],Alpha) * pow(1.0/cities_matrix[current_city][city],Beta)
	return total

# get Probability Distribution
def getProbabilityDistributionList(cities_matrix, pheromone_trail,visited_path):

	sumTotalValue = sumTotal(cities_matrix, pheromone_trail,visited_path)
	probList = []
	total = 0
	current_city = visited_path[-1]
	#print "Current City:"+str(current_city)
	if sumTotalValue != 0:	# 1st iteration where there is no pheromone trail
		for city in range(len(cities_matrix)):
			if city not in visited_path:
				prev_probability = 0
				if len(probList) > 0:
					(prev_city,prev_prob) = probList[-1]
					prev_probability = prev_prob
				cummulative_prob = (prev_probability + (pow(pheromone_trail[current_city][city],Alpha) * pow(1.0/cities_matrix[current_city][city],Beta))/sumTotalValue)
				#print (pow(pheromone_trail[current_city][city],Alpha) * pow(1.0/cities_matrix[current_city][city],Beta))/sumTotalValue
				#if prev_probability < 1.0 and cummulative_prob == 1.0 and city < 45:
				#	print "hurray"+str(prev_probability)+":"+str(current_city)+":"+str(city)+":"+str((pow(pheromone_trail[current_city][city],Alpha) * pow(1.0/cities_matrix[current_city][city],Beta))/sumTotalValue)
				probList.append((city,cummulative_prob))
	return probList


# Find the next unvisited city
def nextCity(cities_matrix, pheromone_trail,visited_path):

	prob_list = getProbabilityDistributionList(cities_matrix, pheromone_trail,visited_path)

	next_city = -1

	if len(prob_list) == 0:	# initial condition
		next_city = random.randint(0,len(cities_matrix)-1)
		while next_city in visited_path:
			next_city = random.randint(0,len(cities_matrix)-1)
	else:
		#print "list------"+str(prob_list)
		toss = random.random()
		for (city,prob) in prob_list:

			if toss <= prob:
				#print str(visited_path)+"*************************************"+str(city)+":"+str(prob)
				next_city = city
				break
	if next_city == -1:
		print str(prob_list)+"*****"+str(toss)
	return next_city

# new pheromone for a particulat edge
def newPheromone(from_city,to_city,paths,cities_matrix):

	tot = 0.0
	for ant in range(len(paths)):
		# Check if the ant has used this path
		if to_city in paths[ant] and from_city in paths[ant]:

			if paths[ant].index(to_city) - paths[ant].index(from_city) == 1:
				tot = tot + PheromoneConstant	/ pathLength(cities_matrix,paths[ant])

	return tot

# Update Pheromone
def updatePheromone(pheromone_trail, path_array,cities_matrix):
	for from_city in range(len(pheromone_trail)):
		for to_city in range(len(pheromone_trail)):

			if from_city == to_city:
				pheromone_trail[from_city][to_city] = 0
			else:
				pheromone_trail[from_city][to_city] = (1 - DecayConstant) * pheromone_trail[from_city][to_city] + newPheromone(from_city,to_city,path_array,cities_matrix)
			#print "Pheromone strength:"+str(pheromone_trail[from_city][to_city])
	return pheromone_trail


# iterationResult
def iterationResult(iteration,paths,cities_matrix,(globalBest,path)):
	print "Iteration:"+str(iteration)
	print "**********************************"
	localBest = 9999999
	for ant in range(len(paths)):
		cost = pathLength(cities_matrix,paths[ant])
		#print "Ant:"+str(ant)+"	Path:"+str(paths[ant])+"\n"
		if cost < globalBest:
			globalBest = cost
			path = paths[ant]
		if cost < localBest:
			localBest = cost
	print "local Best:"+str(localBest)

	#if localBest == 9999999:
	#	print "No local best"
	#	for ant in range(len(paths)):
	#		print str(pathLength(cities_matrix,paths[ant]))+"----"+str(paths[ant])

	f = open('result.csv','a')
	f.write(str(iteration)+","+str(localBest)+"\n")
	f.close()
	return (globalBest,path)


# Find the shortes path
def shortestPath(cities_matrix, ant_count, iterations):

	cities_count = len(cities_matrix)
	pheromone_trail = emptyPath(cities_count)

	globalBest = 999999999999
	path = []
	f = open('result.csv','a')
	f.write("Iteration,LocalBest\n")
	f.close()
	for iteration in range(iterations):

		# Initialize ants with a random city
		paths = initialize_ants(ant_count,cities_count)

		while not isAllCompletedTour(paths,cities_count):	# End iteration when all ants have completed the tour
			# For each ant in the colony
			for ant in range(ant_count):

				# Termination criteria
				if len(paths[ant]) < cities_count:

					paths[ant].append(nextCity(cities_matrix, pheromone_trail,paths[ant]))	# Find next town

		# After all ants have completed the tour - Update pheromone
		updatePheromone(pheromone_trail, paths,cities_matrix)
		(globalBest,path) = iterationResult(iteration,paths,cities_matrix,(globalBest,path))
	return (globalBest,path)

# Read matrix from a customized file
def readTsp():
	pathmatrix = []
	tspfile = open('tsp_matrix.atsp', 'r')
	for cities in range(48):
		city = []

		line1 = tspfile.readline()
		for node in line1.split():
			city.append(int(node.strip()))

		line1 = tspfile.readline()
		for node in line1.split():
			city.append(int(node.strip()))

		line1 = tspfile.readline()
		for node in line1.split():
			city.append(int(node.strip()))

		line1 = tspfile.readline()
		for node in line1.split():
			city.append(int(node.strip()))

		pathmatrix.append(city)
	return pathmatrix

def main():

    print "starting"
    distance_matrix = readTsp()
    globalBest = shortestPath(distance_matrix, ant_count,iterations)
    print "len = ", globalBest


# This experiement graphs and plots the performance of the ACO against different set of ant population and generations
def Experiement1():

	geneartions = [10,50,100,250,500,1000]
	antpopulation = [1,10,50,100,150,200]

	for gen in geneartions:
		for pop in antpopulation:
			ant_count = pop
			iterations = gen
			distance_matrix = readTsp()
			globalBest = shortestPath(distance_matrix, ant_count,iterations)


# This experiement plots and graphs the performance of ACO against different set of decay constants
def Experiement2():

	decay_constants = [0.01,0.25,0.5,0.75,1.0]

	for decay in decay_constants:
		ant_count = 100
		iterations = 300
		PheromoneConstant = 1.0
		DecayConstant = decay
		Alpha = 1	# Pheromone constant
		Beta = 1	# Heuristic constant
		f = open('result.csv','a')
		f.write('Experiement2\n')
		f.write('decay:'+str(decay)+'\n')
		f.close()
		distance_matrix = readTsp()
		globalBest = shortestPath(distance_matrix, ant_count,iterations)

# This experiement plots and graphs the performance of ACO against different set of pheromone constants
def Experiement3():

	pheromone_constants = [1,0.01,-10,100,1000]

	for pheromone in pheromone_constants:
		ant_count = 100
		iterations = 300
		PheromoneConstant = pheromone
		DecayConstant = 0.2
		Alpha = 1	# Pheromone constant
		Beta = 1	# Heuristic constant
		f = open('result.csv','a')
		f.write('Experiement3\n')
		f.write('pheromone:'+str(pheromone)+'\n')
		f.close()
		distance_matrix = readTsp()
		globalBest = shortestPath(distance_matrix, ant_count,iterations)

# This experiement plots and graphs the performance of ACO against different set of alpha and beta
def Experiement4():

	alpha_list = [0.01,0.25,0.5,0.75,1.0]
	beta_list = [0.01,0.25,0.5,0.75,1.0]

	for alpha_val in alpha_list:
		for beta_val in beta_list:
			ant_count = 100
			iterations = 300
			PheromoneConstant = 1.0
			DecayConstant = 0.2
			Alpha = alpha_val	# Pheromone constant
			Beta = beta_val		# Heuristic constant
			f = open('result.csv','a')
			f.write('Experiement4\n')
			f.write('alpha:'+str(alpha_val)+',beta:'+str(beta_val)+'\n')
			f.close()
			distance_matrix = readTsp()
			globalBest = shortestPath(distance_matrix, ant_count,iterations)


if __name__ == "__main__":
   import cProfile
   cProfile.run('main()')

    #main()
