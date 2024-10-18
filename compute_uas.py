import os
import csv
import statistics

ground_truth_dir = 'c:/GitHub/birger/language-complexity/data100/ground_truth'
input_dir = 'c:/GitHub/birger/language-complexity/data100/dep_parse_results/gemini-pro'
output_file = 'c:/GitHub/birger/language-complexity/data100/uas_results_gemini-pro.csv'

def count_matching_lines(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        
    matching_lines = 0
    total_lines = 0
    i, j = 0, 0
    while i < len(lines1) and j < len(lines2):
        l1, l2 = lines1[i].strip(), lines2[j].strip()
        
        if not l1:
            i += 1
            continue
        if not l2:
            j += 1
            continue
        
        cols1 = l1.split(',')
        cols2 = l2.split(',')
        if len(cols1) == 3 and len(cols2) == 3:
            if cols1[0] == cols2[0] and cols1[2] == cols2[2]:
                matching_lines += 1
            total_lines += 1
        
        i += 1
        j += 1
    
    return matching_lines, total_lines

results = []

for filename in os.listdir(ground_truth_dir):
    ground_truth_file = os.path.join(ground_truth_dir, filename)
    input_file = os.path.join(input_dir, f"{filename}_gemini-pro")
    
    if os.path.isfile(ground_truth_file) and os.path.isfile(input_file):
        print( input_file )
        matching, total = count_matching_lines(ground_truth_file, input_file)
        uas = matching / total if total > 0 else 0
        results.append((filename, matching, total, uas))

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Filename', 'Matching Lines', 'Total Lines', 'UAS'])
    writer.writerows(results)

print(f"Results have been written to {output_file}")

# Calculate and print the average UAS
average_uas = statistics.mean([result[3] for result in results])
print(f"Average UAS across all files: {average_uas:.4f}")
