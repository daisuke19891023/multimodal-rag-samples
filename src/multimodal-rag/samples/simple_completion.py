from google import generativeai
from dotenv import load_dotenv
import os


# run as main
if __name__ == "__main__":
    load_dotenv()
    generativeai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    for m in generativeai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)
    # model = generativeai.GenerativeModel('gemini-pro')
    # response = model.generate_content("The quick brown fox jumps over the lazy dog.")
    # print(response)
