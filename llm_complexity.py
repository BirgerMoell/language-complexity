import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def calculate_language_complexity(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a language complexity analyzer. Analyze the given text and provide a complexity score from 1 to 10, where 1 is very simple and 10 is very complex. Also provide a brief explanation for the score."},
                {"role": "user", "content": f"Analyze the complexity of the following text:\n\n{text}"}
            ]
        )
        
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

def calculate_lix_score(text):
    """
    Calculate the LIX (Läsbarhetsindex) score for Swedish text.
    
    LIX = A + B, where:
    A = number of words / number of sentences
    B = (number of long words * 100) / number of words
    
    Long words are defined as words with more than 6 characters.
    """
    # Split text into words and sentences
    words = text.split()
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Count words and sentences
    word_count = len(words)
    sentence_count = len(sentences)
    
    # Count long words (more than 6 characters)
    long_word_count = sum(1 for word in words if len(word) > 6)
    
    # Calculate A and B components
    A = word_count / sentence_count if sentence_count > 0 else 0
    B = (long_word_count * 100) / word_count if word_count > 0 else 0
    
    # Calculate LIX score
    lix_score = A + B
    
    return lix_score

def interpret_lix_score(score):
    """
    Interpret the LIX score according to Swedish readability standards.
    """
    if score < 30:
        return "Very easy"
    elif 30 <= score < 40:
        return "Easy"
    elif 40 <= score < 50:
        return "Medium"
    elif 50 <= score < 60:
        return "Difficult"
    else:
        return "Very difficult"

def calculate_swedish_language_complexity(text):
    lix_score = calculate_lix_score(text)
    interpretation = interpret_lix_score(lix_score)
    
    return f"LIX Score: {lix_score:.2f}\nInterpretation: {interpretation}"


# Example usage
if __name__ == "__main__":
    sample_text = "The quantum entanglement of particles exhibits non-local correlations that challenge our classical intuitions about reality."
    result = calculate_language_complexity(sample_text)
    print(result)
