'''
Use this script to get the differences in factor levels
before and after OC for the permuted patients.
'''
# imports
import numpy as np
import pandas as pd
import pickle
import time
from datetime import date, datetime

# TO DO:
#   compute mean, std and range of difference for each of the factor levels
#   for both lev and dsg 

start_time = time.time()
print(datetime.fromtimestamp(start_time))

# factor
factor = '' #'VII' #'V' #'II' # 'V', 'VII', 'VIII', 'X'
print("Start Factor ", factor)

# number of permutations
n_perms = 1e7

# load data
fname = 'data/Factor' + factor + '_all.csv'
dat = pd.read_csv(fname)

dat_noOC1 = np.sort(dat['noOC1'].to_numpy()) # no OC1 data
dat_lev = np.sort(dat['lev'].to_numpy()) # lev data
dat_noOC2 = np.sort(dat['noOC2'].to_numpy()) # no OC2 data
dat_dsg = np.sort(dat['dsg'].to_numpy()) # dsg data

str_num = "{:.1e}".format(n_perms)
fname = 'perms_' + str(str_num) + '.pkl'
# load permutations
print('loading permutations')
with open(fname, 'rb') as f:
    perms = pickle.load(f)
    
# Compute mean, std, and range of differences in factor level
# for lev and dsg for each permutation sample
print('start for loop')
print(datetime.fromtimestamp(time.time()))

# initialize arrays
mean_diff_lev = np.zeros(len(perms))
std_diff_lev = np.zeros(len(perms))
range_diff_lev = np.zeros(len(perms))

mean_diff_dsg = np.zeros(len(perms))
std_diff_dsg = np.zeros(len(perms))
range_diff_dsg = np.zeros(len(perms))

for ii in range(len(perms)):
    perm = perms[ii]
    lev = dat_lev[perm]
    diff_lev = lev - dat_noOC1
    
    mean_diff_lev[ii] = np.mean(diff_lev)
    std_diff_lev[ii] = np.std(diff_lev)
    range_diff_lev[ii] = np.max(diff_lev) - np.min(diff_lev)
        
    dsg = dat_dsg[perm]
    diff_dsg = dsg - dat_noOC2
    
    mean_diff_dsg[ii] = np.mean(diff_dsg)
    std_diff_dsg[ii] = np.std(diff_dsg)
    range_diff_dsg[ii] = np.max(diff_dsg) - np.min(diff_dsg)
    
end_time = time.time()
compute_time = (end_time - start_time)/60
print("Compute time: ", compute_time, "mins")

# save the results in a dataframe
df = pd.DataFrame(columns = ['mean diff lev', 'std diff lev', 'range diff lev', 'mean diff dsg', 'std diff dsg', 'range diff dsg'])
df['mean diff lev'] = mean_diff_lev
df['std diff lev'] = std_diff_lev
df['range diff lev'] = range_diff_lev
df['mean diff dsg'] = mean_diff_dsg
df['std diff dsg'] = std_diff_dsg
df['range diff dsg'] = range_diff_dsg

# save results
today = date.today()
date_string = today.strftime("%Y-%m-%d")

fname = date_string + 'Factor' + factor + '_diffs_nperms-'+ str_num + '.csv'
df.to_csv(fname, index=False)

print("Factor ", factor, " done.")
print("Saved to: ", fname)