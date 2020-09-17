'''
CS 521 HW2
This program implements the APRIORI algorithm to find the set of closed patterns 
from the dataset found in data/.

Author: Michael Truong
'''
import os
import time
import itertools
from optparse import OptionParser
import scipy.io as sio
import numpy as np

DATA_FILE_LOCATION = os.path.join('data', 'dataAPRIORI.mat')
MIN_SUP = 0.15

class CandidateItem(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

def union(list_1, list_2):
    '''
    Returns the union between two sets
    '''
    return list(set(list_1) | set(list_2))

def generate_candidates(L_k, k):
    '''
    Returns list of candidates, C_(k+1) from L_k
    
    Assumes L_k in the format [[1, ..., k], [1, ... ,k], ...]
    Where each element in L_k is a frequent k-itemset
    '''
    candidates = []

    # Iterate over every possible pair of transactions and 
    # append their union to candidates if the union is 
    # one element larger than an itemset in L_k 
    # (emulate self joining L_k)
    candidates = set()
    for item in itertools.combinations(L_k, 2):
        union_ = frozenset(item[0] + item[1])
        if len(union_) == k+1:
            candidates.add(union_)
    
    # Convert candidates from set to list type
    candidates = [CandidateItem(candidate) for candidate in candidates]

    # Prune
    # TODO: Verify this works for all edge cases
    candidates_to_remove = []
    for candidate in candidates:
        # if theres any itemset of size k in candidates that are not in L_k, add it to the
        # list of candidates to be removed
        if any([c for c in itertools.combinations(candidate, k) if not any([it for it in L_k if len(set(c) & set(it)) == k])]):
            candidates_to_remove.append(candidate)
    
    for i in candidates_to_remove: # maybe create an array of true/false and filter the candidates array by that
        candidates.remove(i)
    
    return candidates

def count_candidates(C, transaction):
    '''
    Returns the count of the number of appearences of each
    candidates in `C` found in `transaction`
    '''
    for candidate in C:
        if all(transaction[elem] == 1 for elem in candidate):
            candidate.count+=1

def min_support_candidates(candidates, min_support):
    '''
    Returns the candidates that meets the min_support requirements
    '''
    frequent_candidates = []
    for candidate in candidates:
        if candidate.count >= min_support:
            frequent_candidates.append(candidate)
    return frequent_candidates

def apriori_(data, frequency):
    '''
    Runs APRIORI algorithm on data and returns all of the closed
    itemsets and their frequencies
    '''
    k = 1
    absolute_freq = int(frequency * data.shape[0])
    single_itemset_count = np.sum(data, axis = 0)
    bool_freq_array = single_itemset_count >= absolute_freq

    # We let item j be the column index and thus get the column indices
    # whose column sum satisfies min frequency requirement
    L = [CandidateItem([item[0]]) for item in enumerate(bool_freq_array) if item[1]]
    for elem in L:
        elem.count+=single_itemset_count[elem[0]]
    union_L = []
    while len(L) != 0:
        union_L.append(L)
        C_k1 = generate_candidates(L, k)
        for transaction in data:
            count_candidates(C_k1, transaction)
        L = min_support_candidates(C_k1, absolute_freq)
        k += 1
    
    return union_L

def find_closed_itemsets(frequent_itemsets):
    '''Takes in a list where each kth element is a list containing
    all of the frequent k-itemsets and returns all of the closed
    itemsets'''

    closed_itemsets = []

    return closed_itemsets

if __name__ == "__main__":
    
    optparser = OptionParser()
    optparser.add_option('-o', '--outfile',
                        dest='output_file',
                        help='filename for .mat input file',
                        default='results.txt')

    optparser.add_option('-s', '--minsupport',
                        dest='min_support',
                        help='minimum support for apriori algorithm (0-1)',
                        default = 0.15,
                        type='float')
    
    (options, args) = optparser.parse_args()

    # Load data
    data = sio.loadmat(DATA_FILE_LOCATION)['data']
    output_file = options.output_file
    min_support = options.min_support


    all_frequent_itemsets = apriori_(data, min_support)
    closed_itemsets = find_closed_itemsets(all_frequent_itemsets)

    with open(output_file, "w") as f:
        for L in all_frequent_itemsets:
            for itemset in L:
                f.write("Itemset: {}\tFrequency: {}\n".format(itemset, itemset.count))
