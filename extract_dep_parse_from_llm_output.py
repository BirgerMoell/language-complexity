import re

def extract_triples(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    pattern = r'\((\d+,\s*\S+,\s*\d+)\)'
    matches = re.findall(pattern, content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        for match in matches:
            print(match.strip() + '\n')
            file.write(match.strip() + '\n')

import os

# Replace with the actual path to your directory
directory = 'c:/GitHub/birger/language-complexity/data100/dep_parse_results/gemini-pro'

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        if os.path.isfile(file_path):
            extract_triples(file_path)
