from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm
import os

load_dotenv()


# Hämta API-nyckeln från miljövariabeln
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")


open_ai_client = OpenAI(
    api_key=OPEN_AI_API_KEY,
)

models = ["gpt-3.5-turbo"]

PARSE_PROMPT = "Analyze the following Swedish sentence and produce a dependency tree from it. For example, the sentence 'Han köper en bok' should result in the following output: [(1, Han, 2), (2, köper, 0), (3, en, 4), (4, bok, 2)], where the first number in each triple is the token index, the second entry is the token itself, and the final number is the index of the head token. Don't forget that punctuation marks like commas, full stops, question marks etc. should be tokens as well. Here is the sentence: {text}"

def get_text_from_open_ai(prompt, model="gpt-3.5-turbo"):
    completion = open_ai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a world class expert on computational linguistics. Answer in a concise and accurate way."},
            {"role": "user", "content": prompt}
        ]
    )
    text = completion.choices[0].message.content
    return text

def process_long_sentences():
    # Ensure the results directory exists
    os.makedirs('c:/GitHub/birger/language-complexity/dep_parse_results', exist_ok=True)
    
    long_sentences_dir = "c:/GitHub/birger/language-complexity/long_sentences"
    subdirs = ['diva_short', 'mimers_brunn_short']
    
    for subdir in subdirs:
        subdir_path = os.path.join(long_sentences_dir, subdir)
        for filename in tqdm(os.listdir(subdir_path), desc=f"Processing {subdir}"):
            if filename.endswith('.txt'):
                filepath = os.path.join(subdir_path, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    for model in models:
                        file_results = get_text_from_open_ai(PARSE_PROMPT.format(text=text), model)

                with open(f'c:/GitHub/birger/language-complexity/dep_parse_results/{filename}_{model}', 'w', newline='', encoding='utf-8') as f:
                    f.write( file_results )
    

if __name__ == "__main__":
    process_long_sentences()
