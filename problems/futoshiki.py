from CSPproblems import *

#f1 = InputPuzzleClass(
#  [4,4],
#  [[3,[2,0]],
#   [1,[2,1]],
#   [1,[3,3]],
#   ['>',[1,1],[1,2]],
#   ['>',[1,2],[2,2]]
#   ],
#  PuzzleType.futoshiki,
#  [[4,2,1,3],
#   [1,4,3,2],
#   [3,1,2,4],
#   [2,3,4,1]] )

class futoshikiPuzzle:
    ###initialization of the puzzle class ###

    ##### what does board do? ####
    def __init__(self, size, puzzle):
        self.size = size
        self.constraintArr = puzzle
        self.constraints = []
        self.variables = []
        self.board = [[0 for x in range(self.size[0])] for y in range(self.size[1])]

    ### Generate constraints of puzzles according to input requirements
    ### Add to the constraints list
    def generateConstraint(self):
        ### adding general constrants (same applies to any futoshiki) ###

        ### setting all input to be between 1 ~ problem size ###
        for i in range(self.size):
            for j in range(self.size):
                self.variables.append(ConstraintVar((list(range(1, self.size+1))), [i,j]))

        ### make every digit in a row distinct ###
        for i in range(self.size):
            templist = []
            for j in range(self.size):
                templist.append([i,j])
            allDiff(self.constraints, templist)

        ### make every digit in a column distinct ###
        for i in range(size):
            templist = []
            for j in range(size):
                templist.append([j,i])
            allDiff(self.constraints, templist)

        ### filling in boxes whose value is given ###
        for i in range(len(self.constraintArr)):
            if (len(self.constraintArr[i]) == 2):
                value = self.constraintArr[i][0]
                cord = self.constraintArr[i][1]
                self.constraints.append(UnaryConstraint(cord, lambda x: x == value))

            ### filling comparision between two boxes ###
            elif (len(self.constraintArr[i]) == 3):
                op = self.constraintArr[i][0]
                cord1 = self.constraintArr[i][1]
                cord2 = self.constraintArr[i][2]

                self.variables.append(cord1)
                self.variables.append(cord2)

                if op == ">":
                    self.constraints.append(BinaryConstraint(cord1, cord2, lambda x, y: x > y))
                if op == "<":
                    self.constraints.append(BinaryConstraint(cord1, cord2, lambda x, y: x < y))

        def computeBoard(self):
            for var in self.variables:
                self.board[var.name[0]][constraint.name[1]] = var.domain
