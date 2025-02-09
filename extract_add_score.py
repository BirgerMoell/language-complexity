import os
import re
import csv

model = "gemini-2.0-flash-thinking-exp"
input_dir = f'c:/GitHub/birger/language-complexity/data100/dep_parse_raw_data/{model}'
output_file = f'c:/GitHub/birger/language-complexity/data100/add_results_{model}.csv'

results = []

for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                match = re.search(r'\d+\.\d+', last_line)
                if match:
                    number = float(match.group())
                    results.append((filename, number))

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Filename', 'Extracted Number'])
    writer.writerows(results)

print(f"Results have been written to {output_file}")
