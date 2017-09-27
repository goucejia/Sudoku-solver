import copy
import time
from AIproblem import *
from solverClass import *
import random
import copy


class Problem(object):
    def __init__(self, initial):
        self.initial = initial
        self.type = len(initial)  # Defines board type, either 6x6 or 9x9
        self.height = int(self.type / 3)  # Defines height of quadrant (2 for 6x6, 3 for 9x9)

    # Return set of valid numbers from values that do not appear in used
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Return first empty spot on grid (marked with 0)
    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    def actions(self, state):
        number_set = range(1, self.type + 1)  # Defines set of valid numbers that can be placed on board
        in_column = []  # List of valid values in spot's column
        in_block = []  # List of valid values in spot's quadrant

        row, column = self.get_spot(self.type, state)  # Get first empty spot on board

        # Filter valid values based on row
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)

        # Filter valid values based on column
        for column_index in range(self.type):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)

        # Filter with valid values based on quadrant
        row_start = int(row / self.height) * self.height
        column_start = int(column / 3) * 3

        for block_row in range(0, self.height):
            for block_column in range(0, 3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)

        for number in options:
            yield number, row, column

            # Returns updated board after adding new valid value

    def result(self, state, action):

        play = action[0]
        row = action[1]
        column = action[2]

        # Add new valid value to board
        new_state = copy.deepcopy(state)
        new_state[row][column] = play

        return new_state

    # Use sums of each row, column and quadrant to determine validity of board state
    def goal_test(self, state):

        # Expected sum of each row, column or quadrant.
        total = sum(range(1, self.type + 1))

        # Check rows and columns and return false if total is invalid
        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.type):
                column_total += state[column][row]

            if (column_total != total):
                return False

        # Check quadrants and return false if total is invalid
        for column in range(0, self.type, 3):
            for row in range(0, self.type, self.height):

                block_total = 0
                for block_row in range(0, self.height):
                    for block_column in range(0, 3):
                        block_total += state[row + block_row][column + block_column]

                if (block_total != total):
                    return False

        return True


class Node:
    def __init__(self, state, action=None):
        self.state = state
        self.action = action

    # Use each action to create a new board state
    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    # Return node with new board state
    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, action)


class sudokuState(ProblemState):
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
	print("Solving now.")
	start_time = time.time()
	
	def __init__( self, testCase):
		Solver.__init__(self, testCase, None)
		self.userid = 'songx544'

	def solve(self):
		popsize = 10
		problem = Problem(self.testCase)

		#making 100 populations of states and finding their fitness. If there's a goal, return it
		StateList = []
		for i in range(0,popsize):
			x = sudokuState(self.testCase)
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


