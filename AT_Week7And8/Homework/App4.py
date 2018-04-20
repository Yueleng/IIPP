"""
Algorithmic Thinking, Part II
Application 4.

@author: Yueleng & Kexin
"""

#DESKTOP = True

from json import dumps
from json import loads
from random import choice
from random import shuffle
from operator import itemgetter
from string import ascii_lowercase

import matplotlib.pyplot as plt
import numpy as np

from project4 import build_scoring_matrix
from project4 import compute_alignment_matrix
from project4 import compute_global_alignment
from project4 import compute_local_alignment

import math
import random
from urllib.request import urlopen

# if DESKTOP:
#     import matplotlib.pyplot as plt
#     import alg_project4_solution as student
# else:
#     import simpleplot
#     import userXX_XXXXXXX as student


# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores

    # NOTE: In python3, urlopen returns binary instead of string. Decode into ascii before using the data.
    """
    scoring_dict = {}
    scoring_file = urlopen(filename)
    ykeys = scoring_file.readline()
    ykeys = ykeys.decode('ascii')
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        line = line.decode('ascii')
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    protein_seq = protein_seq.decode('ascii')
    return protein_seq

def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    # if the input value is '\n' then TypeError: a bytes-like object is required, not 'str'
    word_list = words.split(b'\n')
    word_list = [word.decode('ascii') for word in word_list]
    print("Loaded a dictionary with", len(word_list), "words")
    return word_list


def agreement(xs, ys, scoring, alignmnet):
	_, x, _ = compute_global_alignment(xs, ys, scoring, alignmnet)
	similarity = [1. for (a, b) in zip(x, ys) if a == b] #??? balta2ar wrong? Not Wrong!
	return 100. * len(similarity) / len(x)

def rprot(n, alpha):
	'''
	choice(input) returns random element of input.
	input coulde be list, tuple or string.

	this function return n elements of alpha. Allow duplicate of elements.
	Since there is not pop up during every choice.
	'''
	return ''.join([choice(alpha) for _ in range(n)])

def compare(n, nh, nf, alpha, cons, scoring, align):
	'''
	n: number of trials
	nh: number of characters chosen from alpha and assign to x
	nf: number of characters chosen from alpha and assing to y
	alpha: original string set: alpha = 'ACBEDGFIHKMLNQPSRTWVYXZ'
	cons: Consensus strings 
	scoring: scoring matrix for alpha
	align: alignment matrix????? What is this? Somthing wrong??
	'''
	ag1, ag2 = [], []
	for i in range(n):
		x, y = rprot(nh, alpha), rprot(nf, alpha)
		_, xs, ys = compute_local_alignment(x, y, scoring, align)
		xs_nodash = ''.join([x for x in xs if x!= '-'])
		ys_nodash = ''.join([y for y in ys if y!= '-'])
		ag1.append(agreement(xs_nodash, cons, scoring, align))
		ag2.append(agreement(ys_nodash, cons, scoring, align))

	hc_agree = sum(ag1) / float(n)
	fc_agree = sum(ag2) / float(n)

	print('Random Human vs Consensus agree = %s%%' %hc_agree)
	print('Random Fly vs Consensus agree = %s%%' % fc_agree)

def question1And2():
    human = read_protein(HUMAN_EYELESS_URL)
    fly = read_protein(FRUITFLY_EYELESS_URL)
    print(len(human), len(fly))

    scoring = read_scoring_matrix(PAM50_URL)
    local_align_matrix = compute_alignment_matrix(human, fly, scoring, False)
    score, xs, ys = compute_local_alignment(human, fly, scoring, local_align_matrix)
    print('Question 1')
    print('The score of the local alignment is: ', score)
    print('The sequence for the HumanEyelessProtein is: ', xs)
    print('The sequence for the FruitflyEyelessProtein is: ', ys)
    print()



    print('Question2')
    consensus = read_protein(CONSENSUS_PAX_URL)

    # Step1: Delete any dashes '-' present in the sequence.
    human_nodash = ''.join([x for x in xs if x!= '-'])
    fly_nodash = ''.join([y for y in ys if y!= '-'])

    # Step2: Compute the global alignment of this dash-less sequence with the ConsensusPAXDomain sequence.
    hc_global_align_matrix = compute_alignment_matrix(human_nodash, consensus, scoring, True)
    fc_global_align_matrix = compute_alignment_matrix(fly_nodash, consensus, scoring, True)
    
    # Step3: Compare corresponding elements of these two globally-aligned sequences (local vs consensus) and 
    # compute the percentage  of elements in these two sequences that agree
    # NOTE: func agreement contains Stpe2 and Step3.
    hc_agree = agreement(human_nodash, consensus, scoring, hc_global_align_matrix)
    fc_agree = agreement(fly_nodash, consensus, scoring, fc_global_align_matrix)


    print('Human vs Consensus agree = %s%%' % hc_agree)
    print('Fly vs Consensus agree = %s%%' % fc_agree)

    # alpha = 'ACBEDGFIHKMLNQPSRTWVYXZ'
    # compare(1000, len(human), len(fly), consensus, scoring, local_align)

    # pirnt()


def generate_null_distribution2(seq_x, seq_y, scoring_matrix, num_trials):
    # This function does work. I don't understand why balta2ar write it this way by using distr.json
	distr = {} # store the whole distribution {score1: count1, score2: count2, ..., scoren: countn}
	raw = []   # store all the scores: [score1, score2, ..., scoren], could be duplicate

	try: 
		with open('distr.json') as f:
			pair = loads(f.read())
			return pair['distr'], pair['raw']
	except Exception as e:
		print('can\'t open file', str(e))

	for _ in range(num_trials):
		temp = list(seq_y)
		shuffle(temp)
		rand_y = ''.join(temp)
		align_matrix = compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
		score, _, _ = compute_local_alignment(seq_x, rand_y, scoring_matrix, align_matrix)
		if score not in distr:
			distr[score] = 0
		distr[score] += 1
		raw.append(score)

	with open('distr.json', 'w') as f:
		f.write(dumps({'distr': distr, 'raw': raw}))
	
	return distr, raw

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    distr = {}  # store the whole distribution {score1: count1, score2: count2, ..., scoren: countn}
    raw = []  # store all the scores: [score1, score2, ..., scoren], could be duplicate
    
    for _ in range(num_trials):
        temp = list(seq_y)
        shuffle(temp)
        rand_y = ''.join(temp)
        align_matrix = compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)  # Returns local alignment matrix.
        score, _, _ = compute_local_alignment(seq_x, rand_y, scoring_matrix, align_matrix)
        if score not in distr:
            distr[score] = 0
        distr[score] += 1                
        raw.append(score)
    return distr, raw





def norm(d):
    total = float(sum(d.values()))
	# return {k: v / total for k, v in d.iteritems()}
    # In python3, iteritems has been replaced by items. 
    return {k: v / total for k, v in d.items()}

def str_keys(d):
	# Convert the key k into int k for an input dictionary d.
	return {int(k): v for k, v in d.items()}

def question4And5(filename):
    human = read_protein(HUMAN_EYELESS_URL)
    fly = read_protein(FRUITFLY_EYELESS_URL)
    scoring = read_scoring_matrix(PAM50_URL)
    distr, raw = generate_null_distribution(human, fly, scoring, 1000)
    
    # What does this mean?
    from pprint import pprint as pp
    distr = str_keys(distr)
    pp(distr)
    distr = norm(distr)
    
    pairs = list(distr.items()) #[(k1, v1), (k2, v2), ..., (kn, vn)]
    pairs = sorted(pairs, key = itemgetter(0)) # sort by key. sort by k1, k2, k3, ... kn.
    print(pairs)
    index = np.arange(len(pairs))
    
    # map(function, iteriable)
    # since the second parameter of plt.bar() should be a sequnce instead of a generator.
    # In python2 map() function returns a list, but in python3 map() function repterns a generator.
    plt.bar( index, list(map(itemgetter(1), pairs)) )
    plt.xticks(index , list(map(itemgetter(0), pairs)), fontsize = 8)
    plt.xlabel('Score')
    plt.ylabel('Fraction of total trials')
    plt.title('Distribution of scores')
    plt.tight_layout
    plt.savefig(filename)
    
    s_score = 875 # What does this mean? --> The result from Questio1.
    n = 1000
    mean = sum(raw) / n
    std = np.sqrt(sum((x - mean) ** 2 for x in raw) / n)
    z_score = (s_score - mean) / std
    
    print('mean = %f' % mean)
    print('std = %f' % std)
    print('z_score = %f' % z_score)

def edit_dist(xs, ys):
	alphabet = ascii_lowercase # what is ascii_lowercase??
	scoring = build_scoring_matrix(alphabet, 2, 1, 0)
	align = compute_alignment_matrix(xs, ys, scoring, True) # True means global alignment.
	score, _, _ = compute_global_alignment(xs, ys, scoring, align)
	return len(xs) + len(ys) - score

def check_spelling(checked_word, dist, word_list):
	'''
	Compare every element x in word_list with checked_word a, return 
	a set of words that satisfies edit_dist(a, x) <= given distance.
	'''
	return set([word for word in word_list 
                    if edit_dist(checked_word, word) <= dist])

def question8():
	# Why does he use this method to read list of words
	# while the function read_words() is given?
	# Does the code work?
	# words = [x.strip() for x in open(WORD_LIST_URL).readlines]
    word_list = read_words(WORD_LIST_URL)
    print('len = ', len(word_list))
    print('type = ', type(word_list[0]))
    humble_words = check_spelling('humble', 1, word_list)
    firefly_words = check_spelling('firefly', 2, word_list)
    print(len(humble_words), humble_words)
    print(len(firefly_words),firefly_words)

def main():
	# Uncomment this one by one.
	# question1And2()
	# question4And5('q4.png') # Very Slow. Try 20 iterations first to debug and then change to 1000 iterations
	question8()


if __name__ == '__main__':
    main()
