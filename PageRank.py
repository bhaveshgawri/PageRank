import math
import numpy as np


class PageRank:
	"""PageRank of pages visualized as a graph.

	Contains function to calculate the rank of pages using the Google's
	PageRank Algorithm. The set of web-pages is visulaized as a directed
	graph where a directed edge between pages denotes a hyperlink from a
	parent page to its child.

	...

	Parameters
	----------
	beta : float
		Probability with which teleport will occur
	edges : collections.defaltdict(list)
		Adjacency list containing information connections in web-graph
	epsilon : float
		A small value and total error in ranks should be less than epsilon
	max_iterations : int
		Maximum number of times to apply power iteration
	node_num : int
		Number of nodes in the web-graph

	order : {'beta', 'edges', 'epsilon', 'max_iterations', 'node_num'}
		Order of parameters follows precisely this order.
		None of the parameter is optional.

	Methods
	-------
	pageRank()
		Calculate PageRank of all nodes in the web-graph

	"""
	
	def __init__(self, beta, edges, epsilon, max_iterations, node_num):
		self.beta = beta
		self.edges = edges
		self.epsilon = epsilon
		self.node_num = node_num
		self.MAX_ITERATIONS = max_iterations


	def pageRank(self):
		"""PageRank of all nodes in the web-graph

		Parameters
		----------
		None

		Returns
		-------
		final_rank_vector : numpy.ndarray
			dtype : float
			1-dimensional numpy array with size as number of nodes in web-graph
			Contains rank of each node in the web-graph

		"""
		final_rank_vector = np.zeros(self.node_num)
		initial_rank_vector = np.fromiter(
			[1 / self.node_num for _ in range(self.node_num)], dtype='float')
		
		iterations = 0
		diff = math.inf
		
		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank_vector = np.zeros(self.node_num)
			for parent in self.edges:
				for child in self.edges[parent]:
					new_rank_vector[child] += (initial_rank_vector[parent] /
					len(self.edges[parent]))

			leaked_rank = (1-sum(new_rank_vector))/self.node_num
			final_rank_vector = new_rank_vector + leaked_rank
			diff = sum(abs(final_rank_vector - initial_rank_vector))
			initial_rank_vector = final_rank_vector
			iterations += 1
			print("PageRank iteration: " + str(iterations))

		return final_rank_vector