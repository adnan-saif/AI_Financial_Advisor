import os
import google.generativeai as genai

# Gemini API Key configuration
GEMINI_API_KEY = "AIzaSyA9zyzKSKSccu51LvsA5GksoHSg_8wr8s0"
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")