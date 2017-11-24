 # PageRank Algorithm
 >An implementation of Google's earlier PageRank algorithm.

## Includes:
* Implementation of PageRank Algorithm.
* Implementation of TrustRank Algorithm to identify spam pages.
* Implementation of Topic-Specific Rank Algorithm.
* Visual Representation through a graph at each step as the algorithm proceeds.

## Requirements - `numpy`, `scipy` and `networkx` :  

Using `apt`:
```
$ sudo apt install python3-numpy
$ sudo apt install python3-scipy
$ sudo apt install python3-networkx
```

Using `pip3`:
```
$ sudo pip3 install numpy
$ sudo pip3 install scipy
$ sudo pip3 install networkx
```

## How to run?
Open `main.py`, set the path of corpus and update the number of nodes in your coupus. Save `main.py` and run it.  
```
$ python3 main.py
```
Sample data is provided in `/PageRank/data`. You may use your own graph too.  

## Specification of files:  
### main.py  
Contains the runner function which calls the ranking functions.

### graphs.py
Contains 2 classes: `getGraph` and `plotGraph`.
getGraph: Takes input from graph file. Graph file contains edges of the graph.
plotGraph: The Visualizing class. Plots the web-graph of the screen and shows how it changes as the algorithm proceeds.  

### PageRank.py
Contains class that implements Google's earlier PageRanking Algorithm. Here, teleport set contains all the nodes in the web-graph. A random-surfer can jump to any of the node(page) in the web-graph with equal probaility.

### TrustRank.py
Contains class that implements TrustRank. Trust is propagated from a set of trusted pages to all other pages. Effective in detection of Spam Pages. Here, teleport set is the set of trusted pages.

### TopicSpecificRank.py
Contains class implementing Topic-Specific Rank. Here, teleport set is a set of pages which are related to each other and belong to same topic.

## What else do I need to know?
* Node numbering starts from `0`. Node 0 is a `valid` node in web-graph.
* If you need to change any parameters, change them in `main.py`.
* `Teleports`, `Dead-ends` and `Spider-traps` are taken care off.
* Rank leaked during the iterations is re-distributed among `appropriate` nodes equally.
* 2 implementations of Topic-Spectific Rank:
    - Adjacency list (normal-iteration using numpy arrays)
    - Sparce Matrix  (power-iteration using scipy.csr_matrix)
    
## What are you talking about? What is PageRank?
eFactory: The [PageRank](http://pr.efactory.de/e-pagerank-algorithm.shtml) Algorithm.  
Princeton: [Page Rank](http://www.cs.princeton.edu/~chazelle/courses/BIB/pagerank.htm) explained.  
Wikipedia: [PageRank](https://en.wikipedia.org/wiki/PageRank).
