import os
import csv
from groq import Groq
from dotenv import load_dotenv
from tqdm import tqdm

# Initialize Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = ["llama-3.2-90b-text-preview"]

LIX_PROMPT = "Analyze the following Swedish text and compute a LIX readibility score from it. LIX is calculated as follows: (number of words)/(number of sentences)+(number of words longer than 6 letters)*100/(number of words). Use a calculator and explain how you got your result. Finally, write the result on the form 'LIX=' followed by the score. Here is the text: {text}"

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

    
def calculate_lix_with_model(text, model):
    return call_groq_api(LIX_PROMPT.format(text=text), model)

    
def process_long_sentences():
    skip = True
    with open( "c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            filename = row[0].replace('\\','/')
            if filename == 'f137.txt':
                skip = False
            if skip:
                continue
            text = row[1]
            for model in models:
                os.makedirs(f'c:/GitHub/birger/language-complexity/data100/lix_raw_data/long_prompt/{model}/', exist_ok=True)
                parse_results = calculate_lix_with_model(text,model)
                with open(f'c:/GitHub/birger/language-complexity/data100/lix_raw_data/long_prompt/{model}/{filename}', 'w', newline='', encoding='utf-8') as f:
                    f.write( parse_results )
                    print( filename )


if __name__ == "__main__":
    process_long_sentences()
