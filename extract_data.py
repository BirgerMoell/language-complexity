import os
import csv
import re
import stanza

def extract_paragraph(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()
        start_index = 1000
        while True:
            start_index = content.find('.', start_index)
            if start_index == -1:
                return ""
            
            paragraph = content[start_index + 1:].lstrip()
            paragraph = paragraph.split('\n\n')[0].replace('\n', ' ').strip()
            
            if len(paragraph) >= 2 and paragraph[0].isupper() and paragraph[1].islower():
                return paragraph
            
            start_index += 1

def process_files(root_dir):
    results = []
    nlp = stanza.Pipeline('sv')  # Load Swedish model
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)
                paragraph = extract_paragraph(file_path)
                truncated_paragraph = truncate_paragraph(paragraph)
                lix_score = calculate_lix(truncated_paragraph)
                longest_sentence = get_longest_sentence(truncated_paragraph)
                dependency_parse = parse_sentence(longest_sentence, nlp)
                results.append((relative_path, truncated_paragraph, lix_score, longest_sentence, dependency_parse))
    return results

def write_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File', 'Paragraph', 'LIX Score', 'Longest Sentence', 'Dependency Parse'])
        writer.writerows(results)

def truncate_paragraph(paragraph):
    if len(paragraph) <= 500:
        return paragraph
    
    truncated = paragraph[:500]
    end_index = paragraph.rfind('.', 0, 500)
    
    if end_index != -1:
        return paragraph[:end_index + 1]
    else:
        return truncated + '...'

def calculate_lix(text):
    words = re.findall(r'\w+', text)
    sentences = re.split(r'[.!?]+', text)
    long_words = [word for word in words if len(word) > 6]
    
    if len(words) == 0 or len(sentences) == 0:
        return 0
    
    words_per_sentence = len(words) / len(sentences)
    long_words_percentage = (len(long_words) / len(words)) * 100
    
    lix = words_per_sentence + long_words_percentage
    return round(lix, 2)

def get_longest_sentence(text):
    sentences = re.findall(r'[^.!?]+[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return max(sentences, key=len) if sentences else ""

def parse_sentence(sentence, nlp):
    if not sentence.strip():
        return ""
    doc = nlp(sentence)
    parse_result = [(word.id, word.text, word.head) for word in doc.sentences[0].words]
    return str(parse_result)

root_directory = 'data'
output_csv = 'extracted_paragraphs.csv'

results = process_files(root_directory)
write_to_csv(results, output_csv)

print(f"Extraction complete. Results saved to {output_csv}")
