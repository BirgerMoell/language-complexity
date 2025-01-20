import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Check if the API key is set in the environment
if "GENAI_API_KEY" not in os.environ:
    raise ValueError("GENAI_API_KEY environment variable is not set. Please set it in your .env file or system environment.")

genai.configure(api_key=os.environ["GENAI_API_KEY"])

PARSE_PROMPT = "Analyze the following Swedish sentence and produce a dependency tree from it. For example, the sentence 'Han köper en bok' should result in the following output: [(1, Han, 2), (2, köper, 0), (3, en, 4), (4, bok, 2)], where the first number in each triple is the token index, the second entry is the token itself, and the final number is the index of the head token. Don't forget that punctuation marks like commas, full stops, question marks etc. should be tokens as well. Finally, compute the average dependency distance for the sentence.Here is the sentence: {text}"

models = ['gemini-2.0-flash-thinking-exp']

def get_text_from_gemini(prompt, modelname):
    try:
        model = genai.GenerativeModel(modelname)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None

def process_long_sentences():
    # Ensure the results directory exists
    os.makedirs('c:/GitHub/birger/language-complexity/data100/dep_parse_raw_data/', exist_ok=True)
    
    with open("c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            filename = row[0].replace('diva\\','')
            text = row[3]
            for model in models:
                parse_results = get_text_from_gemini(PARSE_PROMPT.format(text=text), model)
                if parse_results:
                    with open(f'c:/GitHub/birger/language-complexity/data100/dep_parse_raw_data/{filename}_{model}', 'w', newline='', encoding='utf-8') as f:
                        f.write(parse_results)
                        print(filename)
                else:
                    print(f"Failed to generate content for {filename}")

if __name__ == "__main__":
    try:
        process_long_sentences()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
