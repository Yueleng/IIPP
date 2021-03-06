# -*- coding: utf-8 -*-
"""
Algorithmic Thinking - Module 2

Created on Tue Mar  6 22:07:24 2018

@author: Yueleng
"""
# general imports
from urllib.request import urlopen
import random
import sys
import timeit
import math

#Desktop imports
import matplotlib.pyplot as plt
import Submission2 as prj2
import App1 as prj1

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node) # Note that this the delete the key and the values correspond to the key.
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            # find max_degree and max_degree_node
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
                
        #remove the max_degree_node and its relationship
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    # the order is from the maximum to the minimum
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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
    
    print("Loaded graph with", len(graph_lines), "nodes")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        
        # -1 means not including last element!
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

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
    
############################################################
# Code for application
        
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

def make_upa_graph(n, m):
    graph = prj1.make_complete_graph(m)
    upa = UPATrial(m)
    for idx in range(m, n):
        neighbors = upa.run_trial(m);
        graph[idx] = neighbors
        for neighbor in neighbors:
            graph[neighbor].add(idx)
    
    return graph

def num_of_edges(ugraph):
    '''
    Compute how many edges the graph contains
    '''
    return sum([len(v) for k,v in ugraph.items()]) / 2

def avg(xs):
    return sum(xs) / len(xs)

def random_order(ugraph):
    nodes = list(ugraph.keys())
    random.shuffle(nodes)
    return nodes
            

#def random_order(num_nodes, graph):
#    """
#    Creates an attacking order
#    """
#    choices = graph.keys()
#    order = set(random.sample(choices, num_nodes))
#    
#    return order



###############################################
########### Question 1 ########################
def question1(network, er, upa, order_func, order_label, filename):
    N = len(network)
    order_net = order_func(network)
    order_er = order_func(er)
    order_upa = order_func(upa)
    network_res = prj2.compute_resilience(network, order_net)
    er_res = prj2.compute_resilience(er, order_er)
    upa_res = prj2.compute_resilience(upa, order_upa)
    
    xs = range(N+1)
    plt.plot(xs, network_res, '-r', label = 'Network graph')
    plt.plot(xs, er_res, '-b', label = 'ER-generated (p = 0.004)')
    plt.plot(xs, upa_res, '-g', label = 'UPA-generated (m = 3)')
    plt.title('Graph resilience (%s)' % order_label)
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.legend(loc = 'upper right');
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' %filename)
    plt.show()
    
if True: 
    network = load_graph(NETWORK_URL)
    er = make_er_graph(1239, 0.004)
    upa = make_upa_graph(1239, 3)
    
    question1(network, er, upa, random_order, 'random order', 'q1.png')
    

def fast_targeted_order(ugraph):
    ugraph = copy_graph(ugraph)
    N = len(ugraph)
    degree_sets = [set([])] * N # Sao Cao Zuo
    for node, neighbors in ugraph.items():
        degree = len(neighbors)
        degree_sets[degree].add(node)
    order = []
    
    for k in range(N-1, -1, -1): # N-1, N-2, N-3, ..., 0
        while degree_sets[k]: # Sao Cao Zuo
            u = degree_sets[k].pop() # pop up an element we don't know. Since set data structure.
            for neighbor in ugraph[u]:
                d = len(ugraph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d - 1].add(neighbor)
                
            order.append(u)
            delete_node(ugraph, u)
    
    return order


    
def measure_targeted_order(n, m, func):
    graph = make_upa_graph(n, m)
    return timeit.timeit(lambda: func(graph), number = 1)
    
def question3(filename):
    xs = range(10, 1000, 10)
    m = 5
    
    ys_targeted = [measure_targeted_order(n, m, targeted_order) for n in xs]
    ys_fast_targeted = [measure_targeted_order(n, m, fast_targeted_order) for n in xs]
    
    plt.plot(xs, ys_targeted, '-r', label = 'targeted_order')
    plt.plot(xs, ys_fast_targeted, '-r', label = 'fast_targeted_order')
    plt.title('Targeted order functions performance (desktup Python)')
    plt.xlabel('Number of nodes in the graph')
    plt.ylabel('Execution time')
    plt.legend(loc = 'upper left')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' % filename)
    plt.show()

if False:    
    question3('q3.png')
   


def question4(filename):
    network = load_graph(NETWORK_URL)
    er = make_er_graph(1239, 0.004)
    upa = make_upa_graph(1239, 3)
    question1(network, er, upa, fast_targeted_order, 'fast_targeted_order', '%s' % filename)
if True:    
    question4('q4.png')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    