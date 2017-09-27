from copy import deepcopy
from node import Node


def bDFS(problem):

    # Initialize the first node
    node = Node(problem.initial)

    # If the node is in the illegal state, immediately returns
    if problem.notExpandable(node.getState()):
        return

    # Check if the node is goal state before continue towards iteration
    if problem.isGoal(node.getState()):
        return node

    stack = [node]

    # Using the stack to keep track of our nodes for depth-first search
    # Check to see if any expansion of current state is illegal
    # If yes then returns to the last step
    # Otherwise continue until find the solution or no solution
    while len(stack) > 0:
        node = stack.pop()
        for child in node.expand(problem):
            bDFS(problem)
            stack.append(node)

    return None



