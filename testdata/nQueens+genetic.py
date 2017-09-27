from AIproblem import *
from solverClass import *
import time
#from solver import *
import random
import copy

class nQueensProblem(AIproblem):
	def __init__(self, size, evalFn):
		AIproblem.__init__(self, None, size, evalFn, None)

	def getRandomAction( self, state ):
		# randomly produce a single action applicable for this state
		# mutate a state happens here
		for i in range(0,self.size):
			#############################################
			#MUTATE RATE HERE
			#############################################
			if random.random()<0.01:
				state.state[i]=random.randint(1,self.size)
		return state

	def getActions( self, statelist, popsize) :
		# Getting parents by possibility
		ChosenIndex = []
		WeightSum = 0.0
		for i in range(0,popsize):
			WeightSum += statelist[i].value


		for j in range(0,popsize*2):
			RandWeight = random.uniform(0.0, WeightSum)
			tempWeightSum = 0
			for i in range(0,popsize):
				tempWeightSum += statelist[i].value
				if RandWeight<=tempWeightSum:
					ChosenIndex.append(i)
					break
		return ChosenIndex


	def applyAction (self, state1, state2) :
		# parent merging to creat child
		n = random.randint(1,self.size-1)
		newState = state1.state[:n] + state2.state[n:]
		temp = nQueenState(self.size)
		temp.state = newState
		return temp

	def evaluation(self, state):
		return state.evalFn

	def isGoal (self, state):
		if state.evalFn == 0:
			return True
		else:
			return False



class nQueenState(ProblemState):
	def __init__(self, size):
		ProblemState.__init__(self, [], size, value=0)
		for i in range(0,self.size):
			self.state.append(random.randint(1,self.size))


	def evaluate( self, evalFn ):
		self.value = evalFn( self.state )



def fitness(state):
	conflict = 0
	i=0
	while(i<len(state)):
		j=i+1
		while(j<len(state)):
			if state[i]==state[j]:
				conflict = conflict+1
			elif state[i]+(j-i)==state[j] or state[i]+(i-j)==state[j]:
				conflict = conflict+1
			j=j+1
		i=i+1
	if conflict == 0:
		result = 2
	else:
		result = 1/conflict
	return result



class SolverGA(Solver):
	def __init__( self, testCase):
		Solver.__init__(self, testCase, None)
		self.userid = 'lixx2999'
		self.generation = 0

	def solve(self):
		print("hello, please wait...")

		##################################################
		#POPULATION SIZE HERE
		##################################################

		popsize = 10
		Problem = nQueensProblem(self.testCase, fitness)

		#making 100 populations of states and finding their fitness. If there's a goal, return it
		StateList = []
		for i in range(0,popsize):
			x = nQueenState(self.testCase)
			x.evaluate(fitness)
			StateList.append(x)
			if x.value == 1:
				return x

		while True:

			#picking 100 pairs of parents by their fitness
			ChosenIndex = Problem.getActions(StateList,popsize)

			#obtaining 100 new children
			TempList = []
			for i in range(0,popsize):
				p1 = ChosenIndex[i]
				p2 = ChosenIndex[i*2]
				TempList.append(Problem.applyAction(StateList[p1], StateList[p2]))

			#mutate
			StateList = copy.deepcopy(TempList)
			for i in range(0,popsize):
				StateList[i] = Problem.getRandomAction(StateList[i])
				StateList[i].evaluate(fitness)
				if StateList[i].value == 2:
					return StateList[i]

			self.generation +=1

	def printSolution(self):
		if self.solution:
			print(self.solution)
			


print("Please input how many queens you want:")
customsize = int(input())
costtime = 0
generation = 0
iteration = 1

#for smaller n, I test 10 times and get the average
for i in range(0,iteration):
	start = time.clock()
	if customsize == 1:
		print([1])
	else:
		Solve = SolverGA(customsize)
		print(Solve.solve().state)
		#print("generations: ")
		#print(Solve.generation)
		generation += Solve.generation
		end = time.clock()
		#print("time cost")
		#print (end-start)
		costtime += (end-start)

print("average generations: ")
print(generation/iteration)

print("average time cost")
print (costtime/iteration)