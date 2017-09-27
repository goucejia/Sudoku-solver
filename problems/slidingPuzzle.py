'''
Derrick Treul - treul004
Sliding puzzle implementation
'''

from AIproblem import *
from copy import deepcopy
import random

def manhattan(state, goal):
  '''
  Total Manhattan distances
  '''
  score = 0
  for i in range(len(state)):
    for j in range(len(state)):
      a,b = findTile(state[i][j], goal)
      score += abs(i-a)
      score += abs(j-b)
  return score

def findTile(tile, board):
  '''
  finds coordinates of tile
  '''
  for i in range(len(board)):
    for j in range(len(board)):
        if board[i][j] == tile:
          return (i,j)
  return (-1,-1) # not found

class SlidingPuzzle(AIproblem) :
  '''
  Note: Actions are in the form of coordinates of the tile that will be moved.
        for example - if the blank tile is at the bottom right (2,2), an action to move
        the tile above it would be (1,2)
  '''

  def findTile(self, tile, board):
    '''
    finds coordinates of tile
    '''
    for i in range(len(board)):
      for j in range(len(board)):
          if board[i][j] == tile:
            return (i,j)
    return (-1,-1) # not found
  def __init__( self, board, goal=None, evalFn=manhattan ):
    if not len(board) == len(board[0]):
      print('Puzzle must be square')
      return None
    
    # The board is a list of rows. Numbers are 1..n. The blank space is represented by 0

    size = len(board)*len(board)
    self.rowLength = len(board)
    self.recordPath = True
    self.previous = (-1,-1)
    self.explored = set()
    if not goal:
      # If not specified the goal state will be tiles ordered by rows with the blank space in the lower right.
      goal = []
      for tile in range(1, size, self.rowLength):
        goal.append(list( range( tile, tile+self.rowLength )))
      goal[self.rowLength-1][self.rowLength-1] = 0
      self.solution = []

    # find location of blank space
    zero = findTile(0, board)
    if zero == (-1,-1):
      print('No blank space')
      return None

    initialState = SlidingPuzzleState(board, size, self.rowLength, zero, goal, evalFn)
    super().__init__(initialState, size, evalFn, goal)


  def getRandomAction(self, state):
    actions = getActions(state)
    return random.choice(actions)

      
  def getActions(self,state):
    i, j = state.zero
    actions = [] # list of coordinates blank square can move
    
    # left
    if i > 0:
      actions.append((i-1,j))
    # right
    if i < self.rowLength-1:
      actions.append((i+1,j))
    # up
    if j > 0:
      actions.append((i,j-1))
    # down
    if j < self.rowLength-1:
      actions.append((i,j+1))

    for action in actions: # remove any actions that will loop
      if self.applyAction(state, action).getStateTuple() in state.traveled:
        actions.remove(action)
    return actions

  def applyAction(self, state, action):
    newState = deepcopy(state)
    newState.apply(action)
    return newState

  def isGoal(self, state):
    return state.isGoal()

class SlidingPuzzleState(ProblemState):
  def __init__(self, state, size, rowLength, zero, goal, evalFn, value=0):
    super().__init__(state, size, value)
    self.rowLength = rowLength
    self.zero = zero # coordinates of empty tile
    self.goal = goal 
    self.actions = [] # list of actions taken to get to this state
    self.traveled = set() # list of states already traveled. This prevents loops
    self.addState(self.state) # add initial to traveled
    self.evalFn = evalFn 
    self.cost = 0 # cost of getting to this state. should just be length of actions

  def getStateTuple(self):
    '''
    helper used to convert state from 2d lists to 2d tuples for hashing into set
    '''
    rows = []
    for row in self.state:
      rows.append(tuple(row))
    return tuple(rows)

  def addState(self, state):
    '''
    adds state to set of traveled states
    '''
    rows = []
    for row in state:
      rows.append(tuple(row))
    self.traveled.add(tuple(rows))

  def isGoal(self):
    return self.goal == self.state

  def evaluate(self, evalFn):
    self.value = evalFn(self.state, self.goal)
    return self.value

  def apply(self, action):
    i, j = action
    if i < 0 or i > len(self.state)-1 or j < 0 or j > len(self.state)-1:
      print('invalid move')
    i1, j1 = self.zero
    self.state[i][j], self.state[i1][j1] = self.state[i1][j1], self.state[i][j]
    self.zero = (i,j)
    self.cost += 1
    self.actions.append(action)
    self.addState(self.state)

