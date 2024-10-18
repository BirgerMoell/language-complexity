import csv
import os

# File paths
extracted_paragraphs_path = 'c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv'
lix_llama_results_path = 'c:/GitHub/birger/language-complexity/data100/lix_results_gemini-pro.txt'

# Dictionary to store values from extracted_paragraphs.csv
extracted_values = {}

# Read extracted_paragraphs.csv
with open(extracted_paragraphs_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if len(row) >= 3 and row[2].replace('.', '', 1).isdigit():
            filename = os.path.basename(row[0])
            #print(filename)
            extracted_values[filename] = float(row[2])

# Dictionary to store values from lix_llama_results.txt
llama_values = {}

# Read lix_llama_results.txt
with open(lix_llama_results_path, 'r', encoding='utf-8') as txt_file:
    for line in txt_file:
        parts = line.strip().split(',')
        if len(parts) >= 2:
            filename = parts[0].strip()
            #print( filename)
            lix_value = parts[-1].strip()
            if lix_value.replace('.', '', 1).isdigit():
                llama_values[filename] = float(lix_value)

# Calculate the average of absolute differences
total_diff = 0
count = 0

for filename in extracted_values.keys():
    if filename in llama_values:
        diff = abs(extracted_values[filename] - llama_values[filename])
        total_diff += diff
        count += 1

if count > 0:
    average_diff = total_diff / count
    print(f"Average absolute difference: {average_diff:.2f}")
else:
    print("No matching filenames found.")
