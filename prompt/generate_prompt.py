import os
import google.generativeai as genai

def generate(user_input):
    api_key = os.getenv("GEMINI_API_KEY")

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(user_input)
    return response.text

