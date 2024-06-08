"""
PDF Text Extractor
==================

This module provides functionality to extract text from PDF files using different libraries.
It allows comparing the performance and results of each library.

Usage:
    python pdf_extractor.py <file_path> [--extractors=<extractors>] [--output_dir=<output_dir>]

Options:
    --extractors=<extractors>   Comma-separated list of extractors to use (default: all)
    --output_dir=<output_dir>   Directory to save the extracted text files (default: current directory)

"""

import os
import time
import argparse
import PyPDF2
import pdfplumber
from pdf2image import convert_from_path
from pydantic import BaseModel
# import textract

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

def save_sections_to_dirs(file_path, sections, output_dir, save_func, process_name):
    """
    Saves the sections to separate directories using a custom save function.

    :param file_path: The path to the original file.
    :type file_path: str
    :param sections: The sections to be saved.
    :type sections: list
    :param output_dir: The directory to save the section files.
    :type output_dir: str
    :param save_func: The function to save each section.
                      It should take the section and the file path as arguments.
    :type save_func: function
    """
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    parent_dir = os.path.join(output_dir, base_name)
    os.makedirs(parent_dir, exist_ok=True)
    
    for i, section in enumerate(sections, start=1):
        section_dir = os.path.join(parent_dir, str(i))
        os.makedirs(section_dir, exist_ok=True)
        section_file = os.path.join(section_dir, f"section_{i}_{process_name}")
        save_func(section, section_file)
        
class PDFExtractor:
    """
    Base class for PDF text extractors.

    :param file_path: The path to the PDF file.
    :type file_path: str
    :param output_dir: The directory to save the extracted text files.
    :type output_dir: str
    """
    def __init__(self, file_path, output_dir):
        self.file_path = file_path
        self.output_dir = output_dir

    def extract_text(self) -> list[str]:
        """
        Extracts text from the PDF file.

        :return: The extracted text sections and the execution time.
        :rtype: list of sections (str)
        :raises NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclass must implement extract_text method.")

    def save_sections(self, sections):
        """
        Saves the extracted text sections to separate directories.

        :param sections: The extracted text sections.
        :type sections: list of str
        """
        def save_text(section, file_path):
            with open(f"{file_path}.txt", 'w', encoding='utf-8') as file:
                file.write(section)

        save_sections_to_dirs(self.file_path, sections, self.output_dir, save_text, self.__class__.__name__)

class PyPDF2Extractor(PDFExtractor):
    """
    PDF text extractor using PyPDF2 library.
    """
    @measure_time
    def extract_text(self) -> list[str]:
        """
        Extracts text from the PDF file using PyPDF2 library.

        :return: The extracted text and the execution time.
        :rtype: tuple (str, float)
        """
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            sections = []
            for page in range(len(reader.pages)):
                section = reader.pages[page].extract_text()
                sections.append(section)
        self.save_sections(sections)
        return sections

class PDFPlumberExtractor(PDFExtractor):
    """
    PDF text extractor using pdfplumber library.
    """
    @measure_time
    def extract_text(self) -> list[str]:
        """
        Extracts text from the PDF file using pdfplumber library.

        :return: The extracted text and the execution time.
        :rtype: tuple (str, float)
        """
        with pdfplumber.open(self.file_path) as pdf:
            sections = []
            for page in pdf.pages:
                section = page.extract_text()
                sections.append(section)
        self.save_sections(sections)
        return sections


def convert_pdf_to_images(pdf_file_path, output_dir):
    """
    指定されたPDFファイルの各ページを画像ファイルに変換し、指定されたディレクトリに保存する。
    
    Args:
    pdf_file_path (str): PDFファイルのパス。
    output_directory (str): 生成された画像を保存するディレクトリのパス。
    """
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # PDFファイルを画像に変換
    images = convert_from_path(pdf_file_path)

    # 各画像を指定されたディレクトリに保存
    # for i, image in enumerate(images):
    #     image_path = os.path.join(output_dir, f'page_{i + 1}.png')
    #     image.save(image_path, 'PNG')
    #     print(f'Saved: {image_path}')
    
    def save_image(image, file_path):
        image.save(f"{file_path}.png", 'PNG')
    
    save_sections_to_dirs(pdf_file_path, images, output_dir, save_image, "pdf2image")
        
# class TextractExtractor(PDFExtractor):
#     """
#     PDF text extractor using textract library.
#     """
#     @measure_time
#     def extract_text(self):
#         """
#         Extracts text from the PDF file using textract library.

#         :return: The extracted text and the execution time.
#         :rtype: tuple (str, float)
#         """
#         text = textract.process(self.file_path).decode('utf-8')
#         return text

def main(file_path, extractors, output_dir):
    """
    Main function to demonstrate the usage of PDF text extractors.

    :param file_path: The path to the PDF file.
    :type file_path: str
    :param extractors: List of extractors to use.
    :type extractors: list of str
    :param output_dir: Directory to save the extracted text files.
    :type output_dir: str
    """
    if extractors == ['all']:
        extractors = ['PyPDF2', 'PDFPlumber', 'Textract']
    
    extractor_classes = {
        'PyPDF2': PyPDF2Extractor,
        'PDFPlumber': PDFPlumberExtractor,
        # 'Textract': TextractExtractor
    }
    
    for extractor_name in extractors:
        extractor_class = extractor_classes.get(extractor_name)
        if extractor_class:
            extractor = extractor_class(file_path, output_dir)
            text, execution_time = extractor.extract_text()
            print(f"Extractor: {extractor_name}")
            print(f"Extracted Text: {text[:100]}...")
            print(f"Execution Time: {execution_time:.2f} seconds")
            print("---")
            
            # output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}_{extractor_name}.txt")
            # with open(output_file, 'w', encoding='utf-8') as file:
            #     file.write(text)
        else:
            print(f"Unknown extractor: {extractor_name}")
    # save image files
    convert_pdf_to_images(file_path, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF Text Extractor')
    parser.add_argument('file_path', help='Path to the PDF file')
    parser.add_argument('--extractors', default='all', help='Comma-separated list of extractors to use (default: all)')
    parser.add_argument('--output_dir', default='.', help='Directory to save the extracted text files (default: current directory)')
    
    args = parser.parse_args()
    
    extractors = args.extractors.split(',')
    main(args.file_path, extractors, args.output_dir)