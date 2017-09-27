from CSPproblems import *
import itertools


# k1 = InputPuzzleClass(
#   [3,3],
#   [['*',6,[0,0],[1,0]],
#    ['-',1,[0,1],[0,2]],
#    ['+',7,[1,1],[1,2],[2,2]],
#    ['-',1,[2,0],[2,1]]],
#   PuzzleType.kenken,
#   [[3,1,2],[2,3,1],[1,2,3]]
#  )

class kenkenPuzzle:
    ###initialization of the puzzle class ###

    def __init__(self, size, constraintArr):
        self.size = size
        self.constraintArr = constraintArr
        self.constraints = []
        self.variables = []
        self.board = [[None for i in range(self.size[1])] for j in range(self.size[0])]  # board of constraint vars
        self.initVar()
        self.generateConstraint()
        print("kenken initialized")

    ### def kenken version of operations ###
    def kkAdd(*args):
        # if (None in args):
        #     return None
        sum = 0;
        for arg in args:
            sum += arg
        return sum

    def kkSub(*args):
        return abs(args[0] - args[1])

    def kkMul(*args):
        product = 0
        for arg in args:
            product *= arg
        return product

    def kkDiv(*args):
        out = float(args[0] / args[1])
        if (out > 1):
            return out
        else:
            return 1 / out

    def kkAbs(*args):
        for arg in args:
            return abs(arg)

    ### initialize the kenken variables from board
    def initVar(self):
        rows = self.size[0]
        cols = self.size[1]

        domain = []
        for i in range(rows):
            domain.append(i + 1)

        for i in range(rows):
            for j in range(cols):
                self.board[i][j] = ConstraintVar(domain, self.board[i][j])
                self.variables.append(self.board[i][j])

    ### Generate constraints of puzzles according to input requirements
    ### Add to the constraints list
    def generateConstraint(self):

        # add constraints for rows and columns being distinct
        rows = self.size[0]
        cols = self.size[1]
        i = 0
        for row in self.board:
            j = 0
            for var in row:
                for a in range(rows):
                    for b in range(cols):
                        if a == i and b == j:
                            continue
                        if not (a == i or b == j):
                            continue
                        var2 = self.board[a][b]
                        self.constraints.append(BinaryConstraint(var, var2, lambda x, y: x != y))
                j += 1
            i += 1

        for i in range(len(self.constraintArr)):
            if (len(self.constraintArr[i]) == 2):
                value = self.constraintArr[i][0]
                cord = self.constraintArr[i][1]
                # self.variables.append(cord)
                self.constraints.append(UnaryConstraint(self.board[cord[0]][cord[1]], lambda x: x == value))

            elif (len(self.constraintArr[i]) == 3):
                op = self.constraintArr[i][0]
                value = self.constraintArr[i][1]
                cord = self.constraintArr[i][2]

                # self.variables.append(cord)
                self.constraints.append(UnaryConstraint(self.board[cord[0]][cord[1]], lambda x: x == value))

            ###### NEED TO HANDLE OPERATERS WITH MORE THAN TWO VARIABLES #####

            elif (len(self.constraintArr[i]) == 4):
                op = self.constraintArr[i][0]
                value = self.constraintArr[i][1]
                cord1 = self.constraintArr[i][2]
                cord2 = self.constraintArr[i][3]

                # self.variables.append(cord1)
                # self.variables.append(cord2)

                if op == "+":
                    self.constraints.append(
                        BinaryConstraint(self.board[cord1[0]][cord1[1]], self.board[cord2[0]][cord2[1]],
                                         create_add(value)))
                    self.constraints.append(
                        BinaryConstraint(self.board[cord2[0]][cord2[1]], self.board[cord1[0]][cord1[1]],
                                         create_add(value)))

                if op == "-":
                    self.constraints.append(
                        BinaryConstraint(self.board[cord1[0]][cord1[1]], self.board[cord2[0]][cord2[1]],
                                         create_sub(value)))
                    self.constraints.append(
                        BinaryConstraint(self.board[cord2[0]][cord2[1]], self.board[cord1[0]][cord1[1]],
                                         create_sub(value)))
                if op == "*":
                    self.constraints.append(
                        BinaryConstraint(self.board[cord1[0]][cord1[1]], self.board[cord2[0]][cord2[1]],
                                         create_mult(value)))
                    self.constraints.append(
                        BinaryConstraint(self.board[cord2[0]][cord2[1]], self.board[cord1[0]][cord1[1]],
                                         create_mult(value)))
                if op == "/":
                    self.constraints.append(
                        BinaryConstraint(self.board[cord1[0]][cord1[1]], self.board[cord2[0]][cord2[1]],
                                         create_div(value)))
                    self.constraints.append(
                        BinaryConstraint(self.board[cord2[0]][cord2[1]], self.board[cord1[0]][cord1[1]],
                                         create_div(value)))

            elif (len(self.constraintArr[i]) >= 5):
                op = self.constraintArr[i][0]
                value = self.constraintArr[i][1]
                coords = self.constraintArr[i][2:]
                if op == "+":
                    self.nConstraint(sum, value, coords)
                if op == "*":
                    self.nConstraint(mult_sum, value, coords)

                    # def generateBacktracking(self):

    def nConstraint(self, fn, value, coords):
        temp = ConstraintVar([], None)
        coord_domains = []
        i = 0
        for coord in coords:
            var = self.board[coord[0]][coord[1]]
            coord_domains.append(var.domain)
            fns = create_equal(i)
            self.constraints.append(BinaryConstraint(var, temp, fns[0]))
            self.constraints.append(BinaryConstraint(temp, var, fns[1]))
            i += 1
        domain = set(itertools.product(*coord_domains))
        to_remove = set()
        for a in domain:
            if fn(a) != value:
                to_remove.add(a)
        temp.domain = list(domain - to_remove)
        self.variables.append(temp)

    def generateBoard(self):
        out = [[None for i in range(self.size[1])] for j in range(self.size[0])]
        i = 0
        for row in self.board:
            j = 0
            for var in row:
                if len(var.domain) != 1:
                    print("No sltn")
                    return None
                else:
                    out[i][j] = var.domain[0]
                j += 1
        return out


def mult_sum(ls):
    out = 1
    for n in ls:
        out *= n
    return out


def create_add(val):
    return (lambda x, y: x + y == val)


def create_sub(val):
    return (lambda x, y: abs(x - y) == val)


def create_mult(val):
    return (lambda x, y: x * y == val)


def create_div(val):
    return (lambda x, y: (val * x == y) or (val * y == x))


def create_equal(i):
    return (lambda x, y: x == y[i]), (lambda x, y: x[i] == y)