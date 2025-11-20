import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

try:
    response = model.generate_content("Say only: hello")
    print("RAW RESPONSE:", response)
    print("TEXT:", response.text)
except Exception as e:
    print("ERROR:", e)
