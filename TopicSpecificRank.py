class TopicSpecificRank:
	def __init__(self, beta, edges, epsilon, max_iterations, node_num, PageRank_vector):
		self.beta = beta
		self.edges = edges
		self.epsilon = epsilon
		self.node_num = node_num
		self.PageRank_vector = PageRank_vector
		self.MAX_ITERATIONS = max_iterations


	def matrix_get_similarTopicPages(self):
		pass


	def matrix_get_initailRankMatrix(self):
		initial_rank_list = [1/(self.node_num) for i in range(self.node_num)]
		initial_rank_vector = SparseMatrix(np.matrix(initial_rank_list).transpose())
		return initial_rank_vector

	
	def matrix_get_topicSpecificGoogleMatrix(self, related_pages):
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
		
		teleport_matrix = SparseMatrix((teleport_matrix_data, (teleport_matrix_row, teleport_matrix_col)), shape = (self.node_num, self.node_num))

		connection_matrix_row = []
		connection_matrix_col = []
		connection_matrix_data = []

		for parent_node in range(self.node_num):
			for child_node in self.edges[parent_node]:
				connection_matrix_col.append(parent_node)
				connection_matrix_row.append(child_node)
				connection_matrix_data.append(
					self.beta / (len(self.edges[parent_node])))
		
		connection_matrix = SparseMatrix((connection_matrix_data, (connection_matrix_row, connection_matrix_col)), shape = (self.node_num, self.node_num))

		google_matrix = connection_matrix + teleport_matrix
		return google_matrix	


	def matrix_get_topicSpecificRank(self, teleport_set, initial_rank_vector, 
		google_matrix):
		iterations = 0
		diff = math.inf
		teleport_set_size = len(teleport_set)
		final_rank_vector = SparseMatrix(np.zeros(self.node_num).transpose())

		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank_vector = google_matrix * initial_rank_vector

			leaked_rank = (1-SparseMatrix.sum(new_rank_vector))/teleport_set_size
			leaked_rank_vector = SparseMatrix(np.array([leaked_rank if node in teleport_set else 0 for node in range(self.node_num)])).transpose()
			
			final_rank_vector = new_rank_vector + leaked_rank_vector
			diff = SparseMatrix.sum(
				abs(final_rank_vector - initial_rank_vector))
			
			initial_rank_vector = final_rank_vector
			iterations += 1
			print("At iteration: " + str(iterations))

		return final_rank_vector


	def list_get_topicSpecificRank(self, teleport_set):
		diff = math.inf
		iterations = 0
		teleport_set_size = len(teleport_set)

		final_rank_vector = np.zeros(self.node_num)
		initial_rank_vector = np.fromiter(
			[1/teleport_set_size if node in teleport_set else 0 for node in range(self.node_num)], dtype='float')
		
		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank_vector = np.zeros(self.node_num)
			for parent in self.edges:
				for child in self.edges[parent]:
					new_rank_vector[child] += initial_rank_vector[parent] /  len(self.edges[parent])

			leaked_rank = (1 - sum(new_rank_vector)) / teleport_set_size
			leaked_rank_vector = np.array([leaked_rank if node in teleport_set else 0 for node in range(self.node_num)])
			
			final_rank_vector = new_rank_vector + leaked_rank_vector
			diff = sum(abs(final_rank_vector - initial_rank_vector))
			initial_rank_vector = final_rank_vector
			
			iterations += 1
			print("At iteration: " + str(iterations))

		return final_rank_vector


	def topicSpecificRank(self):
		lol_of_topic_pages = self.matrix_get_similarTopicPages()
		list_of_rank_vectors = []
		
		for topic in lol_of_topic_pages:
			## approach 1 :: uses adjacency list to calc. rank
			topicSpecificRank_vector = list_get_topicSpecificRank(topic)
			
			## approach 2: RAM eater :: uses SparseMatrices to calc. rank
			# initialRank_vector = self.matrix_get_initailRankMatrix()
			# google_matrix = self.matrix_get_topicSpecificGoogleMatrix(trusted_pages)
			# topicSpecificRank_vector = self.matrix_get_topicSpecificRank(topic, initialRank_vector, google_matrix)
		
			list_of_rank_vectors.append((topic, topicSpecificRank_vector))
			# can append topic number instead of topic(list)^^
		return list_of_rank_vectors