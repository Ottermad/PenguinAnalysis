import os

# List all files in directories
filenames = os.listdir()
firstlines = []

# For each file
for filename in filenames:
    # If file is CSV
    if filename[-4:] == ".csv":
        with open(filename) as f:
            firstline = f.readline()
            firstlines.append(firstline.strip("\n").strip(" ").strip(","))

unique_first_lines = set(firstlines)
print(unique_first_lines)
