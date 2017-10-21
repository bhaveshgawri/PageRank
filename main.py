from graphs import getGraph
from PageRank import PageRank
from TrustRank import TrustRank


def run(node_num, edgeFile, beta=0.85, epsilon=1e-6, max_iterations=20):
	
	gg = getGraph(edgeFile)
	edges = gg.get_connections()

	print("got edges...")

	pr = PageRank(beta, edges, epsilon, max_iterations, node_num)
	PageRank_vector = pr.pageRank()
	print(PageRank_vector, sum(PageRank_vector))

	tr = TrustRank(beta, edges, epsilon, max_iterations, node_num, PageRank_vector)
	TrustRank_vector = tr.trustRank()
	print(TrustRank_vector, sum(TrustRank_vector))


if __name__ == '__main__':
	run(9, "./data/test")