"""
http://www.codeskulptor.org/#user44_o0IRGoZTfD_12.py
Provided code for Application portion of Module 1

Imports physics citation graph 
"""
#import codeskulptor
#codeskulptor.set_timeout(50)

# general imports
from urllib.request import urlopen
import random
import matplotlib.pyplot as plt
# Set timeout for CodeSkulptor if necessary
# import codeskulptor
# codeskulptor.set_timeout(40)

QUESTION_ONE = True
QUESTION_TWO = False
FINAL = False

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


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.decode().split('\n')
    graph_lines = graph_lines[ : -1]
    
    print("Loaded graph with " + str(len(graph_lines)) + " nodes.")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)



#########################################
def compute_in_degrees(digraph):
    """
    Takes in a digraph and computes the in-degrees for each node.
    
    digraph (dict) - directional graph
    return: dictionary with in-degrees for each node
    """
    #initialize variables
    # degrees = dict.fromkeys(digraph, 0)
    degrees = {}
    for key in digraph:
        degrees[key] = 0
    
    #calculate in-degrees for each node in directional graph
    for node in digraph:
        for edge in digraph[node]:
            degrees[edge] += 1

    #return # of total in degrees
    return degrees
    

def in_degree_distribution(digraph):
    """
    Takes in a digraph and computes the unnormalized distribution for the in-degrees
    
    digraph (dict) - directional graph
    return: 
    """
    #initialize variables
    computed = compute_in_degrees(digraph)
    distrib = {}
    
    #computes distribution for the in-degrees
    for node in computed:
        degree = computed[node]
        if degree not in distrib:
            distrib[degree] = 1
        else:
            distrib[degree] += 1
    
    #return dictionary of distribution
    return distrib
# distr = in_degree_distribution(citation_graph)

######## Question 1 ##########

def normalize_distribution(digraph):
    distribution = in_degree_distribution(digraph)
    sum_nodes = len(digraph)
    
    normalized = {}
    for key in distribution:
        normalized[key] = distribution[key] / float(sum_nodes)
    return normalized

# normalized_distr = normalize_distribution(citation_graph)
# print normalized_distr

def plot_normalized(normal_distrib):
    x_vals = []
    y_vals = []
    for degree in normal_distrib:
        x_vals.append(degree)
        y_vals.append(normal_distrib[degree])
    plt.loglog(x_vals, y_vals, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log of Number of Degrees")
    plt.ylabel("Log of Distribution")
    plt.title("Log/log Normalized Distribution of High Energy Physics Theory Papers")
    plt.show()

if QUESTION_ONE:
    print("Loading citation graph...")
    citation_graph = load_graph(CITATION_URL)
    out_degrees = 0
    print("Calculating average out degrees for citation graph...")
    for node in citation_graph:
        out_degrees += len(citation_graph[node])
    print(out_degrees / len(citation_graph))
    print("Calculating normalized distribution of in degrees...")
    n = normalize_distribution(citation_graph)
    print("Plotting normalized distibution...")
    plot_normalized(n)

######## Question 2 ##########
def generate_rand_digraph_with_prob_p(num_nodes, prob):
    digraph = {}
    for node_i in range(num_nodes):
        edges = []
        for node_j in range(num_nodes):
            random_num = random.random() # Return the next random floating point number in the range [0.0, 1.0).
            if random_num < prob and node_i != node_j:
                edges.append(node_j)
        digraph[node_i] = edges
    return digraph
        
def plot_question_2():
    # digraph = generate_rand_digraph_with_prob_p(1000, 0.6)
    #normalized_distr = normalize_distribution(digraph)
    #dataset = {}
    #for degree in normalized_distr:
    #    dataset[math.log(degree)] =  math.log(normalized_distr[degree])
    #simpleplot.plot_scatter('Log/log Normalized Distribution for Random Generated Digraphs', 600, 600, 'Log of Number of Degrees', 'Log of Distribution', [dataset], ['data'])
    x_d0, y_d0 = [], []
    d0 = generate_rand_digraph_with_prob_p(20000, .5)
    norm_0 = normalize_distribution(d0)
    for degree in norm_0:
        x_d0.append(degree)
        y_d0.append(norm_0[degree])
    
    plt.plot(x_d0, y_d0, color="black", linestyle='None', marker=".", markersize=6)
    
if QUESTION_TWO:
    plot_question_2()

######## Question 3 ##########
class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set([])
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

    
def DPA_algo(num_nodes, exist_nodes):
    """
    
    
    num_nodes (int) - number of nodes to add
    exist_nodes (int) - number of existing nodes to connect to
    return: digraph (dict)
    """
    #initialize variables for direction graph
    digraph = make_complete_graph(exist_nodes)
    trial = DPATrial(exist_nodes)
    #create DPA graph
    for new_node in range(exist_nodes, num_nodes):
        #print(digraph)
        #print("")
        total_in = compute_in_degrees(digraph)
        total_indegrees = 0
        for node in total_in:
            total_indegrees += total_in[node]
        
        to_connect = trial.run_trial(exist_nodes)
        digraph[new_node] = to_connect
    
    #return direction DPA graph
    return digraph
                

########### Question 3-5 ###############

N = 27770
M = 13

def plot_final():
    DPA_graph = DPA_algo(N, M)
    #normalized_distr = normalize_distribution(DPA_graph)
    #dataset = {}
    #for degree in normalized_distr:
    #    dataset[math.log(degree)] =  math.log(normalized_distr[degree])
    # simpleplot.plot_scatter('Log/log Normalized Distribution for DPA Digraphs', 600, 600, 'Log of Number of Degrees', 'Log of Distribution', [dataset], ['data'])
    print(len(DPA_graph))
    normal_distrib = normalize_distribution(DPA_graph)
    x_vals = []
    y_vals = []
    for degree in normal_distrib:
        x_vals.append(degree)
        y_vals.append(normal_distrib[degree])
    plt.loglog(x_vals, y_vals, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log of Number of Degrees")
    plt.ylabel("Log of Distribution")
    plt.title("Log/log Normalized Distribution of DPA_algo generated graph")
    plt.show()
if FINAL:
    plot_final()      
        