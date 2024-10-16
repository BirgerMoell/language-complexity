import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Check if the API key is set in the environment
if "GENAI_API_KEY" not in os.environ:
    raise ValueError("GENAI_API_KEY environment variable is not set. Please set it in your .env file or system environment.")

genai.configure(api_key=os.environ["GENAI_API_KEY"])

LIX_PROMPT = "Analyze the following Swedish text and compute a LIX readibility score from it. Use a calculator and explain how you got your result. Finally, write the result on the form 'LIX=' followed by the score. Here is the text: {text}"

models = ["gemini-pro"]

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
    os.makedirs('c:/GitHub/birger/language-complexity/data100/lix_raw_data/', exist_ok=True)
    
    with open("c:/GitHub/birger/language-complexity/data/extracted_paragraphs.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            filename = row[0].replace('diva\\','')
            if "103" in filename:
                return
            text = row[1]
            for model in models:
                parse_results = get_text_from_gemini(LIX_PROMPT.format(text=text), model)
                if parse_results:
                    with open(f'c:/GitHub/birger/language-complexity/data100/lix_raw_data/{filename}_{model}', 'w', newline='', encoding='utf-8') as f:
                        f.write(parse_results)
                        print(filename)
                else:
                    print(f"Failed to generate content for {filename}")

if __name__ == "__main__":
    try:
        process_long_sentences()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
