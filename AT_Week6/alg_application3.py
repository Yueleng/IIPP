# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 20:33:49 2018

@author: Yueleng
"""
from random import random
from timeit import timeit
from matplotlib import pyplot as plt
from alg_cluster import Cluster
from alg_project3_solution import slow_closest_pair
from alg_project3_solution import fast_closest_pair
from alg_project3_solution import hierarchical_clustering
from alg_project3_solution import kmeans_clustering
from alg_project3_viz import visualize
from alg_project3_viz import load_data_table

def get_random_clusters(num_clusters):
    def make(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return Cluster(set(['0']), x, y, 1, 1)

    return map(make, range(num_clusters))

def question1(filename):
    xs = range(2, 201)
    ys_fast, ys_slow = [], []
    for n in xs:
        clusters = get_random_clusters(n)
        ys_fast.append(timeit(lambda: fast_closest_pair(clusters), number=1))
        ys_slow.append(timeit(lambda: slow_closest_pair(clusters), number=1))

    plt.plot(xs, ys_fast, '-r', label='fast_closest_pair')
    plt.plot(xs, ys_fast, '-b', label='slow_closest_pair')
    plt.title('Running time of two closest_pair functions (desktop Python)')
    plt.xlabel('Number of initial clusters')
    plt.ylabel('Running time, seconds')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s', filename)

def question2(filename):
    visualize('unifiedCancerData_3108.csv', filename, lambda x: hierarchical_clustering(x, 15))


def question3(filename):
    visualize('unifiedCancerData_3108.csv', filename, lambda x: kmeans_clustering(x, 15, 5))

def distortion(clusters, table):
    return sum([x.cluster_error(table) for x in clusters])

