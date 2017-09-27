import sys,os
sys.path.append('algorithms')
sys.path.append('problems')
sys.path.append( os.path.realpath('..') + '/class-repo/projectClasses' )

from bfs import *
from simpleProblem import *
from slidingPuzzle import *
from CrossMathPuzzle import *
from Backtracking import *
from Astar import *
from nQueens import *
from solverClass import Solver

class SolverAStar(Solver):
  def __init__(self, testCase):
    super().__init__(testCase, testCase.goal)
    self.userid = 'treul004'

  def solve(self):
    solutionNode = AStar(self.testCase)
    solutionState = solutionNode.getState()
    self.solution = solutionState.actions


# s = SolverAStar(SlidingPuzzle( [[8,0,6],[5,4,7],[2,3,1]] ))
# s.solve()
# s.printSolution()


class SolverBacktrackDfs(Solver):
        def __init__(self, testCase):
            super().__init__(testCase, testCase.goal)
            self.userid = 'fangx174'

        def solve(self):
            solutionNode = bDFS(self.testCase)
            solution = solutionNode.getState()


#There are another solver in nQueens from the problem folder to make sure it can run by itself too.
#Incase solver doesn't run, you can also run the nQueens in problem folder

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
