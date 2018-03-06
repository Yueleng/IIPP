# -*- coding: utf-8 -*-
"""
Algorithmic Thinking - Module 2

Created on Mon Mar  5 22:27:14 2018

@author: Yueleng
"""

from collections import deque
import random

def bfs_visited(ugraph, start_node):
    '''
    Takes in an undirected graph and start node and returns set of nodes that are visited by that node by BFS.
    
    return: set of nodes
    '''
    #variable initialization
    queue = deque()
    visited = set([start_node])
    queue.append(start_node)
    
    #main loop for computing which nodes are visited by start node
    while len(queue) > 0:
        node_j = queue.popleft()
        for neighbor in ugraph[node_j]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
            
    return visited
    
def cc_visited(ugraph):
    """
    Takes in an undirected graph and returns list of sets where each set consists
    of all the nodes in a connected component.
    
    return: list of sets of nodes
    """
    
    #variable initialization
    remaining = ugraph.keys()
    remaining = set(remaining)
    cc = []
    
    #main loop for calculation all connected components in undirectional graph
    while len(remaining) > 0:
        node_i = random.choice(tuple(remaining)) # You have to change them to tuple in order to use random.choice
        #node_i = random.sample(remaining, 1)[0] # return the list, that's why we have to use [0] 
        component = bfs_visited(ugraph, node_i)
        cc.append(component)
        for node in component:
            remaining.remove(node)
        
    #return list of sets of componenets
    return cc
    
    
def largest_cc_size(ugraph):
    """
    Takes in undirected graph and returns the size of largest connected component
    
    return: int
    """
    #variable initialization
    size = 0
    cc = cc_visited(ugraph)
    
    #loop through components to calculate largest one
    for component in cc:
        if len(component) > size:
            size = len(component)
            
    #return int of largest component
    return size
    

def compute_resilience(ugraph, attack_order):
    '''
    Takes in undirected graph and a list of nodes(attack_order). Iterate throught the attack order
    nodes removing the given node and its edges from the graph. Then computes the largest connected
    component for the remaining graph.
    
    return: list of largest connected components after each removal.
    '''
    #initialize variables
    sizes = []
    newgraph = ugraph.copy()
    sizes.append(largest_cc_size(newgraph))
    
    #loop for calculating and removing nodes
    for node in attack_order:
        newgraph.pop(node) #Python Dictionary pop()
        for nodes in newgraph:
            newgraph[nodes].discard(node)
        sizes.append(largest_cc_size(newgraph))
        
    #return list of sizes for components
    return sizes


    
    
    
    
    
    
    
    
    
    