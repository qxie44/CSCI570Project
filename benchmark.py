import time
import psutil
import os
from generate import generate_strings
from basic_3 import seq_align_basic, process_memory  
from efficient_3 import seq_align_efficient

#folder w the datapoints
datapoints_folder = 'CSCI570_Project_Minimum_V1/datapoints'

# Alignment parameters
delta = 30
alpha = {"A": {"A": 0, "C": 110, "G": 48, "T": 94},
         "C": {"A": 110, "C": 0, "G": 118, "T": 48},
         "G": {"A": 48, "C": 118, "G": 0, "T": 110},
         "T": {"A": 94, "C": 48, "G": 110, "T": 0}}

input_files = sorted([f for f in os.listdir(datapoints_folder) if f.startswith('in') and f.endswith('.txt')],
                     key=lambda x: int(x[2:-4]))

#table format

print("M+N\tTime in MS (Basic)\tMemory in KB (Basic)\tTime in MS (Efficient)\tMemory in KB (Efficient)")

for file in input_files:
    path = os.path.join(datapoints_folder, file)
    str1, str2 = generate_strings(path)
    m_plus_n = len(str1) + len(str2)

    # basic alg
    start_time = time.time()
    _ = seq_align_basic(str1, str2, delta, alpha)
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    memory_kb = process_memory()

    # efficient alg
    start_time = time.time()
    _ = seq_align_efficient(str1, str2)
    end_time_eff = time.time()
    time_taken_ms_eff = (end_time_eff - start_time) * 1000
    memory_kb_eff = process_memory()

    print(f"{file}\t{m_plus_n}\t{time_taken_ms:.2f}\t{memory_kb}\t{time_taken_ms_eff:.2f}\t{memory_kb_eff}")