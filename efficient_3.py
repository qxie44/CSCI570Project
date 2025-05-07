import time
import psutil
import sys

from generate import generate_strings


delta = 30
alpha = {"A" : {"A" : 0,   "C" : 110, "G" : 48,  "T" : 94},
             "C" : {"A" : 110, "C" : 0,   "G" : 118, "T" : 48},
             "G" : {"A" : 48,  "C" : 118, "G" : 0,   "T" : 110},
             "T" : {"A" : 94,  "C" : 48,  "G" : 110, "T" : 0}
             }

def row_cost(x,y):
    m, n = len(x), len(y)
    #base for empty x
    prev = [i * delta for i in range(n + 1)]
    # new row
    curr = [0] * (n + 1)
    #iterate through all
    for i in range(1, m + 1):
        curr[0] = i * delta
        for j in range(1, n + 1):
            cost = alpha[X[i - 1]][y[j - 1]]
            curr[j] = min(
                prev[j - 1] + cost, #match/mismatch
                prev[j] + delta, #gap y
                curr[j - 1] + delta #gap x
            )
        prev, curr = curr, prev  
    return prev