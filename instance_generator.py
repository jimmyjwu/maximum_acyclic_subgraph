from generation import *
from ILP_solver import *


def graph_to_string(graph, filename='instance.in'):
	# First line: number of nodes
	instance_string = str(graph.number_of_nodes()) + '\n'

	# Build the adjacency matrix
	rows = []
	for u in graph.nodes_iter():
		current_row = []
		for v in graph.nodes_iter():
			if graph.has_edge(u,v):
				current_row += ['1']
			else:
				current_row += ['0']
		rows += [ ' '.join(current_row) ]
	instance_string += '\n'.join(rows)

	return instance_string


def write_string_to_file(string, file_number, directory_path_name='instructor_instances/'):
	with open( directory_path_name + str(file_number) + ".in", 'w') as f:
		f.write(string)


def write_graph_to_file(graph, file_number):
	write_string_to_file(graph_to_string(graph), file_number)


def write_graphs_to_files(graphs):
	for i, graph in enumerate(graphs):
		write_graph_to_file(graph, i)


if __name__ == "__main__":

	planted_percentage_values = [0.6, 0.7, 0.8, 0.9]
	density_values = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8]
	instance_count = 100
	
	graphs = []
	for _ in xrange( int(instance_count / (len(planted_percentage_values) * len(density_values)) / 2) ): # How many times to loop through random parameter pairs
		for planted_percentage in planted_percentage_values:
			for density in density_values:
				print 'GENERATING DIRECTED ERDOS-RENYI INSTANCE WITH OPT >= %s, DENSITY %s' % (planted_percentage, density)
				graphs += [ create_sample_MAS_instance(optimum_lower_bound=planted_percentage, density=density) ]
				
				print 'GENERATING UGC-HARD INSTANCE WITH OPT >= %s, DENSITY %s' % (planted_percentage, density)
				graphs += [ create_UGC_hard_MAS_instance(optimum_lower_bound=planted_percentage, density=density) ]

	write_graphs_to_files(graphs)



