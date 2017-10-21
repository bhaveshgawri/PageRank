import math
import numpy as np


class PageRank:
	def __init__(self, beta, edges, epsilon, max_iterations, node_num):
		self.beta = beta
		self.edges = edges
		self.epsilon = epsilon
		self.node_num = node_num
		self.MAX_ITERATIONS = max_iterations


	def pageRank(self):
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