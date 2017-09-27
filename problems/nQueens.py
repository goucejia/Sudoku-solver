from AIproblem import *
from solverClass import *
from solver import *
import random
import copy

class nQueensProblem(AIproblem):
	def __init__(self, size, evalFn):
		AIproblem.__init__(self, None, size, evalFn, None)

	def getRandomAction( self, state ):
		# randomly produce a single action applicable for this state
		# mutate a state happens here
		for i in range(0,8):
			if state.state[i]!=0:
				if random.random()<0.1:
					state.state[i]=random.randint(1,8)
		return state

	def getActions( self, statelist, popsize) :
		# Getting parents by possibility
		ChosenIndex = []
		WeightSum = 0
		for i in range(0,popsize):
			WeightSum += statelist[i].value


		for j in range(0,popsize*2):
			RandWeight = random.uniform(0, WeightSum-1)
			tempWeightSum = 0
			for i in range(0,popsize):
				if RandWeight<=tempWeightSum:
					ChosenIndex.append(i)
					break
				tempWeightSum += statelist[i].value

		return ChosenIndex


	def applyAction (self, state1, state2) :
		# parent merging to creat child
		notDone = True
		while(notDone):
			n = random.randint(0,8)
			newState = state1.state[:n] + state2.state[n:]
			if newState.count(0) == (8-self.size):
				notDone = False
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
		ProblemState.__init__(self, [0,0,0,0,0,0,0,0], size, value=0)
		for i in range(0,8):
			self.state[i] = random.randint(1,8)

		#changing some to 0 in order to represent empty columes
		for i in range(0,8-self.size):
			j=random.randint(0,7)
			while(self.state[j]==0):
				j=random.randint(0,7)
			self.state[j]=0

	def evaluate( self, evalFn ):
		self.value = evalFn( self.state )



def fitness(state):
	conflict = 0
	i=0
	while(i<8):
		j=i+1
		while(j<8):
			if not (state[i]==0 or state[j]==0):
				if state[i]==state[j]:
					conflict = conflict+1
				elif state[i]+(j-i)==state[j] or state[i]+(i-j)==state[j]:
					conflict = conflict+1
			j=j+1
		i=i+1
	result = ((28 - conflict)/28)-0.5
	if result<0:
		result = 0
	#print(result)
	return result



class SolverGA(Solver):
	def __init__( self, testCase):
		Solver.__init__(self, testCase, None)
		self.userid = 'lixx2999'

	def solve(self):
		print("hello, please wait for a few seconds...")

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
				p1 = ChosenIndex[i*2]
				p2 = ChosenIndex[i*2+1]
				TempList.append(Problem.applyAction(StateList[p1], StateList[p2]))

			#mutate
			StateList = copy.deepcopy(TempList)
			for i in range(0,popsize):
				StateList[i] = Problem.getRandomAction(StateList[i])
				StateList[i].evaluate(fitness)
				if StateList[i].value == 0.5:
					return StateList[i]

	def printSolution(self):
		if self.solution:
			print(self.solution)

print("Please input how many queens you want:")
customsize = int(input())
Solve = SolverGA(customsize)
print(Solve.solve().state)
print("numbers are the index of boxes of that column")