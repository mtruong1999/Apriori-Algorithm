# CS 521 Assignment 2: Apriori Algorithm to Find Closed Itemsets
## Overview
The code implements the apriori algorithm to find all frequent itemsets and extract the closed itemsets. The input data is assumed to be a 2-D matrix where each row is a transaction and each column j indicates (using 1 or 0) whether item j is present.

Note: We follow a zero-index convention in our item labels, i.e. we consider the first column of the data matrix to be item `0`.

The closed itemsets and running time measurement results can be found in the `results/` directory. 

## Setup
1. Installation of [Python 3.7](https://www.python.org/downloads/) or later required

2. To install dependencies, in the `HW2_APRIORI/` directory, run
```
pip install -r requirements.txt
```

## Usage
To run the program with dataset provided and default values for minimum support (0.15)
```
python apriori.py
```
### Command Line Options
- Use `-s` to change the min support. Default: `0.15`.
- Use `-i` to change the input file (which must be a `.mat` matrix file). Default: `data/dataAPRIORI.mat`.
- Use `-c` to change the output filename for the list of all closed itemsets. Default: `results/closed_itemsets.txt`.
- Use `-a` to change the output filename for the list of all frequent itemsets. Default: `results/all_frequent_itemsets.txt`.

Example,
```
python apriori.py -s 0.5 -i INPUT_DATA.mat -c OUTPUT_CLOSED_ITEMSETS -a OUTPUT_ALL_ITEMSETS
```
