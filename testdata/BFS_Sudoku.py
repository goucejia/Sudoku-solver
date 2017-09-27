from queue import Queue
import copy
import time


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


def BFS(problem):
    # Create initial node of problem tree holding original board
    node = Node(problem.initial)
    # Check if original board is correct and immediately return if valid
    if problem.goal_test(node.state):
        return node

    frontier = Queue()
    frontier.put(node)

    # Loop until all nodes are explored or solution found
    while (frontier.qsize() != 0):

        node = frontier.get()
        for child in node.expand(problem):
            if problem.goal_test(child.state):
                return child

            frontier.put(child)

    return None


def solve_bfs(board):
    print("Solving...")
    start_time = time.time()

    problem = Problem(board)
    solution = BFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print("Found solution")
        for row in solution.state:
            print(row)
    else:
        print("No possible solutions")

    print("Elapsed time: " + str(elapsed_time))