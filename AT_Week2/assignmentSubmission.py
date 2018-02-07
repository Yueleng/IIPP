# http://www.codeskulptor.org/#user44_28x6sCMYp8_1.py

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
    graph = {}
    if num_nodes > 0:
        for node in range(num_nodes):
            t = list(range(num_nodes))
            t.remove(node)
            graph[node] = t
        return graph
    else:
        return graph
    
print make_complete_graph(0)

compute_in_degrees(digraph)
