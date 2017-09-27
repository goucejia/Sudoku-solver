import sys,os
sys.path.append('algorithms')
sys.path.append( os.path.realpath('..') + '/class-repo/projectClasses' )
from AIproblem import *
from bfs import *
import random
from copy import deepcopy
import time

# USED TO LOG ERROR DATA
import logging
LOG_FILENAME =  os.path.realpath('.') + '/testdata/nQueensBFSerror.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

class nQueensProblem(AIproblem):
    def __init__(self, size, evalFn):
        board = [0 for x in range(size)]
        initial = nQueenState(board)
        AIproblem.__init__(self, initial, size, evalFn, None)
        self.recordPath = True

    def getRandomAction( self, state ):
        actions = self.getActions(state)
        return random.sample(actions,1)[0]

    def getActions( self, state) :
        '''
        returns list of valid actions in tuple form of (i,j)
        '''
        actions = set()
        rows = set()
        board = state.state
        for row in board:
            rows.add(row)
        remainingRows = set(range(1,len(board)+1)) - rows
        if 0 not in board:
            print('error, board is filled')
            return {}
        nextIndex = board.index(0)
        if nextIndex == 0:
            for action in remainingRows:
                actions.add((0, action))
        for i in range(nextIndex):
            for j in remainingRows:
                if abs(j-i) != abs(j-board[i]):
                    actions.add((nextIndex, j))
        return actions

    def applyAction (self, state, action) :
        i, j = action
        newState = deepcopy(state)
        newState.state[i] = j
        return newState

    def evaluation(self, state):
        return state.evalFn

    def isGoal (self, state):
        return self.evalFn(state.state)



class nQueenState(ProblemState):
    def __init__(self, state):
        ProblemState.__init__(self, state, len(state), value=0)


def checker(state):
    '''
    Checks if state is success for nqueens.
    checks all columns have different values then checks diagonals
    '''
    rows = set()
    for rowIndex in state:
        if rowIndex in rows:
            return False
        rows.add(rowIndex)
    if 0 in rows:
        return False
    for i in range(len(state)):
        for j in range(i+1, len(state)):
            if abs(j-i) == abs(state[j]-state[i]):
                return False
    return True


try:
    for i in range(4, 25): # idk how big before it breaks, so i'm going 4 - 24
        fileName = os.path.realpath('.') + "/testdata/nQueensBFSTest" + str(i) + ".txt"
        a = open(fileName, 'w')
        titlestring = "NQueens using BFS, BoardSize = " + str(i) + "\n"
        a.write(titlestring)
        startTime = int(round(time.time() * 1000))
        node = BFS(nQueensProblem(i, checker))
        endTime = int(round(time.time() * 1000))
        s = "Goal state: " + str(node.state) + "\n"
        a.write(s)
        s = "Nodes traveled: " + str(node.nodeCount) + "\n"
        a.write(s)
        s = "Total time in ms: " + str(endTime - startTime) + "\n"
        a.write(s)
        a.close()
        print("completed case " + str(i))
except:
    # caught an exception. probably out of memory so log it
    s = "Time: " + str(int(round(time.time()*1000)) - startTime) + ", Nodes: " + str(Node.nodeCount)
    logging.exception(s)
    raise