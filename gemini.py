# pip install -q -U google-generativeai
#https://developers.googleblog.com/en/gemini-is-now-accessible-from-the-openai-library/

import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
    
    

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


response = client.chat.completions.create(
    model="gemini-1.5-flash-002",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works in portuguese with 50 words"
        }
    ]
)

print(response.choices[0].message.content)
#print(response.text)