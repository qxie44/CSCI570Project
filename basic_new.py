# basic_3.py — Full DP Sequence Alignment with memory/time output
import time
import psutil
import sys
from generate import generate_strings

def basic(str1, str2, delta, alpha):
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1

    opt = [[0] * len_str2 for _ in range(len_str1)]

    # Initialize base cases
    for i in range(len_str1):
        opt[i][0] = i * delta
    for j in range(len_str2):
        opt[0][j] = j * delta

    # Fill DP table
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            char1 = str1[i - 1]
            char2 = str2[j - 1]
            alphaPQ = alpha[char1][char2]
            opt[i][j] = min(
                opt[i - 1][j - 1] + alphaPQ,
                opt[i - 1][j] + delta,
                opt[i][j - 1] + delta
            )

    # Traceback
    res_str1, res_str2 = "", ""
    i, j = len(str1), len(str2)

    while i > 0 and j > 0:
        char1 = str1[i - 1]
        char2 = str2[j - 1]
        alphaPQ = alpha[char1][char2]

        if opt[i][j] == opt[i - 1][j - 1] + alphaPQ:
            res_str1 += char1
            res_str2 += char2
            i -= 1
            j -= 1
        elif opt[i][j] == opt[i - 1][j] + delta:
            res_str1 += char1
            res_str2 += "_"
            i -= 1
        else:
            res_str1 += "_"
            res_str2 += char2
            j -= 1

    # ✅ Add remaining characters (prefix gaps)
    while i > 0:
        res_str1 += str1[i - 1]
        res_str2 += "_"
        i -= 1
    while j > 0:
        res_str1 += "_"
        res_str2 += str2[j - 1]
        j -= 1

    cost_of_align = opt[len(str1)][len(str2)]
    return res_str1[::-1], res_str2[::-1], cost_of_align

# Time wrapper
def seq_align_basic(str1, str2, delta, alpha):
    start_time = time.time()
    opt_str1, opt_str2, cost = basic(str1, str2, delta, alpha)
    end_time = time.time()
    total_time = round((end_time - start_time) * 1000, 3)
    return opt_str1, opt_str2, cost, total_time

# Measure memory with psutil
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_kb = int(memory_info.rss / 1024)
    return memory_kb

# Output to file
def write_output(path, opt_sol, memory_kb):
    cost, str1, str2, time_taken = opt_sol[2], opt_sol[0], opt_sol[1], opt_sol[3]
    content = f"{cost}\n{str1}\n{str2}\n{time_taken}\n{memory_kb}"
    with open(path, "w") as file:
        file.write(content)

# Main entry
if __name__ == '__main__':
    delta = 30
    alpha = {
        "A": {"A": 0,   "C": 110, "G": 48,  "T": 94},
        "C": {"A": 110, "C": 0,   "G": 118, "T": 48},
        "G": {"A": 48,  "C": 118, "G": 0,   "T": 110},
        "T": {"A": 94,  "C": 48,  "G": 110, "T": 0}
    }

    if len(sys.argv) != 3:
        print("Usage: python3 basic_3.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    string_1, string_2 = generate_strings(input_path)
    opt_sol = seq_align_basic(string_1, string_2, delta, alpha)
    memory_kb = process_memory()
    write_output(output_path, opt_sol, memory_kb)
