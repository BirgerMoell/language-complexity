import os
import csv
from groq import Groq
from dotenv import load_dotenv
from tqdm import tqdm

# Initialize Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = ["llama-3.2-1b-preview", "llama-3.2-3b-preview", "llama-3.2-11b-text-preview", "llama-3.2-90b-text-preview"]

PARSE_PROMPT = "Analyze the following Swedish sentence and produce a dependency tree from it. For example, the sentence 'Han köper en bok' should result in the following output: [(1, Han, 2), (2, köper, 0), (3, en, 4), (4, bok, 2)], where the first number in each triple is the token index, the second entry is the token itself, and the final number is the index of the head token. Don't forget that punctuation marks like commas, full stops, question marks etc. should be tokens as well. Here is the sentence: {text}"

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

    
def dep_parse_with_model(text, model):
    return call_groq_api(PARSE_PROMPT.format(text=text), model)

    
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
                        file_results = dep_parse_with_model(text,model)

                # Save results to CSV
                with open(f'c:/GitHub/birger/language-complexity/dep_parse_results/{filename}_{model}', 'w', newline='', encoding='utf-8') as f:
                    f.write( file_results )
    

if __name__ == "__main__":
    process_long_sentences()
