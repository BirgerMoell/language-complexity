import os
import csv
import json
import re
from groq import Groq
from dotenv import load_dotenv
from tqdm import tqdm
from llm_complexity import calculate_lix_score
from calculate_add import calculate_average_dependency_distance
import time

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Prompts
COMPLEXITY_PROMPT = """You are a world expert in mathematics and linguistics. Calculate the LIX (Läsbarhetsindex) score for the following Swedish text. 
Text: {text}

Here is how LIX is calculated.

LIX = A + B, where:
A = number of words / number of sentences
B = (number of long words * 100) / number of words

Long words are defined as words with more than 6 characters. 

To do this you need to do the following.
1. Calculate the number of words
2. Calculate the number of sentences
3. Calculate the number of long words.
4. Calculate A as the number of words / number of sentences
5. Calculate B as (the number of long words*100) / number of words

Use a calculator to double check and make sure that your calculations are correct. End your report by providing the LIX SCORE in this format
LIX_SCORE: 
"""

COMPLEXITY_PROMPT_NEW = """Analyze the complexity of the following text with the following formula:

Calculate the LIX (Läsbarhetsindex) score for Swedish text.

LIX = A + B, where:
A = number of words / number of sentences
B = (number of long words * 100) / number of words

Long words are defined as words with more than 6 characters. Provide the LIX score as a floating point number and nothing else.
Text: {text}
DO NOT WRITE OUT ANYTHING EXPECT THE LIX SCORE. JUST CALCULATE THE LIX SCORE AND WRITE IT OUT!
"""


ADD_PROMPT = """Analyze the following text and calculate its Average Dependency Distance (ADD). ADD is a measure of syntactic complexity that considers the average distance between syntactically related words in a sentence."


Text: {text} Write out your explanation for calculating the ADD score in detail. Use a calculator to double check and make sure that your calculations are correct. After you are done with reasoning. Write out your score in the following format:
ADD_SCORE: """

ADD_PROMPT_NEW = """Analyze the following text and calculate its Average Dependency Distance (ADD). ADD is a measure of syntactic complexity that considers the average distance between syntactically related words in a sentence. Provide the ADD score as a floating point number and nothing else.

Text: {text} DO NOT WRITE OUT ANYTHING EXPECT THE ADD SCORE. JUST CALCULATE THE ADD SCORE AND WRITE IT OUT!"""


def call_groq_api(prompt, max_retries=3, delay=5):
    for attempt in range(max_retries):
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
            print(f"Error calling Groq API (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Returning None.")
                return None

def measure_complexity(text):
    return call_groq_api(COMPLEXITY_PROMPT.format(text=text))

def measure_add(text):
    return call_groq_api(ADD_PROMPT.format(text=text))

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

def extract_score(result, score_type):
    if score_type not in ["LIX_SCORE", "ADD_SCORE"]:
        raise ValueError("Invalid score type")
    
    try:
        # Split the result by the score type and get the part after it
        score_part = result.split(f"{score_type}:")[-1].strip()
        # Extract the first number from the remaining text
        score = float(re.search(r'\d+(\.\d+)?', score_part).group())
        return score
    except (AttributeError, ValueError) as e:
        print(f"Error extracting {score_type}: {str(e)}")
        print("Raw result:", result)
        return None

def run_analysis(text, filename):
    run_name = "calculator_prompt_birger"
    complexity_result = measure_complexity(text)
    add_result = measure_add(text)
    print("Complexity result:", complexity_result)
    print("ADD result:", add_result)
    
    lix_score = extract_score(complexity_result, "LIX_SCORE") if complexity_result else None
    add_score = extract_score(add_result, "ADD_SCORE") if add_result else None
    
    # Calculate LIX and ADD using local functions
    local_lix_score = calculate_lix_score(text)
    local_add_score = calculate_average_dependency_distance(text)
    
    # Ensure the results directory exists
    os.makedirs('results', exist_ok=True)
    
    # Save all responses to a file
    with open(f'results/raw_api_responses_{run_name}.txt', 'a') as f:
        f.write(f"File: {filename}\n")
        f.write(f"Text: {text}\n")
        f.write(f"Complexity result (LLM): {complexity_result}\n")
        f.write(f"ADD result (LLM): {add_result}\n")
        f.write(f"Complexity result (Local): {local_lix_score}\n")
        f.write(f"ADD result (Local): {local_add_score}\n")
        f.write("\n---\n\n")

    # Write prompts at the end of the file
    with open(f'results/raw_api_responses_{run_name}.txt', 'a') as f:
        f.write(f"Complexity Prompt: {COMPLEXITY_PROMPT}\n")
        f.write(f"ADD Prompt: {ADD_PROMPT}\n")
    
    # Save complexity results
    with open(f'results/complexity_analysis_{run_name}.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header if file is empty
            writer.writerow(['file', 'llm_complexity_score', 'local_complexity_score', 'difference'])
        difference = abs(lix_score - local_lix_score) if lix_score is not None and local_lix_score is not None else "N/A"
        writer.writerow([filename, lix_score, local_lix_score, difference])
    
    # Save ADD results
    with open(f'results/add_analysis_{run_name}.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header if file is empty
            writer.writerow(['file', 'llm_add_score', 'local_add_score', 'difference'])
        difference = abs(add_score - local_add_score) if add_score is not None and local_add_score is not None else "N/A"
        writer.writerow([filename, add_score, local_add_score, difference])
    
    print(f"Results saved to results/complexity_analysis_{run_name}.csv and results/add_analysis_{run_name}.csv")
    print(f"Raw API responses saved to results/raw_api_responses_{run_name}.txt")

# Example usage
# if __name__ == "__main__":
#     sample_text = "The quantum entanglement of particles exhibits non-local correlations that challenge our classical intuitions about reality."
#     run_analysis(sample_text, "sample.txt")



def process_data_directory(data_dir):
    all_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.txt'):
                all_files.append(os.path.join(root, file))
    
    for file_path in tqdm(all_files, desc="Processing files"):
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
        
        file_name = os.path.basename(file_path)
        print(f"\nProcessing file: {file_name}")
        run_analysis(subpart, file_name)

if __name__ == "__main__":
    data_directory = "data_short"
    process_data_directory(data_directory)
    print("Analysis completed for all files in the data directory.")

