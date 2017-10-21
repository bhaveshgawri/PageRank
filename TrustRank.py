import math
import heapq
import numpy as np
from scipy.sparse import csr_matrix as SparseMatrix


class TrustRank:
	def __init__(self, beta, edges, epsilon, max_iterations, node_num,
		PageRank_vector):
		self.beta = beta
		self.edges = edges
		self.epsilon = epsilon
		self.node_num = node_num
		self.PageRank_vector = PageRank_vector
		self.MAX_ITERATIONS = max_iterations

		
	def get_trustedPages(self, break_point=100):
		# set number of trusted pages
		if self.node_num < break_point:
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
		trusted_pages = self.get_trustedPages()
		print("got seed set...")
		final_rank_vector = self.get_topicSpecificRank(trusted_pages)
		return final_rank_vector