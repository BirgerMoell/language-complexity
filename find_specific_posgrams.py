import os
import csv
from collections import defaultdict

models = ["gemini-pro", "llama-3.2-90b-text-preview", "gpt-4o-mini", "o1-mini", "gemini-2.0-flash-thinking-exp"]
postags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "NOUN", "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "VERB"]

input_dir = "c:/GitHub/birger/language-complexity/data100/ground_truth_with_postags/"
test_dir = f"c:/GitHub/birger/language-complexity/data100/dep_parse_results/"


def match_head_word(word, lines):
    for line in lines:
        fields = line.split(",")
        if word.strip() in fields:
            head_id = fields[2]
            return find_head(head_id, lines)
    return None

def find_head( head_id, lines):
    for line in lines:
        fields = line.split(",")
        if fields[0].strip() == head_id.strip():
            return fields[1]
    return None

def match_head_of_pattern(postag, input_lines, test_lines, matching_dict, tested_dict):
    for line in input_lines:
        fields = line.split(",")
        if postag in fields:
            word = fields[1]
            head = fields[3]
            head_word = find_head(head, input_lines)
            if head_word:
                tested_dict[postag] += 1
                predicted_head_word = match_head_word(word,test_lines)
                matching_dict[postag] += head_word == predicted_head_word
            
def get_lines_from_file(path) :
    input_lines = []
    with open(path, "r", encoding="utf-8") as f1:
        for line in f1:
            input_lines.append( line.replace(" ","") )
        f1.close()
        return input_lines 
    
matching = {}
tested = {}
for root, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.txt'):
            print( file )
            input_path = os.path.join( input_dir, file )
            input_lines =  get_lines_from_file( input_path )
            for model in models:
                if model not in matching:
                    matching[model] = defaultdict(int)
                if model not in tested:
                    tested[model] = defaultdict(int)
                test_path = os.path.join( test_dir, model, f"{file}_{model}" )
                if not os.path.exists(test_path):
                    continue
                test_lines = get_lines_from_file( test_path )
                for postag in postags:
                    match_head_of_pattern( postag, input_lines, test_lines, matching[model], tested[model] )
                    
total_matching = {}
total_tested = {}
macro_total = {}
for model in models:
    total_matching[model] = 0
    total_tested[model] = 0
    macro_total[model] = 0
    for postag in matching[model]:
        total_matching[model] += matching[model][postag]
        total_tested[model] += tested[model][postag]
        macro_total[model] += (matching[model][postag]/tested[model][postag])
        print( f'Model {model}, postag {postag}: {(matching[model][postag]/tested[model][postag]):.2f}' )

for model in models:
    print( "Micro-accuracy,", model, ":", f'{total_matching[model]/total_tested[model]:.2f}' )
    print( "Macro-accuracy,", model, ":", f'{macro_total[model]/len(postags):.2f}' )

                

