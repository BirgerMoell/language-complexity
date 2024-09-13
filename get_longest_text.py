import os
import re

def get_longest_sentence(text):
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Return the longest sentence
    return max(sentences, key=len) if sentences else ""

def process_files(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Walk through the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                # Construct full file paths
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                
                # Create subdirectory in output if it doesn't exist
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                
                output_path = os.path.join(output_subdir, file)

                # Read the input file
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Get the longest sentence
                longest_sentence = get_longest_sentence(content)

                # Write the longest sentence to the output file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(longest_sentence)

# Usage
input_directory = 'data_short'
output_directory = 'long_sentences'
process_files(input_directory, output_directory)
