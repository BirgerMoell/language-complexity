import os
import re

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    current_number = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(',')
        if len(parts) != 3:
            continue

        number, word, dependency = parts

        try:
            number = int(number)
            if number <= current_number:
                break
            current_number = number
        except ValueError:
            continue

        word = re.sub(r'[\'"]', '', word.strip())
        word = re.sub(r'^\(|\)$', '', word.strip())
        cleaned_line = f"{number},{word},{dependency}"
        cleaned_lines.append(cleaned_line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(cleaned_lines))

directory = 'c:/GitHub/birger/language-complexity/data100/dep_parse_results/gpt-4o-mini'

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        if os.path.isfile(file_path):
            clean_file(file_path)

print("All files have been cleaned.")
