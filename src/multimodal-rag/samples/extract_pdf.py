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

class PDFExtractor:
    """
    Base class for PDF text extractors.

    :param file_path: The path to the PDF file.
    :type file_path: str
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        """
        Extracts text from the PDF file.

        :raises NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclass must implement extract_text method.")

class PyPDF2Extractor(PDFExtractor):
    """
    PDF text extractor using PyPDF2 library.
    """
    @measure_time
    def extract_text(self):
        """
        Extracts text from the PDF file using PyPDF2 library.

        :return: The extracted text and the execution time.
        :rtype: tuple (str, float)
        """
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
        return text

class PDFPlumberExtractor(PDFExtractor):
    """
    PDF text extractor using pdfplumber library.
    """
    @measure_time
    def extract_text(self):
        """
        Extracts text from the PDF file using pdfplumber library.

        :return: The extracted text and the execution time.
        :rtype: tuple (str, float)
        """
        with pdfplumber.open(self.file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text

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
            extractor = extractor_class(file_path)
            text, execution_time = extractor.extract_text()
            print(f"Extractor: {extractor_name}")
            print(f"Extracted Text: {text[:100]}...")
            print(f"Execution Time: {execution_time:.2f} seconds")
            print("---")
            
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}_{extractor_name}.txt")
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(text)
        else:
            print(f"Unknown extractor: {extractor_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF Text Extractor')
    parser.add_argument('file_path', help='Path to the PDF file')
    parser.add_argument('--extractors', default='all', help='Comma-separated list of extractors to use (default: all)')
    parser.add_argument('--output_dir', default='.', help='Directory to save the extracted text files (default: current directory)')
    
    args = parser.parse_args()
    
    extractors = args.extractors.split(',')
    main(args.file_path, extractors, args.output_dir)