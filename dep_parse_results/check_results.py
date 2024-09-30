def read_triples_from_file(filename):
    triples = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                line = line.strip()  # Remove leading/trailing whitespace and newline
                if line:  # Skip empty lines
                    triple_str = line.strip('()')  # Remove parentheses
                    elements = triple_str.split(', ')  # Split into elements
                    triple = (int(elements[0]), str(elements[1]), int(elements[2]))
                    triples.append(triple)
            except ValueError:
                continue
    return triples


def compute_uas( truth, parse ):
    correct = 0
    for i in range(min(len(truth),len(parse))):
        (_,_,a) = truth[i]
        (_,_,b) = parse[i]
        if a==b:
            correct += 1
    return correct/len(truth)


filenames = ['diva_short_1.txt',
             'diva_short_2.txt',
             'diva_short_3.txt',
             'diva_short_4.txt',
             'diva_short_5.txt',
             'mimers_brunn_short_1.txt',
             'mimers_brunn_short_2.txt',
             'mimers_brunn_short_3.txt',
             'mimers_brunn_short_4.txt',
             'mimers_brunn_short_5.txt'
             ]


results = []
for name in filenames:
    truth = read_triples_from_file(f'c:/GitHub/birger/language-complexity/dep_parse_ground_truth/{name}')
    parse = read_triples_from_file(f'c:/GitHub/birger/language-complexity/dep_parse_results/{name}_llama-3.2-90b-text-preview')
    results.append( compute_uas(truth, parse) )
print( sum(results)/len(results) )
    
             



