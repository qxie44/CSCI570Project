import sys

def generate_strings(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    s1 = lines[0]

    def is_int(s):
        try:
            int(s)
            return True
        except:
            return False
    #s2 after ending of numbers
    s2_start = None
    for i in range(1, len(lines)):
        if not is_int(lines[i]):
            s2_start = i
            break

    s1_indices = list(map(int, lines[1:s2_start]))
    s2 = lines[s2_start]
    s2_indices = list(map(int, lines[s2_start + 1:]))

    def full_sequence(base, indices):
        for i, idx in enumerate(indices):
            #inserting after index
            base = base[:idx + 1] + base + base[idx + 1:]
        return base

    return full_sequence(s1, s1_indices), full_sequence(s2, s2_indices)

if __name__ == "__main__":
    input_file = sys.argv[1]
    s1, s2 = generate_strings(input_file)
    #can remove, just printing for testing
    print("String 1:", s1)
    print("String 2:", s2)
