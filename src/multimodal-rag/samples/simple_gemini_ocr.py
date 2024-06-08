from google import generativeai
from dotenv import load_dotenv
import os, sys
import time
from google.generativeai.types.generation_types import GenerateContentResponse

def measure_time(func):
    """
    Decorator to measure the execution time of a function.
    
    :param func: The function to measure the execution time of.
    :type func: function
    :return: The wrapped function.
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

def find_image_file(directory_path):
    # ディレクトリ内のpngファイルを検索
    for filename in os.listdir(directory_path):
        if filename.endswith(".png"):
            return os.path.join(directory_path, filename)
    return None

@measure_time
def process_files(directory_path):
    image_path = find_image_file(directory_path)
    if image_path is None:
        print("Error: No PNG file found in the directory.")
        return

    # ディレクトリ内のtxtファイルを処理
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)

            # 画像ファイルをアップロード
            image = generativeai.upload_file(path=image_path)

            # テキストファイルを読み込む
            with open(file_path, "r") as file:
                file_content = file.read()

            prompt = f"画像ファイルはPDFを画像化したものです。このPDFの配置構造を理解し、文脈を踏まえたうえでテキストになおしてください。文字は日本語をベースに書かれています。最終的な構造はMarkdown形式にして出力してください。その後、このPDFで書かれている内容を解釈して解説してください。これを別のPDF解析ツールで読み取りした結果は以下です。\n読み取り結果: {file_content}"

            response: GenerateContentResponse = model.generate_content([prompt, image])

            # 結果をmdファイルとして保存
            md_file_path = os.path.splitext(file_path)[0] + ".md"
            with open(md_file_path, "w") as md_file:
                md_file.write(response.candidates[0].content.parts[0].text)

            print(f"Processed: {filename}")

# run as main
if __name__ == "__main__":
    load_dotenv()
    generativeai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = generativeai.GenerativeModel("models/gemini-1.5-pro-latest")

    # コマンドライン引数からディレクトリのパスを取得
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    _, execution_time = process_files(directory_path)
    print(f"Execution time: {execution_time:.2f} seconds")