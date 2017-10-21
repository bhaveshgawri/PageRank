import math
import heapq
import numpy as np
from scipy.sparse import csr_matrix as SparseMatrix


class TrustRank:
	"""Similar to PageRank but the teleport set is a set of trusted pages.

	Contains functions to calculate TrustRank of each node in the web-graph.
	Initially trust(rank) is divided into some specific(trusted) pages which
	is then propagated to other pages connected to them. Trust decreases as
	it goes away from a trusted page.

	...
	Parameters
	----------
	beta : float
		Probability with which teleports will occur.
	
	edges : collections.defaltdict(list)
		Adjacency list containing information connections in web-graph.
	
	epsilon : float
		A small value and total error in ranks should be less than epsilon.
	
	max_iterations : int
		Maximum number of times to apply power iteration.
	
	node_num : int
		Number of nodes in the web-graph.
	
	PageRank_vector : numpy.ndarray  [1-dimensional, dtype=float]
		Contains PageRank of each node in the web-graph.

	
	order : {'beta', 'edges', 'epsilon', 'max_iterations', 'node_num',
			'PageRank_vector'}
		Parameters follows precisely the above order.
		None of the parameter is optional.

	
	Methods
	-------
	get_trustedPages(node_number_threshold=100)
		Calculates and returns the set of trusted pages.

	get_topicSpecificRank(teleport_set)
		Calculates TrustRank of each node taking trusted set as `teleport_set`.
	
	trustRank()
		Utility function which call other functions and returns rank vector.

	"""
	def __init__(self, beta, edges, epsilon, max_iterations, node_num,
		PageRank_vector):
		self.beta = beta
		self.edges = edges
		self.epsilon = epsilon
		self.node_num = node_num
		self.PageRank_vector = PageRank_vector
		self.MAX_ITERATIONS = max_iterations

		
	def get_trustedPages(self, node_number_threshold=100):
		"""Calculates and returns the set of trusted pages.

		
		Parameters
		----------
		node_number_threshold : int, optional
			defines the size of trusted based on whether node_num is greated.
			or less than threshold
			Default value : 100

		
		Returns
		-------
		trusted_pages : list of int
			List of trusted pages identified by their node number.
			
		"""
		# set number of trusted pages
		if self.node_num < node_number_threshold:
			ratio = 0.2
		else:
			ratio = 0.0002
		trusted_set_size = int(math.ceil(self.node_num * ratio))
		
		# set and return trusted pages
		heaped_ranks = [(rank, node) for (node, rank) in 
			enumerate(self.PageRank_vector)]
		heapq._heapify_max(heaped_ranks)
		trusted_pages = [heapq._heappop_max(heaped_ranks)[1] 
			for _ in range(trusted_set_size)]
		
		return trusted_pages

	def get_topicSpecificRank(self, teleport_set):
		"""Calculates TrustRank of each node taking trusted set as 
		`teleport_set`.

		
		Parameters
		----------
		teleport_set : list of int
			List of pages to which a random walker in the web-graph can 
			teleport to.
			In TrustRank this set corresponds to trusted pages.

		
		Returns
		-------
		final_rank_vector : numpy.ndarray  [1-dimensional, dtype=float]
			Contains TrustRank of each node in the web-graph.

		"""
		diff = math.inf
		iterations = 0
		teleport_set_size = len(teleport_set)

		final_rank_vector = np.zeros(self.node_num)
		initial_rank_vector = np.fromiter(
			[1/teleport_set_size if node in teleport_set else 0 for node in
				range(self.node_num)], dtype='float')
		
		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank_vector = np.zeros(self.node_num)
			for parent in self.edges:
				for child in self.edges[parent]:
					new_rank_vector[child] += (initial_rank_vector[parent] /
						len(self.edges[parent]))

			leaked_rank = (1 - sum(new_rank_vector)) / teleport_set_size
			leaked_rank_vector = np.array([leaked_rank if node in teleport_set
				else 0 for node in range(self.node_num)])
			
			final_rank_vector = new_rank_vector + leaked_rank_vector
			diff = sum(abs(final_rank_vector - initial_rank_vector))
			initial_rank_vector = final_rank_vector
			
			iterations += 1
			print("TrustRank iteration: " + str(iterations))

		return final_rank_vector

	def trustRank(self):
		"""Utility function which calls other functions in a specific order.

		
		Parameters
		----------
		None

		
		Returns
		-------
		final_rank_vector : numpy.ndarray  [1-dimensional, dtype=float]
			Contains TrustRank of each node in the web-graph.
		
		"""
		trusted_pages = self.get_trustedPages()
		print("got seed set...")
		final_rank_vector = self.get_topicSpecificRank(trusted_pages)
		return final_rank_vector