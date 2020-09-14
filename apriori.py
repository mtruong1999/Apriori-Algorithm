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
    for item in itertools.combinations(L_k, 2):
        u = union(item[0], item[1])
        if len(u) == k+1:
            candidates.append(u)
    
    # Prune
    for candidate in candidates:
        for itemset in L_k:
            if not set(itemset).issubset(set(candidate)):
                candidates.remove(candidate)
                break

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

