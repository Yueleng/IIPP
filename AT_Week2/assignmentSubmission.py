'''
http://www.codeskulptor.org/#user44_28x6sCMYp8_25.py
This program is for week2 Assignment: Degree Distribution for Graphs
'''

EX_GRAPH0 = {0 : set([1,2]), 
             1 : set([]),
             2 : set([])}

EX_GRAPH1 = {0 : set([1, 4, 5]),
             1 : set([2, 6]),
             2 : set([3]),
             3 : set([0]),
             4 : set([1]),
             5 : set([2]),
             6 : set([])}

EX_GRAPH2 = {0 : set([1, 4, 5]),
             1 : set([2, 6]),
             2 : set([3, 7]),
             3 : set([7]),
             4 : set([1]),
             5 : set([2]),
             6 : set([]),
             7 : set([3]),
             8 : set([1, 2]),
             9 : set([0, 4, 5, 6, 7, 3])}


def make_complete_graph(num_nodes):
    '''
    this function is for making complete graph for any input nodes.
    '''
    graph = {}
    if num_nodes > 0:
        for node in range(num_nodes):
            temp = set(list(range(num_nodes)))
            temp.discard(node)
            graph[node] = temp
        return graph
    else:
        return graph
    
# print make_complete_graph(0)

def compute_in_degrees(digraph):
    '''
    This function computes each nodes in degree for directed graph.
    '''
    op_digraph = {}
    for key1 in digraph:
        count = 0
        for key2 in digraph:
            if key1 in digraph[key2]:
                count += 1
        op_digraph[key1] = count
    return op_digraph
        
#### For Testing #####        
# dic = compute_in_degrees(EX_GRAPH2)
# for key in dic:
#    print str(key) + " with value: " + str(dic[key])
    
def in_degree_distribution(digraph):
    '''
    This function find the distribution for the in degree.
    '''
    dic = compute_in_degrees(digraph)
    op_dic = {}
    distr_key = set([])
    for key in dic:
        value = dic[key]
        distr_key.add(value)
    for distinct_key in distr_key:
        count = 0
        for key in dic:
            value = dic[key]
            if distinct_key == value:
                count += 1
        op_dic[distinct_key] = count
    return op_dic

print ''
dic = in_degree_distribution(EX_GRAPH2)
for key in dic:
    print str(key) + ' with value: ' + str(dic[key])