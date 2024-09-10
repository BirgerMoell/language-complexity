import stanza
import pandas as pd
import numpy as np
import os
from tqdm import tqdm

# Download the Swedish language model if not already downloaded
stanza.download('sv')

# Initialize the Swedish pipeline
nlp = stanza.Pipeline('sv')

def calculate_average_dependency_distance(text):
    if not isinstance(text, str):
        return None  # Return None for non-string inputs
    
    # Parse the text
    doc = nlp(text)
    
    dependencies = []
    
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.head != 0:  # Skip root word
                dependencies.append((word.id, word.head))
    
    # Calculate average dependency distance
    total_distance = sum(abs(head - dependent) for dependent, head in dependencies)
    average_distance = total_distance / len(dependencies) if dependencies else 0.0
    
    return average_distance

def process_files(directory):
    results = []
    
    # Get all text files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    for filename in tqdm(files, desc="Processing files"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        
        add_score = calculate_average_dependency_distance(text)
        
        results.append({
            'filename': filename,
            'add_score': add_score
        })
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    input_directory = "data/diva/"
    output_file = "results/add_analysis.csv"
    
    # Process all files
    df = process_files(input_directory)
    
    # Sort by ADD score in descending order
    df = df.sort_values('add_score', ascending=False)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")