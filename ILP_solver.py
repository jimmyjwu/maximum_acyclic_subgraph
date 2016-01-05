from gurobipy import *
import networkx

def all_pairs_of_nodes(graph):
	return [(i,j) for i in graph.nodes_iter() for j in graph.nodes_iter() if i != j]

def all_triples_of_nodes(graph):
	return [(i,j,k) for i in graph.nodes_iter() for j in graph.nodes_iter() for k in graph.nodes_iter() if (i != j and j != k and i != k)]


def solve_MAS_instance(graph):
	"""
	Given a directed graph, computes the linearization of its nodes that maximizes the number of forward edges.
	"""
	# MODEL SETUP
	model = Model('maximum_acyclic_subgraph')

	# Create variables x_{ij}
	X = {}
	for i,j in all_pairs_of_nodes(graph):
		X[i,j] = model.addVar(vtype=GRB.BINARY, name='X_%s_%s' % (i,j))

	model.update()

	# Create coefficients c_{ij}
	C = {}
	for i,j in all_pairs_of_nodes(graph):
		C[i,j] = int(graph.has_edge(i,j))


	# CONSTRAINTS
	for i,j in all_pairs_of_nodes(graph):
		model.addConstr(X[i,j] + X[j,i] == 1)

	for i,j,k in all_triples_of_nodes(graph):
		model.addConstr(X[i,j] + X[j,k] + X[k,i] <= 2)

	# OBJECTIVE
	objective_expression = quicksum( C[i,j] * X[i,j] for i,j in all_pairs_of_nodes(graph) )
	model.setObjective(objective_expression, GRB.MAXIMIZE)


	# SOLVE AND RECOVER SOLUTION
	model.optimize()





