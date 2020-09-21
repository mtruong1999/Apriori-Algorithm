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
from tabulate import tabulate

TIMING_RESULT_OUTPUT_FILE = os.path.join('results','timing_result.txt')

class CandidateItem(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

def generate_candidates(L_k, k):
    """Returns list of candidates, C_(k+1), from L_k
    
    Assumes L_k in the format [[1, ..., k], [1, ... ,k], ...]
    Where each element in L_k is a frequent k-itemset
    """
    candidates = []

    # Iterate over every possible pair of transactions and 
    # append their union to candidates if the union is 
    # one element larger than an itemset in L_k 
    # (emulate self joining L_k)
    candidates = set()
    for item in itertools.combinations(L_k, 2):
        union_ = frozenset(item[0].union(item[1]))
        if len(union_) == k+1:
            candidates.add(union_)
    
    # Convert candidates into a list with each candidate converted to custom set
    candidates = [CandidateItem(candidate) for candidate in candidates]

    # Prune
    candidates_to_remove = []
    for candidate in candidates:
        # if there's any itemset of size k in each candidate that is not in L_k, add it to the
        # list of candidates to be removed
        if any([c for c in itertools.combinations(candidate, k) if not any([L for L in L_k if len(set(c) & set(L)) == k])]):
            candidates_to_remove.append(candidate)
    
    for i in candidates_to_remove:
        candidates.remove(i)
    
    return candidates

def count_candidates(C, transaction):
    """Returns the count of the number of appearences of each
    candidate in `C` found in `transaction`
    """
    for candidate in C:
        if all(transaction[elem] == 1 for elem in candidate):
            candidate.count+=1

def min_support_candidates(candidates, min_support):
    """Returns the candidates that meets the min_support requirements""" 

    frequent_candidates = []
    for candidate in candidates:
        if candidate.count >= min_support:
            frequent_candidates.append(candidate)
    return frequent_candidates

def apriori_(data, frequency):
    """Runs APRIORI algorithm on data and returns all of the closed
    itemsets and their frequencies

    Parameters
    ----------
    data: 2-D numpy array
        Matrix where each row is a transaction and the columns are items where
        Mij = 1 indicates that item j is present in transaction i.
    frequency: float
        Min support 'relative' frequency

    Returns
    -------
    Union_L
        A list of lists, where each k-th list contains all the
        frequent k-itemsets. Each set element is of the custom type
        CandidateItem, which has an associated support count.
        e.g. [ [{1}, {2}] , [{1,2}] ]
    """
    k = 1
    absolute_freq = int(frequency * data.shape[0])
    single_itemset_count = np.sum(data, axis = 0)
    bool_freq_array = single_itemset_count >= absolute_freq

    # We let item j be the column index and thus get the column indices
    # whose column sum satisfies min frequency requirement
    L = [CandidateItem([item[0]]) for item in enumerate(bool_freq_array) if item[1]]
    for elem in L:
        for idx in elem:
            elem.count += single_itemset_count[idx]

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

    # For O(n) complexity, we create a frequent itemset dictionary
    # where each key is the absolute frequency count
    frequent_dict = {}
    for itemset in itertools.chain.from_iterable(frequent_itemsets):
        if itemset.count not in frequent_dict:
            frequent_dict[itemset.count] = [itemset]
        else:
            frequent_dict[itemset.count].append(itemset)

    # Find closed itemsets
    closed_itemsets = []
    for itemset in itertools.chain.from_iterable(frequent_itemsets):
        is_closed_itemset = True
        same_frequency_set = frequent_dict[itemset.count]
        for i in same_frequency_set:
                if itemset != i:
                    if itemset.issubset(i):
                        is_closed_itemset = False
                        break
        if is_closed_itemset:
            closed_itemsets.append(itemset)

    return closed_itemsets

if __name__ == "__main__":
    
    optparser = OptionParser()
    optparser.add_option('-a', '--allFrequentOut',
                        dest='all_frequent_output_file',
                        help='output filename for table of all frequent itemsets',
                        default=os.path.join('results','all_frequent_itemsets.txt'))

    optparser.add_option('-c', '--closedItemsetsOut',
                        dest='closed_itemsets_output_file',
                        help='output filename for table of all closed itemsets',
                        default=os.path.join('results','closed_itemsets.txt'))

    optparser.add_option('-s', '--minsupport',
                        dest='min_support',
                        help='minimum support for apriori algorithm (0-1)',
                        default = 0.15,
                        type='float')

    optparser.add_option('-i', '--input',
                        dest='input_file',
                        help='filename for .mat input data',
                        default=os.path.join('data', 'dataAPRIORI.mat'))
    
    # Parse input arguments
    (options, args) = optparser.parse_args()
    all_frequent_output_file = options.all_frequent_output_file
    closed_itemsets_output_file = options.closed_itemsets_output_file
    min_support = options.min_support
    input_file = options.input_file

    # Load data
    data = sio.loadmat(input_file)['data']

    # Run apriori on data, find closed itemsets, and measure running time
    start_time = time.time()
    all_frequent_itemsets = apriori_(data, min_support)
    closed_itemsets = find_closed_itemsets(all_frequent_itemsets)
    time_elapsed = time.time() - start_time

    with open(all_frequent_output_file, "w") as f:
        table = []
        for L in all_frequent_itemsets:
            for itemset in L:
                table.append([set(itemset),itemset.count])
        f.write(tabulate(table, headers = ['Frequent Itemset', 'Count']))
    
    total_number_transactions = data.shape[0]
    with open(closed_itemsets_output_file, 'w') as f:
        table = []
        for closed_itemset in closed_itemsets:
            table.append([set(closed_itemset), closed_itemset.count/total_number_transactions,closed_itemset.count])
        f.write(tabulate(table, headers = ['Closed Itemset', 'Relative Freq.', 'Absolute Freq.']))

    with open(TIMING_RESULT_OUTPUT_FILE, 'w') as f:
        f.write('Running time: {} seconds\n'.format(time_elapsed))
