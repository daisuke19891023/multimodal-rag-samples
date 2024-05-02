from urllib import response
from google import generativeai
from dotenv import load_dotenv
import os

from google.generativeai.types.generation_types import GenerateContentResponse

# run as main
if __name__ == "__main__":
    load_dotenv()
    generativeai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = generativeai.GenerativeModel("models/gemini-1.5-pro-latest")
    audio_file = generativeai.upload_file(path="example_data/audio.mp3")
    response: GenerateContentResponse = model.generate_content(["この音声ファイルを文字起こししてください。話している言語は日本語です。文字起こしは日本語で出力してください。", audio_file])
    print(response)
