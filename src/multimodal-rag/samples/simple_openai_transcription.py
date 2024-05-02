from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# run as main
if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    audio_file = open("example_data/audio.mp3", "rb")
    start_time = time.time()
    transcription = client.audio.transcriptions.create(model="whisper-1", language="ja", file=audio_file)
    print(transcription.text)
    print(f"処理にかかった時間: {time.time()-start_time} 秒")
