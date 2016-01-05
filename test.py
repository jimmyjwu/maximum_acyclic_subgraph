from generation import *
from ILP_solver import *







if __name__ == "__main__":

	for OPT, density in [(0.6,0.2), (0.6,0.4), (0.6,0.6), (0.6,0.8)]:
		print 'SOLVING INSTANCE WITH OPT >= %s, DENSITY %s' % (OPT, density)
		graph = create_sample_MAS_instance(optimum_lower_bound=OPT, density=density)
		solve_MAS_instance(graph)
		print '\n\n\n\n'