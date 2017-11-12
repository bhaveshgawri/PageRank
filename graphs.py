import heapq
import networkx as nx
import matplotlib.pyplot as plt
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
	edges : collections.defaltdict(list)
		Adjacency list containing information of connections in web-graph.
	
	interval : int, optional
		Time in milli-seconds for which graph is shown on screen
		Default value: 5000
	
	
	Methods
	-------
	get_KMaxRankNodes(number_of_nodes, rank_vector)
		Calculates and Returns `number_of_nodes` with highest value in `rank_vector`.

	get_edgesConnectedToTopK(rank_vector, topK, ranks)
		Calculates and Return the list of child nodes of the top `k` nodes.

	get_EdgesToDrawWithRanks(drawing_list, ranks)
		Returns list of edges and rank of nodes to be shown on graph.

	draw(edge_list, nodes_to_draw)
		Draws the directed-graph on the screen with size of node equivalent to rank of nodes.

	plot(number_of_nodes, rank_vector)
		Utility function which calls other functions in appropriate order to plot the graph.

	"""
	def __init__(self, edges, interval=5000):
		self.edges = edges
		self.interval = interval


	def get_KMaxRankNodes(self, number_of_nodes, rank_vector):
		"""Calculates and Returns `number_of_nodes` with highest value in `rank_vector`.

		
		Parameters
		----------
		number_of_nodes : int
			Contains the number of nodes to be picked.

		rank_vector	: numpy.ndarray [1-dimensional, dtype=float]
			Contains PageRank of each node in the web-graph.

		
		Returns
		-------
		topK : list of tuple [(int, double), (int, double), ...]
			Contain node and rank of top `number_of_nodes`. 

		"""
		heaped_ranks = [(rank, node) for (node, rank) in 
			enumerate(rank_vector)]
		heapq._heapify_max(heaped_ranks)
		topK = [heapq._heappop_max(heaped_ranks)
			for _ in range(number_of_nodes)]

		return topK


	def get_edgesConnectedToTopK(self, rank_vector, topK, ranks):
		"""Calculates and Return the list of child nodes of the top `k` nodes.


		Parameters
		----------
		rank_vector	: numpy.ndarray [1-dimensional, dtype=float]
			Contains PageRank of each node in the web-graph.

		topK : list of tuple [(int, double), (int, double), ...]
			Contain node and rank of top `number_of_nodes`. 

		ranks : dict {int: double, int: double}
			Contains rank of the nodes int the web-graph.

		
		Returns
		-------
		weighted_edges : defaultdict(list) 
			{
				(int, double): [(int, double), (int, double), ...],
				(int, double): [(int, double), (int, double), ...],
				(int, double): [(int, double), (int, double), ...],
				... 
			}
			(int, double) : (node: rank) 
			Here node belongs to the list of nodes with top k ranks.
			Contains top `k` nodes with their childs in list.

		"""
		weighed_edges = defaultdict(list)
		
		for couple in topK:
			weighed_edges[(couple[1], couple[0])] = [(node, ranks[node]) 
				for node in self.edges[couple[1]]]

		return weighed_edges


	def get_EdgesToDrawWithRanks(self, drawing_list, ranks):
		"""Returns list of edges and rank of nodes to be shown on graph.

		
		Parameters
		----------
		drawing_list : defaultdict(list)
		{
			(int, double): [(int, double), (int, double), ...],
			(int, double): [(int, double), (int, double), ...],
			(int, double): [(int, double), (int, double), ...],
			... 
		}
		(int, double) : (node: rank) 
		Here node belongs to the list of nodes with top k ranks.
		Contains top `k` nodes with their childs in list.

		ranks : dict {int: double, int: double}
			Contains rank of the nodes int the web-graph.

		
		Returns
		-------
		edge_list : list of tuple [(int, int), (int, int), ...]
			(int, int) : (node1, node2)
			Symbolizes directed edges from node1 to node2.

		nodes_to_draw : list of tuple [(int, double), (int, double), ...]
			(int, double) : (node, rank)
			Node belongs to a set of nodes to be drawn on the graph.

		"""
		edge_list=[]
		to_draw_node_set = set();
		for (node, rank) in drawing_list:
			to_draw_node_set.add(node)
			for child in drawing_list[(node, rank)]:
				to_draw_node_set.add(child[0])
				edge_list.append((node, child[0]))

		nodes_to_draw = [(node, ranks[node]) for node in to_draw_node_set]
		return (edge_list, nodes_to_draw)

	
	def draw(self, edge_list, nodes_to_draw):
		"""Draws the directed-graph on the screen with size of node equivalent to rank of nodes.


		Parameters
		----------
		edge_list : list of tuple [(int, int), (int, int), ...]
			(int, int) : (node1, node2)
			Symbolizes directed edges from node1 to node2.

		nodes_to_draw : list of tuple [(int, double), (int, double), ...]
			(int, double) : (node, rank)
			Node belongs to a set of nodes to be drawn on the graph.

		
		Returns
		-------
		None

		"""
		Graph = nx.DiGraph()
		Graph.add_edges_from(sorted(edge_list))
		print(sorted(edge_list))
		
		fig = plt.figure()
		timer = fig.canvas.new_timer(self.interval)
		timer.add_callback(plt.close)

		# pos = nx.spring_layout(Graph)
		pos = nx.shell_layout(Graph)
		nx.draw_networkx_nodes(Graph, 
				pos, 
				cmap=plt.get_cmap('jet'), 
				node_size=[node[1]*10000 for node in nodes_to_draw])
		nx.draw_networkx_labels(Graph, pos, labels={node[0]: node[0] for node in nodes_to_draw})
		nx.draw_networkx_edges(Graph, pos, arrows=True)
		timer.start()
		plt.show()

	
	def plot(self, number_of_nodes, rank_vector):
		"""Utility function which calls other functions in appropriate order to plot the graph.

		Parameters
		----------
		number_of_nodes : int
			Contains the number of nodes to be picked.

		rank_vector	: numpy.ndarray [1-dimensional, dtype=float]
			Contains PageRank of each node in the web-graph.

		Returns
		-------
		None	
	
		"""
		ranks = {node: rank for (node, rank) in enumerate(rank_vector)}
		topK = self.get_KMaxRankNodes(number_of_nodes, rank_vector)
		drawing_list = self.get_edgesConnectedToTopK(rank_vector, topK, ranks)
		(edge_list, nodes_to_draw) = self.get_EdgesToDrawWithRanks(
														drawing_list, ranks)
		self.draw(edge_list, nodes_to_draw)