import networkx
import random

def coin_flip(probability_1=0.5):
    return 1 if random.random() < probability_1 else 0


def permute_graph(graph):
	# Create new graph with vertices permuted (to obfuscate planted solution)
	permuted_nodes = graph.nodes() # New copy of nodes
	random.shuffle(permuted_nodes)
	permuted_graph = networkx.DiGraph()
	permutation = {original_node: permuted_node for (original_node, permuted_node) in zip(graph.nodes_iter(), permuted_nodes)}
	for u,v in graph.edges_iter():
		permuted_graph.add_edge(permutation[u], permutation[v])

	return permuted_graph



def create_sample_MAS_instance(node_count=100, optimum_lower_bound=0.8, density=0.4):
	"""
	Creates a directed graph, subject to the constraints:
		- Some solution must contain at at least (optimum_lower_bound)% of the edges.
		- The graph has density (density)
	"""
	
	# Create directed graph on nodes 1,...,node_count
	graph = networkx.DiGraph()
	graph.add_nodes_from(xrange(1, node_count+1))

	# Generate all possible directed edges, forward and backward
	possible_forward_edges = [(u,v) for u in graph.nodes_iter() for v in graph.nodes_iter() if u < v]
	possible_backward_edges = [(u,v) for u in graph.nodes_iter() for v in graph.nodes_iter() if u > v]

	# Compute balance of forward and backward edges
	edge_count = density * node_count * (node_count - 1) / 2
	
	# Sample subsets of forward and backward edges
	chosen_forward_edges = random.sample(possible_forward_edges, int(optimum_lower_bound * edge_count))
	chosen_backward_edges = random.sample(possible_backward_edges, int( (1 - optimum_lower_bound) * edge_count ))
	graph.add_edges_from(chosen_forward_edges)
	graph.add_edges_from(chosen_backward_edges)

	return permute_graph(graph)



def create_UGC_hard_MAS_instance(node_count=100, optimum_lower_bound=0.8, density=0.4):
	"""
	Creates a directed graph as in create_sample_MAS_instance(), but embedding edges uniformly by interval length.
	"""
	# Create directed graph on nodes 1,...,node_count
	graph = networkx.DiGraph()
	graph.add_nodes_from(xrange(1, node_count+1))

	# Compute edge count
	edge_count = density * node_count * (node_count - 1) / 2

	# All possible edge interval lengths: 1,...,node_count-1
	interval_lengths = range(1, node_count)

	# How many edges will be of each interval length
	edges_per_interval_length = int( edge_count / len(interval_lengths) )

	# Generate edges of each interval length
	for interval_length in interval_lengths:
		# Edge of length k can start from nodes 1,...,n-k
		possible_starting_nodes = range(1, node_count - interval_length + 1)

		# Sample the allowed number of edges for this interval
		chosen_starting_nodes = random.sample(possible_starting_nodes, edges_per_interval_length) if edges_per_interval_length < len(possible_starting_nodes) else possible_starting_nodes

		# Embed edges as forward and backward edges with appropriate probabilities
		for starting_node in chosen_starting_nodes:
			if coin_flip(probability_1=optimum_lower_bound) == 1:
				graph.add_edge( starting_node, starting_node + interval_length ) # Add forward edge
			else:
				graph.add_edge( starting_node + interval_length, starting_node ) # Add backward edge

	return permute_graph(graph)






