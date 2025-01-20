import os
import csv
import stanza

nlp = stanza.Pipeline('sv')  # Load Swedish model

def parse_sentence(sentence, nlp):
    if not sentence.strip():
        return ""
    doc = nlp(sentence)
    parse_result = [(word.id, word.text, word.pos, word.head) for word in doc.sentences[0].words]
    return parse_result


with open("c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            rows = []
            filename = row[0].replace('diva\\','')
            text = row[3]
            rows.extend( parse_sentence(text, nlp) )
            with open( f"c:/GitHub/birger/language-complexity/data100/ground_truth_with_postags/{filename}", "w", encoding="utf-8") as f2:
                for r in rows:
                    for field in r:
                        f2.write( str(field) )
                        f2.write( ', ' )
                    f2.write('\n')
                    
