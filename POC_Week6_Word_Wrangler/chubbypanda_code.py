"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"

# Function that checks for the presenct of an element in a list
def binary_search(lst, elt):
    """ 
    O(log2) algorithm used to check for the presence of el in list
    """
    # base case
    if len(lst) == 1:
        return lst[0] == elt
    middle = len(lst) / 2
    if lst[middle] == elt:
        return True
    else:
        if elt < lst[middle]:
            return binary_search(lst[:middle], elt)
        else:
            return binary_search(lst[middle:], elt)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    This function can be iterative.
    """
    unique_list = []
    for idx in range(len(list1)):
        if idx == 0 or list1[idx] != list1[idx-1]:
            unique_list.append(list1[idx])
    return unique_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.
    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    This function can be iterative.
    """
    intersection_set = []
    for elt in list1:
        if binary_search(list2, elt):
            intersection_set.append(elt)
    return intersection_set


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.
    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.
    This function can be iterative.
    """   
    result = []
    idx, jdx = 0, 0
    while idx < len(list1) and jdx < len(list2):
        if list1[idx] < list2[jdx]:
            result.append(list1[idx])
            idx += 1
        else:
            result.append(list2[jdx])
            jdx += 1
    while idx < len(list1):
        result.append(list1[idx])
        idx += 1
    while jdx < len(list2):
        result.append(list2[jdx])
        jdx += 1
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.
    Return a new sorted list with the same elements as list1.
    This function should be recursive.
    """
    # base case
    if len(list1) <= 1:
        return list1
    # recursive case
    else:
        middle = len(list1) / 2
        left = merge_sort(list1[:middle])
        right = merge_sort(list1[middle:])
        return merge(left, right)

# Function to generate all strings for the word wrangler game


def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.
    Returns a list of all strings that can be formed from the letters
    in word.
    This function should be recursive.
    """
    # base case
    if len(word) == 0:
        return ['']
    # recursive case
    else:
        first_char = word[0]
        rest_chars = word[1:]
        rest_chars_words = gen_all_strings(rest_chars)
        words = rest_chars_words[:]
        for word in rest_chars_words:
            words += string_char_combinations(word, first_char)
        return words


# Function to generate all possible new words by adding a character to a word

def string_char_combinations(word, char):
    """
    Returns all new possible words generated by adding char to any position in word
    """
    words = []
    for char_pos in range(len(word)+1):
        new_word = [''] * (len(word)+1)
        word_chars = list(word)
        for pos in range(len(new_word)):
            if pos == char_pos:
                new_word[pos] = char   
            else:
                new_word[pos] = word_chars.pop(0)
        words.append(''.join(new_word))
    return words


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.
    Returns a list of strings.
    """
    return filename.readlines()

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
