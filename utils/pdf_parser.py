# utils/pdf_parser.py

import pdfplumber

class PDFParser:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path

    def parse_text(self):
        try:
            text = ""
            with pdfplumber.open(self.pdf_file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            if(text == ""):
                print("Error: No text extracted from the PDF. Please check the PDF file.")
            return text
        except Exception as e:
            print(f"An error occurred while parsing the PDF: {e}")
            return ""
