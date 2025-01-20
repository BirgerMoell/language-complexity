import os
import csv

extracted_paragraphs_path = 'c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv'
results_path = 'c:/GitHub/birger/language-complexity/data100/'
output_file = 'c:/GitHub/birger/language-complexity/data100/lix_values.csv'

textnames = []
lix_dict = {}

with open(extracted_paragraphs_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if len(row) >= 3 and row[2].replace('.', '', 1).isdigit():
            textname = os.path.basename(row[0]).strip()
            textnames.append( textname )
            lix_dict[textname.strip()] = {}
            ground_truth = float(os.path.basename(row[2]))
            lix_dict[textname]['ground_truth'] = ground_truth

models = ['llama', 'gemini-pro', 'gpt-4o-mini', 'o1-mini']

for model in models:
    file_path = os.path.join(results_path, 'lix_results_' + model + '.txt')
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as in_file:
            for content in in_file:
                try :
                    content_list = content.split(',')
                    if len(content_list) == 2:
                        textname = content_list[0].strip()
                        r = float(content_list[1])
                        lix_dict[textname][model] = r
                        diff = abs(r-lix_dict[textname]['ground_truth'])
                        lix_dict[textname][model+'_diff'] = f"{diff:.2f}"
                except ValueError:
                    continue
                except KeyError:
                    continue


                                        
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    header = ['Text', 'Ground truth']
    for model in models:
        header.append( model )
        header.append( model+' diff' )
    writer.writerow(  header )
    for text in textnames:
        row = [text, lix_dict[text]['ground_truth']]
        for model in models:
            row.append( lix_dict[text].get(model, '') )
            row.append( lix_dict[text].get(model+'_diff', '') )
        writer.writerow( row )
        print( row )
