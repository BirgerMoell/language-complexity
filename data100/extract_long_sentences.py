import csv

with open( "c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        filename = row[0].replace('\\','/')
        string = row[3]
        print( filename, string )


#os.makedirs('c:/GitHub/birger/language-complexity/data100/long_sentences', exist_ok=True)


