import math
import numpy as np
from collections import defaultdict

class PageRanker:
	def __init__(self, node_num, edge_file, beta = 0.85, epsilon = 1e-6, max_iterations = 100):
		self.beta = beta
		self.edges = None
		self.edge_file = edge_file
		self.epsilon = epsilon
		self.node_num = node_num
		self.MAX_ITERATIONS = max_iterations
		self.rank = np.zeros(self.node_num)

	def get_connections(self):
		edge_list = []
		self.edges = defaultdict(list)

		with open (self.edge_file, 'r') as ef:
			edge_list = ef.readlines()
		
		for edge in edge_list:
			from_, to_ = edge.split('\t')
			from_, to_ = int(from_), int(to_[:-1])
			self.edges[from_].append(to_)
		
		for edge in self.edges:
			print(edge, self.edges[edge])

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
			print(self.rank)

if __name__ == '__main__':
	p = PageRanker(9, './data/test')
	p.get_connections()
	p.pagerank()