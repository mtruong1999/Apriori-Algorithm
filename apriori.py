'''
CS 521 HW2
This program implements the APRIORI algorithm to find the set of closed patterns 
from the dataset found in data/.

Author: Michael Truong
'''
import os
import time
import itertools
import scipy.io as sio

DATA_FILE_LOCATION = os.path.join('data', 'dataAPRIORI.mat')
MIN_SUP = 0.15

class CandidateList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
    candidates = [list(candidate) for candidate in candidates]

    # Prune
    # TODO: Verify this works for all edge cases
    candidates_to_remove = []
    for candidate in candidates:
        # if theres any itemset of size k in candidates that are not in L_k, add it to the
        # list of candidates to be removed
        if any([c for c in itertools.combinations(candidate, k) if not any([it for it in L_k if len(set(c) & set(it)) == k])]):
            candidates_to_remove.append(candidate)
    
    for i in candidates_to_remove:
        candidates.remove(i)
    
    return candidates

def count_candidates(C, transaction):
    '''
    Returns the count of the number of appearences of each
    candidates in `C` found in `transaction`
    '''
    pass

def min_support_candidates(candidate_counts, min_support):
    '''
    Returns the candidates that meets the min_support requirements
    '''
    pass

def apriori_(data):
    '''
    Runs APRIORI algorithm on data and returns all of the closed
    itemsets and their frequencies
    '''
    pass

if __name__ == "__main__":
    # Load data
    data = sio.loadmat(DATA_FILE_LOCATION)['data']

