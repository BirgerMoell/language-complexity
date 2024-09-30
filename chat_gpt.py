from openai import OpenAI
from dotenv import load_dotenv
import os

# Ladda miljövariabler från .env-filen
load_dotenv()

# Hämta API-nyckeln från miljövariabeln
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

open_ai_client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def get_text_from_open_ai(prompt, model="gpt-3.5-turbo"):
    completion = open_ai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a world class expert on everything. Answer concise and accurate with compassion."},
            {"role": "user", "content": prompt}
        ]
    )
    print("the completion is", completion)
    text = completion.choices[0].message.content
    return text





# Example usage of the get_text_from_open_ai function
prompt = "What is the capital of France?"
result = get_text_from_open_ai(prompt)
print("OpenAI response:", result)
