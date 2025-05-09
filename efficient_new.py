import time
import sys
import psutil

from generate import generate_strings
from basic_new import basic  # fallback when string length is 1

# Gap penalty
delta = 30

# Mismatch penalty table
alpha = {
    "A": {"A": 0,   "C": 110, "G": 48,  "T": 94},
    "C": {"A": 110, "C": 0,   "G": 118, "T": 48},
    "G": {"A": 48,  "C": 118, "G": 0,   "T": 110},
    "T": {"A": 94,  "C": 48,  "G": 110, "T": 0}
}

# Compute last row of DP matrix using only linear space
def row_cost(x, y):
    m, n = len(x), len(y)
    prev = [i * delta for i in range(n + 1)]
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i * delta
        for j in range(1, n + 1):
            cost = alpha[x[i - 1]][y[j - 1]]
            curr[j] = min(
                prev[j - 1] + cost,
                prev[j] + delta,
                curr[j - 1] + delta
            )
        prev, curr = curr, [0] * (n + 1)

    return prev

# Hirschberg algorithm: divide and conquer
def efficient_alignment(x, y):
    if len(x) == 0:
        return "_" * len(y), y
    if len(y) == 0:
        return x, "_" * len(x)
    if len(x) == 1 or len(y) == 1:
        aligned_x, aligned_y, _ = basic(x, y, delta, alpha)
        return aligned_x, aligned_y  # ✅ 修正点：不要再反转！

    x_mid = len(x) // 2
    score_left = row_cost(x[:x_mid], y)
    score_right = row_cost(x[x_mid:][::-1], y[::-1])

    y_split = min(
        range(len(y) + 1),
        key=lambda j: score_left[j] + score_right[len(y) - j]
    )

    leftA, leftB = efficient_alignment(x[:x_mid], y[:y_split])
    rightA, rightB = efficient_alignment(x[x_mid:], y[y_split:])
    return leftA + rightA, leftB + rightB

# Alignment wrapper with timer
def seq_align_efficient(str1, str2):
    start_time = time.time()
    opt_str1, opt_str2 = efficient_alignment(str1, str2)
    end_time = time.time()

    cost = sum(
        delta if a == '_' or b == '_' else alpha[a][b]
        for a, b in zip(opt_str1, opt_str2)
    )
    total_time = round((end_time - start_time) * 1000, 3)  # in ms
    return opt_str1, opt_str2, cost, total_time

# Use psutil to get actual memory in KB
def get_memory_kb():
    process = psutil.Process()
    return int(process.memory_info().rss / 1024)

# Output result to file
def write_output(path, opt_sol, memory_kb):
    cost, str1, str2, time_taken = opt_sol[2], opt_sol[0], opt_sol[1], opt_sol[3]
    content = f"{cost}\n{str1}\n{str2}\n{time_taken}\n{memory_kb}"
    with open(path, "w") as file:
        file.write(content)

# Main CLI entry
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 efficient_3.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    string_1, string_2 = generate_strings(input_path)
    opt_sol = seq_align_efficient(string_1, string_2)
    memory_kb = get_memory_kb()
    write_output(output_path, opt_sol, memory_kb)

