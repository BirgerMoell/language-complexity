import os
import csv
from llm_complexity import calculate_lix_score, interpret_lix_score

def calculate_subpart_complexity(text):
    # Take a chunk of 1000 characters and extend to the next period
    if len(text) <= 1000:
        subpart = text
    else:
        subpart = text[:1000]
        last_period = subpart.rfind('.')
        if last_period != -1:
            subpart = text[:last_period + 1]
        else:
            # If no period is found, take the whole chunk
            subpart = text[:1000]
    
    # Calculate complexity using LIX score
    lix_score = calculate_lix_score(subpart)
    complexity = interpret_lix_score(lix_score)
    
    return subpart, lix_score, complexity

def process_files(data_dir, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file', 'text', 'length', 'word_count', 'complexity_score', 'complexity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    subpart, lix_score, complexity = calculate_subpart_complexity(text)
                    word_count = len(subpart.split())

                    writer.writerow({
                        'file': file,
                        'text': subpart,
                        'length': len(subpart),
                        'word_count': word_count,
                        'complexity_score': round(lix_score, 2),
                        'complexity': complexity
                    })

if __name__ == "__main__":
    data_directory = "data"
    output_csv = "results/complexity_analysis.csv"
    
    # Ensure the results directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    process_files(data_directory, output_csv)
    print(f"Complexity analysis completed. Results saved to {output_csv}")
