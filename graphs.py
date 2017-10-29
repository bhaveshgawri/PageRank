from collections import defaultdict


class getGraph:
	"""Converts edges from text file to adjacenct list.
	...

	Parameters
	----------
	edge_file : string
		Path to the file where edges of web-graph are stored.

	
	Methods
	-------
	get_connections()
		Reads the edges from the edge_file and save it in adjacency list on 
		RAM.

	"""
	def __init__(self, edge_file):
		self.edge_file = edge_file

	def get_connections(self):
		"""Reads the edges from the edge_file and save it in adjacency list on 
		RAM.

		Parameters
		----------
		None

		
		Returns
		-------
		edges : collections.defaltdict(list)
			Adjacency list containing information of connections in web-graph.

		"""
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
	"""Plots the web-graph, graphically on the screen.

	...

	Parameters
	----------
	None

	
	Methods
	-------
	None

	"""
	def __init__(self):
		pass