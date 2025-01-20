import os
import csv
from collections import defaultdict

#models = ["gemini-pro", "llama-3.2-90b-text-preview", "gpt-4o-mini", "o1-mini"]
models = ["gemini-2.0-flash-thinking-exp"]
input_dir = "c:/GitHub/birger/language-complexity/data100/ground_truth/"
test_dir = f"c:/GitHub/birger/language-complexity/data100/dep_parse_results/"

def compute_add(lines):
    total_diff = 0
    for line in lines:
        try :
            fields = line.split(",")
            id = int(fields[0])
            head = int(fields[2])
            total_diff += abs(id-head)
        except ValueError:
            continue
        except IndexError:
            continue
    if not lines:
        return 0
    return total_diff/len(lines)

def get_lines_from_file(path) :
    input_lines = []
    with open(path, "r", encoding="utf-8") as f1:
        for line in f1:
            input_lines.append( line.replace(" ","") )
        f1.close()
        return input_lines 
    
diffs = defaultdict(int)
filecount = defaultdict(int)
for root, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.txt'):
            #print( file )
            input_path = os.path.join( input_dir, file )
            input_lines =  get_lines_from_file( input_path )
            ground_truth_add = compute_add( input_lines )
            for model in models:
                test_path = os.path.join( test_dir, model, f"{file}_{model}" )
                if not os.path.exists(test_path):
                    continue
                test_lines = get_lines_from_file( test_path )
                model_add = compute_add( test_lines )
                diffs[model] += abs(ground_truth_add-model_add)
                print( file, model_add )
                filecount[model] += 1
for model in models:
    print( "ADD difference", model, ":", f'{diffs[model]/filecount[model]:.2f}' )


                

