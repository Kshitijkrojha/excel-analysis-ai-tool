import os
from dotenv import load_dotenv
import pandas as pd
from google import genai

# Load environment variables from .env
load_dotenv()

# Get Gemini API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Load Excel file
file_path = "data/sample_sales_data.xlsx"
df = pd.read_excel(file_path)

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text.strip()

def handle_query(query):
    context = f"Dataset columns: {', '.join(df.columns)}. First few rows:\n{df.head().to_string(index=False)}"
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    return generate_response(prompt)

print("Ask your question about the sales data (type 'exit' to quit).")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
    answer = handle_query(user_input)
    print("Answer:", answer)
