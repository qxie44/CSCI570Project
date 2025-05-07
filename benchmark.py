import time
import psutil
from basic_3 import seq_align_basic, process_memory  

# Values of M + N 
total_lengths = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1536, 2048, 2560, 3072, 3584, 3968]

# Alignment parameters
delta = 30
alpha = {"A": {"A": 0, "C": 110, "G": 48, "T": 94},
         "C": {"A": 110, "C": 0, "G": 118, "T": 48},
         "G": {"A": 48, "C": 118, "G": 0, "T": 110},
         "T": {"A": 94, "C": 48, "G": 110, "T": 0}}

# This generates synthetic strings to test the total length
import random
def generate_random_dna_string(length):
    return ''.join(random.choices(['A', 'C', 'G', 'T'], k=length))


print("M+N\tTime in MS (Basic)\tMemory in KB (Basic)")

for total in total_lengths:
    len1 = total // 2
    len2 = total - len1
    str1 = generate_random_dna_string(len1)
    str2 = generate_random_dna_string(len2)

    # Time and memory
    start_time = time.time()
    aligned1, aligned2, cost = seq_align_basic(str1, str2, delta, alpha)[:3]
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000

    memory_kb = process_memory()

    print(f"{total}\t{time_taken_ms:.2f}\t\t\t{memory_kb}")
