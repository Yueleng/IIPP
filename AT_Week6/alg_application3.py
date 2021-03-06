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
    # def make(_):
    #     x = random() * 2 - 1
    #     y = random() * 2 - 1
    #     return Cluster(set(['0']), x, y, 1, 1)
    #
    # return map(make, range(num_clusters))
    clusters = []
    for dummy_idx in range(num_clusters):
        x = random() * 2 - 1
        y = random() * 2 - 1
        clusters.append(Cluster(set(['0']), x, y, 1, 1))
    return clusters

def question1(filename):
    xs = range(2, 201)
    ys_fast, ys_slow = [], []
    for n in xs:
        clusters = get_random_clusters(n)
        ys_fast.append(timeit(lambda: fast_closest_pair(clusters), number=1))
        ys_slow.append(timeit(lambda: slow_closest_pair(clusters), number=1))

    plt.plot(xs, ys_fast, '-r', label='fast_closest_pair')
    plt.plot(xs, ys_slow, '-b', label='slow_closest_pair')
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
    '''
    :param clusters: list of clusters
    :param table: data table
    :return: sum of errors for each cluster
    '''
    return sum([x.cluster_error(table) for x in clusters])


def question5(filename):
    data = 'unifiedCancerData_111.csv'
    dist = distortion(visualize(data, filename, lambda x: hierarchical_clustering(x, 9)), load_data_table(data))
    print('Distortion in question5, hierarchical_clustering = %f (%s)' % (dist, dist))


def question6(filename):
    data = 'unifiedCancerData_111.csv'
    dist = distortion(visualize(data, filename, lambda x: kmeans_clustering(x, 9, 5)), load_data_table(data))
    print('Distortion in question6, kmeans = %f (%s)' % (dist, dist))




def load_as_list(filename):
    clusters = []
    with open(filename) as f:
        for line in f.readlines():
            fips, x, y, pop, risk = line.split(',')
            clusters.append(Cluster(set([fips]), float(x), float(y), int(pop), float(risk)))
    return clusters


def question10(data, filename):
    table = load_data_table(data)
    clusters = load_as_list(data)
    xs = range(6, 21)
    ys_hier = []

    def dist(clusters):
        ys_hier.append(distortion(clusters, table))

    hierarchical_clustering(clusters, 6, dist, set(xs))
    ys_hier.reverse()
    clusters = load_as_list(data)
    ys_kmeans = [distortion(kmeans_clustering(clusters, x, 5), table) for x in xs]

    plt.cla()
    plt.plot(xs, ys_hier, '-r', label='Hierarchical clustering distortion')
    plt.plot(xs, ys_kmeans, '-b', label='k-means clustering distortion')
    plt.title('Clustering distortion (%s)' % data)
    plt.xlabel('Number of output clusters')
    plt.ylabel('Distortion')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' % filename)




def main():
    # question1('question1.png')
    # question2('question2.png')
    # question3('question3.png')
    # question5('question5.png')
    # question6('question6.png')
    question10('./unifiedCancerData_111.csv', 'question10-111.png')
    question10('./unifiedCancerData_290.csv', 'question10-290.png')
    question10('./unifiedCancerData_896.csv', 'question10-896.png')

if __name__ == '__main__':
    main()
