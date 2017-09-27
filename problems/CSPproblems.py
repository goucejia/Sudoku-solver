class ConstraintVar:
    # instantiation example: ConstraintVar( [1,2,3],'A1' )
    # MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__(self, d, n):
        self.domain = [v for v in d]
        self.name = n
        self.neighbors = set()  # changed to set and gets modified in BinaryConstraint


class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__(self, v, fn):
        self.type = "Unary"
        self.var = v
        self.func = fn


class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, fn):
        self.type = "Binary"
        self.var1 = v1
        self.var2 = v2
        self.func = fn
        v1.neighbors.add(v2)
        v2.neighbors.add(v1)

# class TripleConstraint:
#     # constrant with 3 variables
#     def __init__(self, v1, v2, v3, fn):
#         self.var1 = v1
#         self.var2 = v2
#         self.var3 = v3
#         self.func = fn
#         v1.neighbors.add(v2)
#         v1.neighbors.add(v3)
#         v2.neighbors.add(v1)
#         v2.neighbors.add(v3)
#         v3.neighbors.add(v1)
#         v3.neighbors.add(v2)

def allDiff(constraints, v ):
	# generate a list of constraints that implement the allDiff constraint for all variable combinations in v
	# constraints is a preconstructed list. v is a list of ConstraintVar instances.
	# call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in v:
        for j in v:
            if ( i != j ) :
                constraints.append(BinaryConstraint( i,j,fn ))
