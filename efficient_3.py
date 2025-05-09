import time
import psutil
import sys

from generate import generate_strings
from basic_3 import basic

delta = 30
alpha = {"A" : {"A" : 0,   "C" : 110, "G" : 48,  "T" : 94},
             "C" : {"A" : 110, "C" : 0,   "G" : 118, "T" : 48},
             "G" : {"A" : 48,  "C" : 118, "G" : 0,   "T" : 110},
             "T" : {"A" : 94,  "C" : 48,  "G" : 110, "T" : 0}
             }

def efficient_alignment(x, y):
    #build table by storing lengths of x and y string
    m = len(x)
    n = len(y)
    #store min alignment costs for x and y at i/j
    dp = []

    for row in range(m + 1): # +1 for base (empty)
        inside = [0] * (n + 1)
        dp.append(inside)

    # store result to get to min cost
    backtracking =[]
    for row in range( m + 1):
        inside = []
        for col in range(n + 1):
            inside.append(None)
        backtracking.append(inside)

    #base cases
    for i in range( 1, m + 1):
        dp[i][0] = i * delta
        backtracking[i][0] = 'gapy' #came from above, fill gap in y
    for j in range( 1 , n + 1):
        dp[0][j] = j * delta
        backtracking[0][j] = 'gapx' #from left, fill gap in x

    #fill the table 
    for i in range(1, m + 1):
        for j in range(1, n +1):

            dp[i][j] = min( dp[i-1][j-1] + alpha[x[i-1]][y[j-1]], #match/mismatch
                            dp[i-1][j] + delta, #gapx
                            dp[i][j-1] + delta) #gapy
            if dp[i][j] == (dp[i-1][j-1] + alpha[x[i-1]][y[j-1]]):
                backtracking[i][j] = 'match' #is aligned
            elif dp[i][j] == (dp[i-1][j] + delta):
                backtracking[i][j] = 'gapy' #gap in y
            else:
                backtracking[i][j] = 'gapx' #gap in x
    alignedx, alignedy = [], []
    i, j = m,n


    while i>0 or j >0:
        if backtracking[i][j] == 'match':
            alignedx.append(x[i-1])
            alignedy.append(y[j-1])
            i-= 1
            j -= 1
        elif backtracking[i][j] == 'gapy':
            alignedx.append(x[i-1])
            alignedy.append('_')
            i-=1
        else:
            alignedx.append('_')
            alignedy.append(y[j-1])
            j-= 1

    #reversing string because we are backtracking
    alignedx_str = ''.join(reversed(alignedx))
    alignedy_str = ''.join(reversed(alignedy))
    return dp[m][n], alignedx_str, alignedy_str

    
#Time wrapper
def seq_align_efficient(str1,str2):

    start_time = time.time()
    cost,opt_str1,opt_str2 = efficient_alignment(str1, str2)
    end_time = time.time()

    total_time = (end_time - start_time) * 1000
    print("Final Aligned Result:")
    print(opt_str1)
    print(opt_str2)
    print("Alignment Cost:", cost)

    return opt_str1, opt_str2, cost, total_time

#Memory taken
def process_memory():

    process = psutil.Process()
    memory_info = process.memory_info()
    memory_usage = int(memory_info.rss / 1024)
    return memory_usage

def write_output(path,opt_sol,memory_required):

    try:
        with open(path,"x") as file:
            file.write(f'{str(opt_sol[2])}')
            file.write(f'\n{str(opt_sol[0])}')
            file.write(f'\n{str(opt_sol[1])}')
            file.write(f'\n{str(opt_sol[3])}')
            file.write(f'\n{str(memory_required)}')
    except FileExistsError:
        with open(path,"w") as file:
            file.write(f'{str(opt_sol[2])}')
            file.write(f'\n{str(opt_sol[0])}')
            file.write(f'\n{str(opt_sol[1])}')
            file.write(f'\n{str(opt_sol[3])}')
            file.write(f'\n{str(memory_required)}')


if __name__ == '__main__':

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    string_1,string_2 = generate_strings(input_path)

    opt_sol = seq_align_efficient(string_1,string_2)
    memory_required = process_memory()

    write_output(output_path,opt_sol,memory_required)