import math
import heapq
import random
import numpy as np
from collections import defaultdict
from scipy.sparse import csr_matrix as SparseMatrix


class Ranker:
	def __init__(self, node_num, edge_file, beta=0.85, epsilon=1e-6, max_iterations=100):
		self.beta = beta
		self.edges = None
		self.edge_file = edge_file
		self.epsilon = epsilon
		self.node_num = node_num
		self.MAX_ITERATIONS = max_iterations
		self.rank = np.zeros(self.node_num)
		self.trusted_pages = []
		self.trusted_set_size = 0


	def get_connections(self):
		edge_list = []
		self.edges = defaultdict(list)

		with open (self.edge_file, 'r') as e_file:
			edge_list = e_file.readlines()
		
		for edge in edge_list:
			from_, to_ = edge.split('\t')
			from_, to_ = int(from_), int(to_[:-1])
			self.edges[from_].append(to_)
		
		print("adjacency list on RAM now...")
		# for edge in self.edges:
		# 	print(edge, self.edges[edge])


	def pagerank(self):
		old_rank = np.fromiter(
			[1/self.node_num for _ in range(self.node_num)],
			dtype='float'
		)

		iterations = 0
		diff = math.inf
		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank = np.zeros(self.node_num)
			for parent in self.edges:
				for child in self.edges[parent]:
					new_rank[child] += old_rank[parent]/len(self.edges[parent])

			leaked_rank = (1-sum(new_rank))/self.node_num
			self.rank = new_rank + leaked_rank
			diff = sum(abs(self.rank - old_rank))
			old_rank = self.rank
			iterations += 1
			# print("completed iteration "+str(iterations))
			# print(self.rank)
		# print(self.rank, sum(self.rank))


	def trustrank(self):
		def get_trustedPages(break_point=100):
			# set number of trusted pages
			if self.node_num < break_point:
				ratio = 0.1
			else:
				ratio = 0.01
			trusted_set_size = int(math.ceil(self.node_num * ratio))
			
			# set and return trusted pages
			sorted_ranks = [(rank, node) for (node, rank) in enumerate(self.rank)]
			heapq._heapify_max(sorted_ranks)
			trusted_pages = [heapq._heappop_max(sorted_ranks)[1] for _ in range(trusted_set_size)]
			
			return (trusted_set_size, trusted_pages)

		def get_topicSpecificGoogleMatrix(related_pages, related_set_size):
			
			teleport_matrix_row = []
			teleport_matrix_col = []
			teleport_matrix_data = []
			for related_node in related_pages:
				for node in range(self.node_num):
					teleport_matrix_col.append(node)
					teleport_matrix_row.append(related_node)
					teleport_matrix_data.append((1-self.beta)/related_set_size)
			
			teleport_matrix = SparseMatrix((teleport_matrix_data, (teleport_matrix_row, teleport_matrix_col)), shape = (self.node_num, self.node_num))
			# print(teleport_matrix)
			# print(teleport_matrix.todense())

			connection_matrix_row = []
			connection_matrix_col = []
			connection_matrix_data = []

			for parent_node in range(self.node_num):
				for child_node in self.edges[parent_node]:
					connection_matrix_col.append(parent_node)
					connection_matrix_row.append(child_node)
					connection_matrix_data.append(self.beta / (len(self.edges[parent_node])))
			
			connection_matrix = SparseMatrix((connection_matrix_data, (connection_matrix_row, connection_matrix_col)), shape = (self.node_num, self.node_num))
			# print(connection_matrix)
			# print(connection_matrix.todense())

			google_matrix = connection_matrix + teleport_matrix
			return google_matrix


		def get_topicSpecificRank(initial_rank, google_matrix, teleport_set_size, teleport_set):
			iterations = 0
			diff = math.inf
			rank_v = SparseMatrix(np.zeros(self.node_num).transpose())
			while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
				new_rank = google_matrix * initial_rank

				leaked_rank = (1-SparseMatrix.sum(new_rank))/teleport_set_size
				leaked_vector = SparseMatrix(np.array([leaked_rank if node in teleport_set else 0 for node in range(self.node_num)])).transpose()
				
				rank_v = new_rank + leaked_vector
				diff = SparseMatrix.sum(abs(rank_v - initial_rank))
				
				initial_rank = rank_v
				iterations += 1
				# print("completed iteration " + str(iterations))
				# print(rank_v)

			return rank_v


		self.trusted_set_size, self.trusted_pages = get_trustedPages()
		google_matrix = get_topicSpecificGoogleMatrix(self.trusted_pages, 
			self.trusted_set_size)
		initial_rank = [1/(self.node_num) for i in range(self.node_num)]
		initial_rank = SparseMatrix(np.matrix(initial_rank).transpose())
		rank_vector = get_topicSpecificRank(initial_rank, google_matrix, 
			self.trusted_set_size, self.trusted_pages)
		print(rank_vector)
		# return rank_vector


if __name__ == '__main__':
	r = Ranker(9, './data/test', max_iterations=10)
	r.get_connections()
	r.pagerank()
	r.trustrank()