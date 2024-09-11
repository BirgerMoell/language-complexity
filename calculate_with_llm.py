import os
import csv
import json
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
    prompt = f"""Analyze the complexity of the following text with the following formula:

    Calculate the LIX (Läsbarhetsindex) score for Swedish text.
    
    LIX = A + B, where:
    A = number of words / number of sentences
    B = (number of long words * 100) / number of words
    
    Long words are defined as words with more than 6 characters.
    Text: {text}

    Please format your response as a JSON object with the following structure, when you have your answer, end your response by writing out the answer in the following format RESPONSE:
    {{
        "score": [numerical score],
        "explanation": [your explanation]
    }}"""

    return call_groq_api(prompt)

def measure_add(text):
    prompt = f"""Analyze the following text and calculate its Average Dependency Distance (ADD). ADD is a measure of syntactic complexity that considers the average distance between syntactically related words in a sentence. Provide the ADD score and a brief explanation of how you calculated it.

Text: {text}

 Please format your response as a JSON object with the following structure, when you have your answer, end your response by writing out the answer in the following format RESPONSE:
{{
    "score": [numerical score],
    "explanation": [your explanation of the calculation method]
}}"""

    return call_groq_api(prompt)

def parse_result(result):
    if result is None:
        raise ValueError("API response is None")
    try:
        if "RESPONSE:" in result:
            _, json_str = result.split("RESPONSE:", 1)
        else:
            json_str = result
        result_json = json.loads(json_str.strip())
        score = float(result_json['score'])
        explanation = result_json['explanation']
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise ValueError(f"Error parsing API response: {str(e)}")
    return score, explanation

def run_analysis(text, filename):
    complexity_result = measure_complexity(text)
    add_result = measure_add(text)
    print(complexity_result)
    print(add_result)
    
    try:
        complexity_score, complexity_explanation = parse_result(complexity_result)
        add_score, add_explanation = parse_result(add_result)
    except ValueError as e:
        print(f"Error parsing API response: {str(e)}")
        return
    
    # Ensure the results directory exists
    os.makedirs('results', exist_ok=True)
    
    # Save complexity results
    with open('results/complexity_analysis_llm.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header if file is empty
            writer.writerow(['file', 'text', 'complexity_score', 'explanation'])
        writer.writerow([filename, text, complexity_score, complexity_explanation])
    
    # Save ADD results
    with open('results/add_analysis_llm.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header if file is empty
            writer.writerow(['file', 'text', 'add_score', 'explanation'])
        writer.writerow([filename, text, add_score, add_explanation])
    
    print(f"Results saved to results/complexity_analysis_llm.csv and results/add_analysis_llm.csv")

# Example usage
if __name__ == "__main__":
    sample_text = "The quantum entanglement of particles exhibits non-local correlations that challenge our classical intuitions about reality."
    run_analysis(sample_text, "sample.txt")
