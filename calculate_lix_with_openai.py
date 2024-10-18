from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm
import os
import csv

load_dotenv()


# Hämta API-nyckeln från miljövariabeln
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")


open_ai_client = OpenAI(
    api_key=OPEN_AI_API_KEY,
)

#models = ["gpt-3.5-turbo"]
models = ["o1-mini"]

LIX_PROMPT = "Analyze the following Swedish text and compute a LIX readibility score from it. Use a calculator and explain how you got your result. Finally, write the result on the form 'LIX=' followed by the score. Here is the text: {text}"

def get_text_from_open_ai(prompt, model):
    completion = open_ai_client.chat.completions.create(
        model=model,
        messages=[
            #{"role": "system", "content": "You are a world class expert on computational linguistics. Answer in a concise and accurate way."},
            #{"role": "system", "content": "You are a world class expert on computational linguistics. Before giving your final answer, explain how you reasoned to obtain the answer."},
            {"role": "user", "content": prompt}
        ]
    )
    text = completion.choices[0].message.content
    return text



def process_long_sentences():
    # Ensure the results directory exists
    os.makedirs('c:/GitHub/birger/language-complexity/data100/lix_raw_data/diva', exist_ok=True)
    
    with open( "c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            filename = row[0].replace('\\','/')
            text = row[1]
            for model in models:
                parse_results = get_text_from_open_ai(LIX_PROMPT.format(text=text), model)
                with open(f'c:/GitHub/birger/language-complexity/data100/lix_raw_data/{filename}_{model}', 'w', newline='', encoding='utf-8') as f:
                    f.write( parse_results )
                    print( filename )

if __name__ == "__main__":
    process_long_sentences()
