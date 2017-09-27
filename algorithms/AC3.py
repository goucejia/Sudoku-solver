from collections import deque


class AC3:
    def __init__(self, problem):
        self.problem = problem
        self.vars = problem.variables
        self.constraints = deque(problem.constraints)
        self.solution = None

    @staticmethod
    def revise(bc):
        # The revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
        # A single BinaryConstraint instance is passed in to this function.

        revised = False
        dom1 = list(bc.var1.domain)
        dom2 = list(bc.var2.domain)

        for x in dom1:
            sat = False
            for y in dom2:
                if bc.func(x, y):
                    sat = True
            if not sat:
                bc.var1.domain.remove(x)
                revised = True
        return revised

    def find_constraints(self, var1, var2):
        # returns list of all constraints with var1 var2
        out = []
        for constraint in self.constraints:
            if (constraint.var1 == var1 and constraint.var2 == var2) or (
                            constraint.var1 == var2 and constraint.var2 == var1):
                out.append(constraint)
        return out

    def solve(self):
        while len(self.constraints) > 0:
            current = self.constraints.popleft()
            if AC3.revise(current):
                if len(current.var1.domain) == 0:
                    # no solution
                    return False
                for var in (current.var1.neighbors - {current.var2}):
                    constraints = self.find_constraints(var, current.var1)
                    for constraint in constraints:
                        self.constraints.append(constraint)
        self.problem.variables = self.vars
        return True

    def printSolution(self):
        print(self.problem.generateBoard())