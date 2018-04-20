"""
Created on Tue Mar 13 22:40:02 2018

@author: Yueleng

Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane

"""

#import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    current_dist = float("inf") # set default current distance
    closest_pair = [] # default empty list
    #epsilon = .000000001 # default value to measure against differences
    
    for index_u in range(len(cluster_list)): # go through each index
        for index_v in range(index_u + 1, len(cluster_list)): # each comparison index
            if index_u != index_v: # make sure indices are not the same
                distance_pair = pair_distance(cluster_list, index_u, index_v) # compute distance based on cluster index
                #if abs(distance_pair[0] - current_dist) < epsilon:  # test if they are equal
                #    closest_pair.append(distance_pair)# assign new distance and cluster indices
                #elif distance_pair[0] < current_dist:
                #    closest_pair = [distance_pair]
                #    current_dist = distance_pair[0]
                
                if distance_pair[0] < current_dist:
                    closest_pair = distance_pair
                    current_dist = distance_pair[0]
    
    # if cluster_list contains only one element/cluster
    if len(closest_pair) == 0:
        closest_pair = (current_dist, -1, -1) # set default distance and index
    return closest_pair

def fast_helper(cluster_list, horiz_order, vert_order):
    """
    They need doc string! Stupid! 
    """
    #test if the number of clusters is less than 4
    if len(horiz_order) < 4: 
        list_q = [cluster_list[idx] for idx in horiz_order]
        closest_pair = slow_closest_pair(list_q) #returned tuple (dist, idx1, idx2)
        return (closest_pair[0], horiz_order[closest_pair[1]], horiz_order[closest_pair[2]])
    else:
        #split lists into two halves
        idx_m = len(horiz_order) // 2 #set idx_m as the splitting index
        horiz_left, horiz_right = horiz_order[:idx_m], horiz_order[idx_m:]
        
        # split vertical elements in half to match horizontal
        vert_left = [idx for idx in vert_order if idx in set(horiz_left)] # Beautiful code
        vert_right = [idx for idx in vert_order if idx in set(horiz_right)] # Beautiful code
        
        # recursively find the closest distances in the smaller lists
        left_distance, right_distance = fast_helper(cluster_list, horiz_left, vert_left), fast_helper(cluster_list, horiz_right, vert_right)
        
        ## divide cluster lists in half and find distances
        if left_distance[0] < right_distance[0]:
            closest_pair = left_distance
        else:
            closest_pair = right_distance
            
        ## conquer remaining clusters by comparison
        # get the horizontal middle position of the middle two points.
        hcoord = (1/2.0) * (cluster_list[horiz_order[idx_m - 1]].horiz_center() + cluster_list[horiz_order[idx_m]].horiz_center())
        
        # find the horizontal coordinate of the two middle clusters
        list_split = [idx for idx in vert_order if abs(cluster_list[idx].horiz_center() - hcoord) < closest_pair[0]]
        for idx_u in range(len(list_split) - 1):
            for idx_v in range(idx_u + 1, min([idx_u + 3, len(list_split) - 1]) + 1):
                contender = pair_distance(cluster_list, list_split[idx_u], list_split[idx_v])
                if closest_pair[0] > contender[0]:
                    closest_pair = contender
    
    return closest_pair


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    
    
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) for idx in range(len(cluster_list))]
    hcoord_and_index.sort() # sort function sort the tuple by the first element of the tuple by default
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
    
    # compute list of indeces for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) for idx in range(len(cluster_list))]
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]
    
    # compute answer recersively
    answer = fast_helper(cluster_list, horiz_order, vert_order)
    return (answer[0], min(answer[1:]), max(answer[1:]))



def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    # filter out the cluster_list with only clusters inside the strip and should not mutate the cluster_list
    
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) for idx in range(len(cluster_list))]
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))] 
    
    list_split = [idx for idx in vert_order if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width]
    length = len(list_split)
    
    # initialize the closest pair
    closest_pair = (float("inf"), -1 , -1)
    
    for idx_u in range(length - 1):
        for idx_v in range(idx_u + 1, min(idx_u + 3, length - 1) + 1):
            contender = pair_distance(cluster_list, list_split[idx_u], list_split[idx_v])
            if closest_pair[0] > contender[0]:
                closest_pair = contender
                
    return closest_pair
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters, dfunc = None, trigger_set = None):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        current = fast_closest_pair(cluster_list)
        cluster_list[current[1]].merge_clusters(cluster_list[current[2]])
        cluster_list.pop(current[2])

        if dfunc is not None and len(cluster_list) in trigger_set:
            dfunc(cluster_list)
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    cluster_list_sorted = sorted(cluster_list, key = lambda x: x.total_population(), reverse = True)
    # initialize k-means clusters to be initial clusters with largest population
    k_clusters = cluster_list_sorted[:num_clusters]
    
    for dummy_idx in range(num_iterations):
        new_clusters = [alg_cluster.Cluster(set([]), 0, 0, 1, 0) for dummy_index in range(num_clusters)]
        for idx_j in range(len(cluster_list)):
            current_dist = [cluster_list[idx_j].distance(k_clusters[idx_l]) for idx_l in range(num_clusters)]
            idx_l = min(range(len(current_dist)), key = current_dist.__getitem__)
            new_clusters[idx_l].merge_clusters(cluster_list[idx_j])
        k_clusters = new_clusters[:]
    return k_clusters


