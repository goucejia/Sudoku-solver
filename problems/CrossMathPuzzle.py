from AIproblem import *
from copy import deepcopy
from opDictionary import *


# This function check through each rows and apply the operation (+, -, *, /)
# to the existing evaluations with the next parameter
# After each iteration this function will calculate the value of each expressions and then
# compare with the given value, if all values are matched then return true, else false
def checkRows(state):
    for i in range(0, (state.size-2)):
        if state[i].contains("="):
            evaluation=state[i][0]
            for j in range(0, (state.size-1)):
                if ops.contains(state[i][j]) and state[i][j] != "=":
                    evaluation = ops.get(state[i][j])(evaluation, state[i][j+1])
                if evaluation != state[i][len(state.size)-1]:
                    return False
            return True


# Similar to checkRows, his function check through each columns and see
# the expressions in state matched with answers
def checkCols(state):
    for i in range(0, (state.size-2)):
        if state[(state.size-2)][i] == "=":
            evaluation=state[i][0]
            for j in range(0, (state.size-1)):
                if ops.contains(state[j][i]) and state[j][i] != "=":
                    evaluation = ops.get(state[i][j])(evaluation, state[i+1][j])
                if evaluation != state[len(state.size)-1][j]:
                    return False
            return True


# If both rows and columns check passes, then the goal state is reached
def isGoal(state):
    if checkCols(state) == True and checkRows(state) == True:
        return True
    else:
        return False


# Checking for any completed rows /columns (if not contains 0 in it)
# if the existing solution matches the given answer
# if not, this node is not expandable, thus returns false
def notExpandable(state):
    for i in range(0, state.size):
        if not state[i].contains(0) and state[i].contains("="):
            evaluation = state[i][0]
            for j in range(0, (state.size - 1)):
                if ops.contains(state[i][j]) and state[i][j] != "=":
                    evaluation = ops.get(state[i][j])(evaluation, state[i][j + 1])
                if evaluation != state[i][len(state.size) - 1]:
                        return True

    i = 0
    while i < state.size:
        for j in range(0, (state.size - 1)):
            if not state[j][i].contains(0) and state[-1][i] == "=":
                evaluation = state[i][0]
                if ops.contains(state[j][i]) and state[j][i] != "=":
                    evaluation = ops.get(state[i][j])(evaluation, state[i + 1][j])
                if evaluation != state[len(state.size) - 1][j]:
                        return True
        i += 1

    return True


 class CrossMathPuzzle(AIproblem):
    def __init__(self, board, size,  evalFn = None, goal = None):
        super().__init__(self, size, evalFn, goal)
        self.size = len(board)*len(board)
        self.length = len(board)
        self.board = board

        # Initialization
        initialState = CrossMathPuzzle(board, size)
        super().__init__(initialState, size, evalFn, goal)

        self.puzState = puzzleState(initialState, size, goal)




    # GetAction returns a valid changes for the current state that is not yet tried
    def getActions(self, state):
        actions = []
        j = 0
        while j < self.size:
            for i in range (0, self.size):
                if state[i].contains("=") and state[i][j] == "=":
                    for num in range(1, 10):
                        if num in puzzleState.getTried(self.puzState,state):
                            return
                        state[i][j] = num
                        puzzleState.addState(self.puzState, num)
                        actions.append(state)
        return actions


    def applyAction(self, state, action):
        newState= deepcopy(state)
        newState.apply(action)
        return newState

    def isGoal(self,state):
        if checkCols(state) == True and checkRows(state) == True:
            return True
        else:
            return False


 class puzzleState(ProblemState):
    def __init__(self, state, size, goal):
        super().__init__(self, state, size)
        self.size = size
        self.goal = goal
        self.tried= set()

    def addState(self, state, attempts):
        self.tried.add(attempts)

    def getTried(self, state):
        return self.tried

