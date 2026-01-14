import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# print(f"This is google api key: {os.getenv("GOOGLE_API_KEY")}")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

chat_model = genai.GenerativeModel("models/gemini-2.5-flash")
embedding_model = "models/text-embedding-004"
