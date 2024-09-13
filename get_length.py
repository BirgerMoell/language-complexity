def analyze_text(text):
    # Split the text into words
    words = text.split()
    
    # Count total words
    word_count = len(words)
    
    # Count sentences (assuming sentences end with '.', '!', or '?')
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    # Count long words (more than 8 characters)
    long_word_count = sum(1 for word in words if len(word) > 6)
    
    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'long_word_count': long_word_count
    }

def analyze_files_in_folder(folder_path, output_file):
    import os
    import csv

    results = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                analysis = analyze_text(text)
                analysis['file_name'] = file
                results.append(analysis)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_name', 'word_count', 'sentence_count', 'long_word_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

# Example usage:
analyze_files_in_folder('data_short', 'text_analysis_results.csv')
