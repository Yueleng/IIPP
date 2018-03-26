"""
Algorithmic Thinking - Module 3
10-5-2014
Divide and Conquer Method and Clustering
Closest Pairs and Clustering Algorithms
Project File
Student will implement four functions:
slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)
where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))



def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    current_dist = float("inf") # set default current distance
    closest_pair = [] # default empty list
    epsilon = .000000001 # default value to measure against differences
    
    for index_u in range(len(cluster_list)): # go through each index
        for index_v in range(len(cluster_list)): # each comparison index
            if index_u != index_v: # make sure indeces are not the same
                distance_pair = pair_distance(cluster_list, index_u, index_v) # compute distance based on cluster index
                if abs(distance_pair[0] - current_dist) < epsilon:  # test if less than current distance
                    closest_pair.append(distance_pair)# assign new distance and cluster indeces
                elif distance_pair[0] < current_dist:
                    closest_pair = [distance_pair]
                    current_dist = distance_pair[0]
    
    # if cluster_list contains only one element/cluster
    if len(closest_pair) == 0:
        closest_pair = [(current_dist, -1, -1)] # set default distance and index
    return set(closest_pair)



def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        if len(horiz_order) < 4: # test if number of clusters less than 4
            list_q = [cluster_list[idx] for idx in horiz_order]
            closest_pair = list(slow_closest_pairs(list_q)) # Ugly here!
            return tuple((closest_pair[0][0], horiz_order[closest_pair[0][1]], horiz_order[closest_pair[0][2]]))# if less than use brute force algorithm
        ## base case for fast helper
        
        else:
            idx_m = len(horiz_order) / 2 # number of points in each list half
            horiz_left, horiz_right = horiz_order[:idx_m], horiz_order[idx_m:]
            # split lists into halves
            
            vert_left = [idx for idx in vert_order if idx in set(horiz_left)] # Beautiful code
            vert_right = [idx for idx in vert_order if idx in set(horiz_right)] # Beautiful code
            
            # split vertical elements in half to match horizontal
            left_distance, right_distance = fast_helper(cluster_list, horiz_left, vert_left), fast_helper(cluster_list, horiz_right, vert_right)
            # recursively find the closest distances in the smaller lists
            if left_distance[0] < right_distance[0]:
                closest_pair = left_distance
            else:
                closest_pair = right_distance
        ## divide cluster lists in half and find distances
        
            hcoord = (1/2.0) * (cluster_list[horiz_order[idx_m - 1]].horiz_center() + cluster_list[horiz_order[idx_m]].horiz_center())
            # find the horizontal coordinate of the two middle clusters
            list_split = [idx for idx in vert_order if abs(cluster_list[idx].horiz_center() - hcoord) < closest_pair[0]]
            for idx_u in range(len(list_split) - 1):
                for idx_v in range(idx_u + 1, min([idx_u + 3, len(list_split) - 1]) + 1):
                    contender = pair_distance(cluster_list, list_split[idx_u], list_split[idx_v])
                    if closest_pair[0] > contender[0]:
                        closest_pair = contender
        ## conquer remaining clusters by comparison

        return closest_pair
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order)
    return (answer[0], min(answer[1:]), max(answer[1:]))

    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        current = fast_closest_pair(cluster_list)
        cluster_list[current[1]].merge_clusters(cluster_list[current[2]])
        cluster_list.pop(current[2])
    return cluster_list
    
    
    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    cluster_list_sorted = sorted(cluster_list, key = lambda x: x.total_population(), reverse = True)
    k_clusters = cluster_list_sorted[:num_clusters]
    # initialize k-means clusters to be initial clusters with largest populations
    for dummy_idx in range(num_iterations):
        new_clusters = [alg_cluster.Cluster(set([]), 0, 0, 1, 0) for dummy_idx in range(num_clusters)]
        for idx_j in range(len(cluster_list)):
            current_dist = [cluster_list[idx_j].distance(k_clusters[idx_l]) for idx_l in range(num_clusters)]
            idx_l = min(range(len(current_dist)), key=current_dist.__getitem__)
            new_clusters[idx_l].merge_clusters(cluster_list[idx_j])      
        k_clusters = new_clusters[:]
    return k_clusters