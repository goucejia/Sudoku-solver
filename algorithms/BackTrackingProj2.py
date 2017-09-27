from collections import deque
from sets import Set



class Backtracking:
    def __init__(self, problem):
        self.problem = problem
        self.variables = problem.variables
        self.constraints = deque(problem.constraints)
        self.solved = False
        self.assignment = {}



    def backtrack(self, constraints, variables, assignment):
        if completeness(assignment):
            return assignment
        consistent = True;
        for var in variables:
            for val in var:
                for constrant in constrants:
                    if type(constraint) == UnaryConstraint:
                        if constraint.var == var:
                            consistent = False
                if res:
                    constraints.append(UnaryConstraint(var, lambda x: x == value))
                    assignment[var] = value
                inference = inferenceFunc(var, assignment, constraint)
                if inference != "failure":
                    #assignment.append(inference)
                    constraints.append(UnaryConstraint(var, lambda x: #inference))
                    result = backtrack(constraints, variables, assignment)
                    if result != "failure":
                        return result
        constraints.remove(UnaryConstraint(var, lambda x: x == value))
        del assignment[var]
        return "failure"


    @staticmethod
    def inference(csp, var, assignment, constraints):
        if not checkConsistant:
            return False
        return False

    def checkConsistant(self, constraints):
        collectV = set()
        for each in constraints:
            if type(constraint) == UnaryConstraint:
                if constraint in collectV:
                    return False
                else:
                    collect.add(constraint)
        return True

    def solve(self):
        return backtrack(self.constrants, self.vars)

    def print(self):
        self.problem.print(self.vars)

    def completeness(self, assignment):
        assignment = Set()
        if len(assignment.keys()) == len(problem.size ** 2):
            return True
        return False
