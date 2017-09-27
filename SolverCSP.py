import sys, os

sys.path.append(os.path.realpath('..') + '/class-repo/projectClasses')
sys.path.append(os.path.realpath('.') + '/algorithms')
sys.path.append(os.path.realpath('.') + '/problems')

import CSPclasses
from AC3 import *
from futoshiki import *
from kenken import *

# _______________________________________________________________________
# PROVIDE the following for Puzzle and Algorithm Implementation:
#         THE INFORMATION BELOW REGARDING AUTHORSHIP AND IMPLEMENTATION STATUS IS REQUIRED
#         Your team can collectively create implementation classes here or in separate files
#         Make sure that paths are set properly.
# _______________________________________________________________________

### PUZZLES
##       -- If anyone completed an extra puzzle, create an instance and set algo.bonus = True


# >>>>>>> APPEND TO THIS LIST with puzzle implementation instances
puzzlesImplemented = [CSPclasses.PuzzleType.kenken, CSPclasses.PuzzleType.futoshiki]

ken = CSPclasses.PuzzleImplementation(CSPclasses.PuzzleType.kenken)
ken.authors = ['treul004', 'fangx174']
ken.status = CSPclasses.StatusType.Buggy
puzzlesImplemented.append(ken)

futo = CSPclasses.PuzzleImplementation(CSPclasses.PuzzleType.futoshiki)
futo.authors = ['lixx2999', 'songx544']
futo.status = CSPclasses.StatusType.Complete
puzzlesImplemented.append(futo)

#### ALGORITHMS
##        -- AC3 and Backtracking are required parts of this assignment
##        -- Please create a class instance for each type of backtracking (with mac and forward-checking)
##        -- Create an additional class for any variable or value ordering implentation
##
##  IF your team produced multiple versions, please create a separate instance for each implementation


# >>>>>>> APPEND TO THIS LIST with algorithm implementation instances
algosImplemented = [CSPclasses.AlgoType.AC3]

ac3imp = CSPclasses.AlgoImplementation(CSPclasses.AlgoType.AC3)
ac3imp.authors = ['treul004', 'fangx174']
ac3imp.status = CSPclasses.StatusType.Buggy
algosImplemented.append(ac3imp)


backMac = CSPclasses.AlgoImplementation(CSPclasses.AlgoType.backtrackMAC)
backMac.authors = ['lixx2999', 'songx544']
backMac.status = CSPclasses.StatusType.Buggy
algosImplemented.append(backMac)

backFC = CSPclasses.AlgoImplementation(CSPclasses.AlgoType.backtrackFC)
backFC.authors = ['lixx2999', 'songx544']
backFC.status = CSPclasses.StatusType.Buggy
algosImplemented.append(backFC)

# Here is how you would test 2 different implementations of the same algorithm
# back2 = CSPclasses.AlgoImplementation(CSPclasses.AlgoType.backtrackMAC)
# ...
#
# deg = CSPclasses.AlgoImplementation(CSPclasses.AlgoType.degreeHeuristic)
# deg.authors = None
# deg.status = CSPclasses.StatusType.NotSelected
# deg.bonus = True
# algosImplemented.append(deg)


def SolverCSP(puzzle, algorithm):
    # puzzle is of type CSPclasses.InputPuzzleClass
    # algorithm is of type CSPclasses.AlgoImplementation
    #
    # RETURN a class instance that has methods solve() and printSolution() with member solution

    # FILL THIS IN such that a grading script can be called that will ...

    if puzzle.pType == CSPclasses.PuzzleType.kenken:
        p = kenkenPuzzle(puzzle.size, puzzle.puzzle)
    elif puzzle.pType == CSPclasses.PuzzleType.futoshiki:
        p = futoshikiPuzzle(puzzle.size, puzzle.puzzle)
    else:
        print("Puzzle not recognized")
        return None

    if algorithm == CSPclasses.AlgoType.AC3:
        return AC3(p)
    else:
        print("Algorithm not recognized")
        return None


# solver = SolverCSP(
#     CSPclasses.InputPuzzleClass(
#         [3, 3],
#         [['*', 6, [0, 0], [1, 0]],
#          ['-', 1, [0, 1], [0, 2]],
#          ['+', 7, [1, 1], [1, 2], [2, 2]],
#          ['-', 1, [2, 0], [2, 1]]],
#         CSPclasses.PuzzleType.kenken,
#         [[3, 1, 2], [2, 3, 1], [1, 2, 3]]
#     ),
#     CSPclasses.AlgoType.AC3
# )
#
# solver.solve()
# solver.printSolution()

# f1 = CSPclasses.InputPuzzleClass(
#  [4,4],
#  [[3,[2,0]],
#   [1,[2,1]],
#   [1,[3,3]],
#   ['>',[1,1],[1,2]],
#   ['>',[1,2],[2,2]]
#   ],
#  CSPclasses.PuzzleType.futoshiki,
#  [[4,2,1,3],
#   [1,4,3,2],
#   [3,1,2,4],
#   [2,3,4,1]] )

# solver = SolverCSP(f1, CSPclasses.AlgoType.AC3)
# solver.solve()
# solver.printSolution()