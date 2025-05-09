import os
import subprocess
import time
from generate import generate_strings

# 配置
datapoints_dir = "CSCI570_Project_Minimum_V1/datapoints"
basic_script = "basic_new.py"
efficient_script = "efficient_new.py"

# 输出表头
print(f"{'File':<10} {'M+N':<6} {'Time Basic (ms)':<15} {'Mem Basic (KB)':<15} {'Time Eff (ms)':<15} {'Mem Eff (KB)':<15}")

# 遍历 input 文件
input_files = sorted(
    [f for f in os.listdir(datapoints_dir) if f.startswith("in") and f.endswith(".txt")],
    key=lambda x: int(x[2:-4])
)

for file in input_files:
    input_path = os.path.join(datapoints_dir, file)
    out_basic = f"out_basic_{file}"
    out_eff = f"out_efficient_{file}"

    # basic run
    subprocess.run(["python3", basic_script, input_path, out_basic])
    # efficient run
    subprocess.run(["python3", efficient_script, input_path, out_eff])

    # 获取 M+N
    s1, s2 = generate_strings(input_path)
    total_len = len(s1) + len(s2)

    # 读取 basic 输出时间/内存
    with open(out_basic, "r") as f:
        lines = f.readlines()
        time_b = float(lines[3].strip())
        mem_b = int(lines[4].strip())

    # 读取 efficient 输出时间/内存
    with open(out_eff, "r") as f:
        lines = f.readlines()
        time_e = float(lines[3].strip())
        mem_e = int(lines[4].strip())

    print(f"{file:<10} {total_len:<6} {time_b:<15} {mem_b:<15} {time_e:<15} {mem_e:<15}")
