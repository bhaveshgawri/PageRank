import math
import heapq
import numpy as np
from scipy.sparse import csr_matrix as SparseMatrix


class TopicSpecificRank:
	"""Similar to PageRank but the teleport set is a subset(related topics)
	of all nodes.

	...
	
	Parameters
	----------
	
	beta : float
		Probability with which teleports will occur
	
	edges : collections.defaltdict(list)
		Adjacency list containing information connections in web-graph
	
	epsilon : float
		A small value and total error in ranks should be less than epsilon
	
	max_iterations : int
		Maximum number of times to apply power iteration
	
	node_num : int
		Number of nodes in the web-graph
	
	PageRank_vector : numpy.ndarray  [1-dimensional, dtype=float]
		Contains PageRank of each node in the web-graph

	
	order : {'beta', 'edges', 'epsilon', 'max_iterations', 'node_num', 
	'PageRank_vector'}
		Parameters follows precisely the above order.
		None of the parameter is optional.

	
	Methods
	-------
	get_similarTopicPages()
		Classifies topics pages in different classes.

	matrix_get_initailRankMatrix()
		Initailises the topicSpecificRank Matrix.

	matrix_get_topicSpecificGoogleMatrix()
		Creates the Google Matrix which is used in power iteration.

	matrix_get_topicSpecificRank()
		Applies power iteration on Google Matrix and Initial Rank Matrix 
		to get TopicSpecificRank Matrix.

	list_get_topicSpecificRank()
		Alternative method for power iteration which used much less RAM.

	topicSpecificRank()
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


	def get_similarTopicPages(self):
		"""Classifies topics pages in different classes.

		[INCOMPLETE] Write your own implementation to classify pages into
		topics.
		
		...
		
		Parameters
		----------
		None
		[May add more if required.]

		
		Returns
		-------
		lol_of_topic_pages : list of list of int
			Each inner list contains the related pages.
			Each page belongs to only one inner list.
			Outer list contains all such inner lists.
		"""
		pass


	def matrix_get_initailRankMatrix(self):
		"""Initailises the topicSpecificRank Matrix.

		
		Parameters
		----------
		None

		
		Returns
		-------
		initial_rank_vector : scipy.sparse.csr_matrix [shape = (n x 1), 
			n is `node_num`]
			Ranks are distributed equally among all pages, initially.

		"""
		initial_rank_list = [1/(self.node_num) for i in range(self.node_num)]
		initial_rank_vector = SparseMatrix(np.matrix(initial_rank_list).
			transpose())
		return initial_rank_vector

	
	def matrix_get_topicSpecificGoogleMatrix(self, related_pages):
		"""Creates the Google Matrix which is used in power iteration.

		
		Parameters
		----------
		related_pages : list of int
			Contains list of pages which belong to the same topic.

		
		Returns
		-------
		google_matrix : scipy.sparse.csr_matrix [shape = (n x n), n is 
						`node_num`]
			It contains proportion of rank that will propagate from a 
			page to another page.
			Proportion of rank depends on degree of node and leaked rank.
		"""
		related_set_size = len(related_pages)

		teleport_matrix_row = []
		teleport_matrix_col = []
		teleport_matrix_data = []

		for related_node in related_pages:
			for node in range(self.node_num):
				teleport_matrix_col.append(node)
				teleport_matrix_row.append(related_node)
				teleport_matrix_data.append(
					(1 - self.beta) / related_set_size)
		
		teleport_matrix = SparseMatrix((teleport_matrix_data, (
			teleport_matrix_row, teleport_matrix_col)), shape = (self.node_num,
				self.node_num))

		connection_matrix_row = []
		connection_matrix_col = []
		connection_matrix_data = []

		for parent_node in range(self.node_num):
			for child_node in self.edges[parent_node]:
				connection_matrix_col.append(parent_node)
				connection_matrix_row.append(child_node)
				connection_matrix_data.append(
					self.beta / (len(self.edges[parent_node])))
		
		connection_matrix = SparseMatrix((connection_matrix_data, (
			connection_matrix_row, connection_matrix_col)), shape = (self.
			node_num, self.node_num))

		google_matrix = connection_matrix + teleport_matrix
		return google_matrix	


	def matrix_get_topicSpecificRank(self, teleport_set, initial_rank_vector, 
		google_matrix):
		"""Calculates TopicSpecificRank of each node taking some related_pages 
		as `teleport_set`.

		This method works by applying power iteration until convergence
		or till iterations reach `MAX_ITERATIONS`, whichever happens first.
		
		[USAGE WARNING] : If graph is large, then sparse matrix may become
			huge and use up the entire RAM(which is not a condition to be in).
		...

		Parameters
		----------
		teleport_set : list of int
			List of pages to which a random walker in the web-graph can 
			teleport to.
			In TopicSpecificRank this set corresponds to pages of same topic.

		initial_rank_vector : scipy.sparse.csr_matrix [shape = (n x 1), 
			n is `node_num`]
			Ranks are distributed equally among all pages, initially.

		google_matrix : scipy.sparse.csr_matrix [shape = (n x n), n is 
						`node_num`]
			It contains proportion of rank that will propagate from a 
			page to another page.


		Returns
		-------
		final_rank_vector : scipy.sparse.csr_matrix [shape = (n x 1), 
			n is `node_num`]
			Contains TopicSpecificRank of each node in the web-graph.

		"""
		iterations = 0
		diff = math.inf
		teleport_set_size = len(teleport_set)
		final_rank_vector = SparseMatrix(np.zeros(self.node_num).transpose())

		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank_vector = google_matrix * initial_rank_vector

			leaked_rank = (1-SparseMatrix.sum(new_rank_vector))/
				teleport_set_size
			leaked_rank_vector = SparseMatrix(np.array([leaked_rank if node in
				teleport_set else 0 for node in range(self.node_num)])).
				transpose()
			
			final_rank_vector = new_rank_vector + leaked_rank_vector
			diff = SparseMatrix.sum(
				abs(final_rank_vector - initial_rank_vector))
			
			initial_rank_vector = final_rank_vector
			iterations += 1
			print("At iteration: " + str(iterations))

		return final_rank_vector


	def list_get_topicSpecificRank(self, teleport_set):
		"""Calculates TopicSpecificRank of each node taking some related
		pages as `teleport_set`. Related Pages belong to same topic.


		Parameters
		----------
		teleport_set : list of int
			List of pages to which a random walker in the web-graph can 
			teleport to.
			In TopicSpecificRank this set corresponds to pages of same topic.

		
		Returns
		-------
		final_rank_vector : numpy.ndarray  [1-dimensional, dtype=float]
			Contains TopicSpecificRank of each node in the web-graph.

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
					new_rank_vector[child] += initial_rank_vector[parent] /
						len(self.edges[parent])

			leaked_rank = (1 - sum(new_rank_vector)) / teleport_set_size
			leaked_rank_vector = np.array([leaked_rank if node in teleport_set 
				else 0 for node in range(self.node_num)])
			
			final_rank_vector = new_rank_vector + leaked_rank_vector
			diff = sum(abs(final_rank_vector - initial_rank_vector))
			initial_rank_vector = final_rank_vector
			
			iterations += 1
			print("At iteration: " + str(iterations))

		return final_rank_vector


	def topicSpecificRank(self):
		"""Utility function which calls other functions in a specific order.

		
		Parameters
		----------
		None

		
		Returns
		-------
		[Assumption: list_get_topicSpecificRank is used instead of 
		matrix_get_topicSpecificRank]

		dict_of_rank_vectors : dict of int and numpy.ndarray 
			[1-dimensional, dtype=float]
			Example: 
				{
					int: ndarray, 
					int: ndarray,
					int: ndarray,
					...
				}
			int is the topic number
			ndarray has rank of pages in the web-graph wrt that topic.  
		"""
		lol_of_topic_pages = self.matrix_get_similarTopicPages()
		list_of_rank_vectors = {}
		
		for topic in lol_of_topic_pages:
			## approach 1 :: uses adjacency list to calc. rank
			topicSpecificRank_vector = list_get_topicSpecificRank(topic)
			
			## approach 2: RAM eater :: uses SparseMatrices to calc. rank
			# initialRank_vector = self.matrix_get_initailRankMatrix()
			# google_matrix = self.matrix_get_topicSpecificGoogleMatrix(
			# topic)
			# topicSpecificRank_vector = self.matrix_get_topicSpecificRank(
			# topic, initialRank_vector, google_matrix)
		
			list_of_rank_vectors[topic] = topicSpecificRank_vector
			# can append topic number instead of topic(list)^^
			# create a function to map topic with topic_number
		return list_of_rank_vectors