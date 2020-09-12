'''
CS 521 HW2
This program implements the APRIORI algorithm to find the set of closed patterns 
from the dataset found in data/.

Author: Michael Truong
'''
import os
import time
import numpy as np
import scipy.io as sio

DATA_FILE_LOCATION = os.path.join('data', 'dataAPRIORI.mat')
MIN_SUP = 0.15

if __name__ == "__main__":
    # Load data
    data = sio.loadmat(DATA_FILE_LOCATION)['data']

