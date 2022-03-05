# CPSC 450 - Bioinformatics
# Isayha Raposo - 230133508
# Assignment 3 - Longest Common Subsequence Problem

from sys import argv, exit
from os import path

# Global Variables:
bases = ['A', 'T', 'C', 'G']

dna_str_1 = None
dna_str_2 = None
str_len_1 = None
str_len_2 = None
dp_table = None

max_len = 0

# Returns the two (2) DNA strings found within the user-specified data file
def process_data_file(data_file_name):
    data_file = open(data_file_name, 'r')
    dna_strs = []
    for _ in range(0, 2):
        dna_str = data_file.readline().strip()
        for base in dna_str.upper():
            if base not in bases:
                print("ERROR: Invalid DNA string specified (Invalid base/nucleotide specified).")
                exit(0)
        dna_strs.append(dna_str)
    if len(dna_strs) != 2:
        print("ERROR: Invalid quantity of DNA strings specified. See assignment details.")
        exit(0)
    return dna_strs

# Prints string to the console in addition to writing string to output_file
def print_and_write(output_file, string):
    print(string)
    output_file.write(string + '\n')

# Initializes global variables with values unpacked from dna_strs, 
# including the memoization table
def init_global_vars(dna_strs):
    global dna_str_1
    global dna_str_2
    global str_len_1
    global str_len_2
    global dp_table

    dna_str_1 = dna_strs[0]
    dna_str_2 = dna_strs[1]
    str_len_1 = len(dna_str_1)
    str_len_2 = len(dna_str_2)
    dp_table = [[0] * (str_len_2 + 1) for _ in range(str_len_1 + 1)]

    # Initializes the memoization table
    for row in range(str_len_1):
        for col in range(str_len_2):
            if dna_str_1[row] == dna_str_2[col]:
                dp_table[row + 1][col + 1] = dp_table[row][col] + 1
            else:
                dp_table[row + 1][col + 1] = max(dp_table[row][col + 1], dp_table[row + 1][col]) 

# Prints the memoization table
def print_dp_table():
    if dp_table is not None:

        col_header = ' ' * 6
        for _ in range(str_len_2):
            col_header += dna_str_2[_] + (' ' * 2)
        print(col_header)

        row_header = " " + dna_str_1
        
        for _ in range(str_len_1 + 1):
            print(row_header[_], dp_table[_])

# Obtains and returns ALL possible longest common subsequences (LCSs) via recursive
# logic additional to the usual dynamic programming logic
    # IMPORTANT: The LCSs returned are BACKWARDS due to the traversal method used
def get_LCSs(row=0, col=0, LCSs=[""]):
    global max_len

    # Returns the current solution if the row or the column value(s) is/are about to exceed the size of dp_table
    if row == str_len_1 or col == str_len_2:
        return LCSs

    # Handles cases where the current comparison characters are identical
        # Recursively calls get_LCSs for the next set of comparison characters
            # Returns the list of subsequences returned by said recursive call...
    if dna_str_1[row] == dna_str_2[col]:
        LCSs = get_LCSs(row + 1, col + 1)

        # ...with the current comparison character appended to each element...
        LCSs = [_ + dna_str_1[row] for _ in LCSs]

        # ...and with subsequence(s) of length(s) less than that defined by max_len removed...
        max_len = max(len(_) for _ in LCSs)
        LCSs = [_ for _ in LCSs if len(_) == max_len]

        # ...and with duplicate subsequence(s) removed...
        return list(set(LCSs))

    # Handles cases where the current comparison characters are NOT identical
    # Handles cases where the next character in DNA string 2 matches the current character from DNA string 1 but NOT vice versa"
    if dp_table[row][col + 1] > dp_table[row + 1][col]:
        return get_LCSs(row, col + 1, LCSs)
    # Handles cases where the next character in DNA string 1 matches the current character from DNA string 2 but NOT "vice versa"
    elif dp_table[row][col + 1] < dp_table[row + 1][col]:
        return get_LCSs(row + 1, col, LCSs)
    # Handles "vice versa" cases (creates two (2) recursive branches to check BOTH character incrementation options)...
    else:
        LCSs = get_LCSs(row, col + 1, LCSs) + get_LCSs(row + 1, col, LCSs)

        # ...with subsequence(s) of length(s) less than that defined by max_len removed...
        max_len = max(len(_) for _ in LCSs)
        LCSs = [_ for _ in LCSs if len(_) == max_len]

        # ...and with duplicate subsequence(s) removed...
        return list(set(LCSs))

def main():
    arg_count = len(argv)
    if arg_count < 2:
        print("ERROR: No command line argument provided. See README.md.")
        exit(1)

    data_file_name = argv[1]
    if not path.isfile(data_file_name):
        print("ERROR: Specified data file " + data_file_name + " not found. See README.md.")
        exit(1)
    
    dna_strs = process_data_file(data_file_name)

    print("Specified data file found and processed:", "\nDNA String 1 =", dna_strs[0], "\nDNA String 2 =", dna_strs[1], '\n')

    #
    # Solution Logic:
    #

    init_global_vars(dna_strs)

    print("Memoization Table Generated:")
    print_dp_table()
    print()

    solutions_backwards = get_LCSs()
    solutions = [_[::-1] for _ in solutions_backwards]

    #
    # Output Logic:
    #

    output_file_name = data_file_name.split(".txt")[0] + "_output.txt"
    output_file = open(output_file_name, "w")

    print_and_write(output_file, "Solutions: ")
    for solution in solutions:
        print_and_write(output_file, solution)

    print("\nThese solutions have been written to " + output_file_name)

if __name__ == "__main__":
    main()