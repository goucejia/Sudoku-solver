'''
Derrick Treul - treul004
AStar implementation

Notes:
problem state must have:
- cost attribute - cost of getting to that state
- value attribute - heuristic value to goal state
- evaluation method - updates state's value
Returns node of goal state, so path must be contained in the state class if path matters.
'''

from node import *

def AStar(problem):
  '''
  based off of pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm
  '''
  openset = set()
  current = Node(problem.initial)
  openset.add(current)
  fScore = dict()
  problem.evaluation(current.getState())
  fScore[current] = current.getState().value
  while openset:
    # input()
    currentf = float('inf') 
    for node in openset: # find minimum fScore
      if fScore[node] < currentf:
        current = node
        currentf = fScore[current]
    if problem.isGoal(current.getState()):
      return current
    openset.remove(current)
    neighbors = current.expand(problem)
    for node in neighbors:
      if node not in openset:
        openset.add(node)
      problem.evaluation(node.getState()) # evaluate cost
      fScore[node] = node.getState().cost + node.getState().value # cost + heuristic

