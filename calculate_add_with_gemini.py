import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Check if the API key is set in the environment
if "GENAI_API_KEY" not in os.environ:
    raise ValueError("GENAI_API_KEY environment variable is not set. Please set it in your .env file or system environment.")

genai.configure(api_key=os.environ["GENAI_API_KEY"])

models = ["gemini-pro"]

ADD_PROMPT = "Analyze the following Swedish sentence and calculate the average dependency distance from it. For example, in the sentence 'Han köper en bok', the average dependency distance is 4/3=1.33, since the distance from 'Han' to its head 'köper' is 1, from 'bok' to its head 'köper' is 2, and the distance from 'en' to its head 'bok' is 1. Don't forget that punctuation marks like commas, full stops, question marks etc. should be tokens as well. Here is the sentence: {text}"


def get_text_from_gemini(prompt, modelname):
    try:
        model = genai.GenerativeModel(modelname)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None

def process_long_sentences():
    with open("c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            filename = row[0].replace('diva\\','')
            text = row[1]
            for model in models:
                os.makedirs(f'c:/GitHub/birger/language-complexity/data100/add_raw_data/{model}/', exist_ok=True)
                parse_results = get_text_from_gemini(ADD_PROMPT.format(text=text), model)
                if parse_results:
                    with open(f'c:/GitHub/birger/language-complexity/data100/add_raw_data/{model}/{filename}', 'w', newline='', encoding='utf-8') as f:
                        f.write(parse_results)
                        print(filename)
                else:
                    print(f"Failed to generate content for {filename}")

if __name__ == "__main__":
    try:
        process_long_sentences()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
