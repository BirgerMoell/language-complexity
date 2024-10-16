import os
import csv
from groq import Groq
from dotenv import load_dotenv
from tqdm import tqdm

# Initialize Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = ["llama-3.2-90b-text-preview"]

ADD_PROMPT = "Analyze the following Swedish sentence and calculate the average dependency distance from it. For example, in the sentence 'Han köper en bok', the average dependency distance is 4/3=1.33, since the distance from 'Han' to its head 'köper' is 1, from 'bok' to its head 'köper' is 2, and the distance from 'en' to its head 'bok' is 1. Don't forget that punctuation marks like commas, full stops, question marks etc. should be tokens as well. Here is the sentence: {text}"

def call_groq_api(prompt, model):
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {str(e)}")
        return None

    
def compute_add_with_model(text, model):
    return call_groq_api(ADD_PROMPT.format(text=text), model)

    
def process_long_sentences():
    # Ensure the results directory exists
    os.makedirs('c:/GitHub/birger/language-complexity/data100/add_raw_data/', exist_ok=True)
    
    with open( "c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        skip = True
        for row in reader:
            filename = row[0].replace('diva\\','')
            #if skip and filename != 'mimers_brunn/f6.txt':
            #    continue
            #else:
            #    skip = False
            text = row[3]
            if not text:
                continue
            for model in models:
                add_results = compute_add_with_model(text,model)
                with open(f'c:/GitHub/birger/language-complexity/data100/add_raw_data/{filename}_{model}', 'w', newline='', encoding='utf-8') as f:
                    f.write( add_results )
                    print( filename )


if __name__ == "__main__":
    process_long_sentences()
