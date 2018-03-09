# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 23:04:29 2018

@author: Yueleng

This program is for picking up right p and m that satifies the condition: all
 three graphs being analyzed in this Application should have the same number 
of nodes and approximately the same number of edges.
"""
from urllib.request import urlopen
import random
import App1 as prj1

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.decode().split('\n')
    graph_lines = graph_lines[ : -1] #Test yourself. You can print graph_lines[-1] and graph_lines[-2] 
                                     # to see which is the real last point.
    
    print("Loaded network graph with", len(graph_lines), "nodes")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        
        # -1 means not including last element!
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def num_of_edges(ugraph):
    '''
    Compute how many edges the graph contains
    '''
    return sum([len(v) for k,v in ugraph.items()]) / 2


##########################################################
# Code for loading UPA graph
    
class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


###########################################################
###########################Testing########################

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
network =   load_graph(NETWORK_URL)
edges_network = num_of_edges(network)
print('Network edges are ', edges_network, '\n')

def make_er_graph(num_nodes, p):
    """
    Takes number of nodes and returns dictionary with ER graph
    
    num_nodes (int) - number of nodes to build into graph
    """
    graph = {key: set([]) for key in range(num_nodes)}
    for node in range(num_nodes):
        for to_node in range(node + 1, num_nodes):
            chance = random.random() #Return the next random floating point number in the range [0.0, 1.0).
            if chance < p:
                graph[node].add(to_node)
                graph[to_node].add(node)
    #print(graph)                
    return graph

er = make_er_graph(1239, 0.004) # after choosing for 10 values of p
print("Loaded er graph with", len(er), "nodes")
edges_er = num_of_edges(er)
print('er edges are ', edges_er, '\n')


def make_upa_graph(n, m):
    graph = prj1.make_complete_graph(m)
    upa = UPATrial(m)
    for idx in range(m, n):
        neighbors = upa.run_trial(m);
        graph[idx] = neighbors
        for neighbor in neighbors:
            graph[neighbor].add(idx)
    
    return graph

upa = make_upa_graph(1239, 3) # after choosing for 10 values of m
print("Loaded upa graph with", len(upa), "nodes")
edges_upa = num_of_edges(upa)
print('upa edges are ', edges_upa, '\n')