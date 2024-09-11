import os
import csv
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq_api(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
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

def measure_complexity(text):
    # prompt = f"""Analyze the complexity of the following text with the following formula:

    # Calculate the LIX (Läsbarhetsindex) score for Swedish text.
    
    # LIX = A + B, where:
    # A = number of words / number of sentences
    # B = (number of long words * 100) / number of words
    
    # Long words are defined as words with more than 6 characters.
    # Text: {text}

    # Please provide the result in JSON format with the following structure:
    # {{
    #     "score": <LIX score>,
    #     "explanation": "<explanation of the calculation>"
    # }}
    # """

    prompt = f"""Analyze the complexity of the following text with the following formula:

    Calculate the LIX (Läsbarhetsindex) score for Swedish text.
    
    LIX = A + B, where:
    A = number of words / number of sentences
    B = (number of long words * 100) / number of words
    
    Long words are defined as words with more than 6 characters. Provide the LIX score as a floating point number and nothing else.
    Text: {text}
     DO NOT WRITE OUT ANYTHING EXPECT THE LIX SCORE. JUST CALCULATE THE LIX SCORE AND WRITE IT OUT!

    
    """


    return call_groq_api(prompt)

def measure_add(text):
#     prompt = f"""Analyze the following text and calculate its Average Dependency Distance (ADD). ADD is a measure of syntactic complexity that considers the average distance between syntactically related words in a sentence. Provide the ADD score and a brief explanation of how you calculated it.

# Text: {text}

#     Please provide the result in JSON format with the following structure:
#     {{
#         "score": <ADD score>,
#         "explanation": "<explanation of the calculation>"
#     }}
#     """
    prompt = f"""Analyze the following text and calculate its Average Dependency Distance (ADD). ADD is a measure of syntactic complexity that considers the average distance between syntactically related words in a sentence. Provide the ADD score as a floating point number and nothing else.
        
        Text: {text} DO NOT WRITE OUT ANYTHING EXPECT THE ADD SCORE. JUST CALCULATE THE ADD SCORE AND WRITE IT OUT!"""

    return call_groq_api(prompt)

def parse_result(result):
    if result is None:
        raise ValueError("API response is None")
    try:
        json_result = json.loads(result)
        score = float(json_result['score'])
        explanation = json_result['explanation']
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error parsing JSON response: {str(e)}")
        print("Raw response:", result)
        return None, None
    return score, explanation

def run_analysis(text, filename):
    complexity_result = measure_complexity(text)
    add_result = measure_add(text)
    print("Complexity result:", complexity_result)
    print("ADD result:", add_result)
    
    # complexity_score, complexity_explanation = parse_result(complexity_result)
    # add_score, add_explanation = parse_result(add_result)
    
    # Ensure the results directory exists
    os.makedirs('results', exist_ok=True)
    
    # Save all responses to a file
    with open('results/raw_api_responses_short.txt', 'a') as f:
        f.write(f"File: {filename}\n")
        f.write(f"Text: {text}\n")
        f.write(f"Complexity result: {complexity_result}\n")
        f.write(f"ADD result: {add_result}\n")
        f.write("\n---\n\n")
    
    # Save complexity results
    with open('results/complexity_analysis_llm_short.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header if file is empty
            writer.writerow(['file', 'text', 'complexity_score', 'explanation'])
        #writer.writerow([filename, text, complexity_score, complexity_explanation])
        writer.writerow([filename, text, complexity_result])
    
    # Save ADD results
    with open('results/add_analysis_llm_short.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header if file is empty
            writer.writerow(['file', 'text', 'add_score', 'explanation'])
        writer.writerow([filename, text, add_result])
        #writer.writerow([filename, text, add_score, add_explanation])
    
    print(f"Results saved to results/complexity_analysis_llm.csv and results/add_analysis_llm.csv")
    print(f"Raw API responses saved to results/raw_api_responses.txt")

# Example usage
# if __name__ == "__main__":
#     sample_text = "The quantum entanglement of particles exhibits non-local correlations that challenge our classical intuitions about reality."
#     run_analysis(sample_text, "sample.txt")



def process_data_directory(data_dir):
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                # Take a chunk of 1000 characters and extend to the next period
                if len(text) <= 1000:
                    subpart = text
                else:
                    subpart = text[:1000]
                    last_period = subpart.rfind('.')
                    if last_period != -1:
                        subpart = text[:last_period + 1]
                    else:
                        # If no period is found, take the whole chunk
                        subpart = text[:1000]
                
                print(f"Processing file: {file}")
                run_analysis(subpart, file)

if __name__ == "__main__":
    data_directory = "data"
    process_data_directory(data_directory)
    print("Analysis completed for all files in the data directory.")

