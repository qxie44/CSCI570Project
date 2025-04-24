#Basic.py
#Basic Sequence alignment
import time
import psutil
import sys

from BasicModel import generate_strings

def basic(str1,str2,delta,alpha):
    """

    :param str1: String 1
    :param str2: String 2
    :param delta: 30
    :param alpha: alpha pq values

    Recurrence equation : opt[i][j] = min(
                    #optimal alignment      opt[i-1][j-1] + alpha(i,j)
                    #char1 is not matched   opt[i-1][j] + delta,
                    #char2 is not matched   opt[i][j-1] + delta
                                          )

    """
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1

    opt = [[0] * len_str2 for _ in range(len_str1)]

    #Initialize base cases
    for i in range(len_str1):
        opt[i][0] = i * delta
    for i in range(len_str2):
        opt[0][i] = i * delta

    #Filling out the OPT table(dp)
    for i in range(1,len_str1):
        for j in range(1,len_str2):
            char1 = str1[i - 1]
            char2 = str2[j - 1]
            alphaPQ = alpha[char1][char2]
            opt[i][j] = min(opt[i-1][j-1] + alphaPQ,
                            opt[i - 1][j] + delta,
                            opt[i][j-1] + delta
                            )

    res_str1,res_str2 = "",""
    i,j = len(str1),len(str2)

    #Sequence
    while i > 0 and j > 0:
        char1 = str1[i - 1]
        char2 = str2[j - 1]
        alphaPQ = alpha[char1][char2]

        if opt[i][j] == opt[i-1][j-1] + alphaPQ: #Match
            res_str1 += char1
            res_str2 += char2
            i -= 1
            j -= 1
        elif opt[i][j] == opt[i - 1][j] + delta: #Gap in string 1
            res_str1 += char1
            res_str2 += "_"
            i -= 1
        elif opt[i][j] == opt[i][j - 1] + delta: #Gap in string 2
            res_str1 += "_"
            res_str2 += char2
            j -= 1

    cost_of_align = opt[len(str1)][len(str2)]

    return res_str1[::-1], res_str2[::-1], cost_of_align


#Time wrapper
def seq_align_basic(str1,str2,delta,alpha):

    start_time = time.time()
    opt_str1,opt_str2,cost_of_align = basic(string_1, string_2, delta, alpha)
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
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

    delta = 30
    alpha = {"A" : {"A" : 0,   "C" : 110, "G" : 48,  "T" : 94},
             "C" : {"A" : 110, "C" : 0,   "G" : 118, "T" : 48},
             "G" : {"A" : 48,  "C" : 118, "G" : 0,   "T" : 110},
             "T" : {"A" : 94,  "C" : 48,  "G" : 110, "T" : 0}
             }


    input_path = sys.argv[1]
    output_path = sys.argv[2]

    string_1,string_2 = generate_strings(input_path)

    opt_sol = seq_align_basic(string_1,string_2,delta,alpha)
    memory_required = process_memory()

    write_output(output_path,opt_sol,memory_required)
