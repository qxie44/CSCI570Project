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
            cost = alpha[x[i - 1]][y[j - 1]]
            curr[j] = min(
                prev[j - 1] + cost, #match/mismatch
                prev[j] + delta, #gap y
                curr[j - 1] + delta #gap x
            )
        prev, curr = curr, [0] * (n + 1)  
    return prev

def efficient_alignment(x, y):
    ##debug help:
    print(f"Aligning x({len(x)}) vs y({len(y)})")

    #x empty, align y with gap
    if len(x ) == 0:
        return "_" * len(y), y
    #y empty, align x w gap
    if len(y) == 0:
        return x, "_" * len(x)
    #if 1
    if len(x) == 1 or len(y) == 1:
        aligned_x, aligned_y, _ = basic(x, y, delta, alpha)
        #already flipped once in basic
        return aligned_x, aligned_y
    
    #split x
    xsplit = len(x) // 2

    #alginment costs
    costLeft = row_cost(x[:xsplit], y)
    costRight = row_cost(x[xsplit:][::-1], y[::-1])

    #minimize cost
    min_score = float('inf')
    ymid = 0
    for i in range(len(y)+ 1):
        total = costLeft[i] + costRight[len(y) - i]
        if total < min_score:
            min_score = total
            ymid = i
    ##test
    print(f"Split x at {xsplit}, y at {ymid}, cost = {min_score}")

    #recursion
    leftA, leftB = efficient_alignment(x[:xsplit], y[:ymid])
    rightA, rightB = efficient_alignment(x[xsplit:], y[ymid:])

    resultA = leftA + rightA
    resultB = leftB + rightB
    #needs to be the same length
    assert len(resultA) == len(resultB), (
    f" Misaligned result: len(x) = {len(resultA)}, len(y) = {len(resultB)}"
)

    return resultA, resultB

    
#Time wrapper
def seq_align_efficient(str1,str2):

    start_time = time.time()
    opt_str1,opt_str2 = efficient_alignment(str1, str2)
    end_time = time.time()
    cost_of_align = sum(
        delta if a == '_' or b == '_' else alpha[a][b]
        for a, b in zip(opt_str1, opt_str2)
    )
    total_time = (end_time - start_time) * 1000
    print("Final Aligned Result:")
    print(opt_str1)
    print(opt_str2)
    print("Alignment Cost:", cost_of_align)

    return opt_str1, opt_str2, cost_of_align, total_time

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