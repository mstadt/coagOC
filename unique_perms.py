'''
This script can be used to generate a list of unique
random permutations of a given length.
'''

# imports
import numpy as np
import pandas as pd
import time
from datetime import datetime
import pickle

# set number of permutations
n_perms = 1e7 # number of permutations
length = 28 # length of permutations


# Generates a list of permutations 
# based on given length and number of permutations
def get_perms(length, num_perms):
    # Define your sequence
    seq = np.arange(length)  

    # Set to store seen permutations
    seen = set()

    # List to store unique permutations
    unique_perms = []

    while len(unique_perms) < num_perms:
        perm = np.random.permutation(seq)
        # Convert to tuple so it can be added to a set
        tuple_perm = tuple(perm)
        if tuple_perm not in seen:
            seen.add(tuple_perm)
            unique_perms.append(perm)
    
    return unique_perms

start_time = time.time()
print(datetime.fromtimestamp(start_time))
# get permuatations
perms = get_perms(length, n_perms)

end_time = time.time()
compute_time = end_time - start_time
print("Compute time: ", compute_time/60, "mins")

# save perms
# Convert to string in scientific notation
str_num = "{:.1e}".format(n_perms)
fname = 'perms_' + str(str_num) + '.pkl'

with open(fname, 'wb') as f:
    pickle.dump(perms, f)
    

print("Perms saved to: ", fname)