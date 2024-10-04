import os

def add_parentheses(content):
    lines = content.split('\n')
    modified_lines = ['(' + line + ')' if line.strip() else line for line in lines]
    return '\n'.join(modified_lines)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                modified_content = add_parentheses(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)

# Process diva and mimers_brunn directories
diva_dir = os.path.join('data100', 'ground_truth', 'diva')
mimers_brunn_dir = os.path.join('data100', 'ground_truth', 'mimers_brunn')

process_directory(diva_dir)
process_directory(mimers_brunn_dir)

print("Files in diva and mimers_brunn directories have been processed.")
