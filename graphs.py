from collections import defaultdict


class getGraph:
	def __init__(self, edge_file):
		self.edge_file = edge_file

	def get_connections(self):
		edge_list = []
		edges = defaultdict(list)

		with open (self.edge_file, 'r') as e_file:
			edge_list = e_file.readlines()
		
		for edge in edge_list:
			from_, to_ = edge.split('\t')
			from_, to_ = int(from_), int(to_[:-1])
			edges[from_].append(to_)
		
		return edges


class plotGraph:
	def __init__(self):
		pass