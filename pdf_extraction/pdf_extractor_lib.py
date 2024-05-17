import io
import math

import fitz
import pdfplumber


class PDFExtractor:
    @staticmethod
    def filter_by_font_size(obj, threshold):
        """ Returns True if the object's font size is above the threshold. """
        if obj['object_type'] != 'char':
            return False
        return float(obj['size']) > threshold

    # We use different library (PyMuPDF), because it's logarithmically faster.
    @staticmethod
    def get_fonts(pdf_content):
        results = set()  # list of tuples that store the information as (text, font size, font name)
        with fitz.open(stream=pdf_content, filetype="pdf") as pdf:
            for page in pdf:
                dict = page.get_text("dict")
                blocks = dict["blocks"]
                for block in blocks:
                    if "lines" in block.keys():
                        spans = block['lines']
                        for span in spans:
                            data = span['spans']
                            for lines in data:
                                results.add(math.ceil(lines['size'] * 10) / 10)
                                # lines['text'] -> string, lines['size'] -> font size, lines['font'] -> font name
        return sorted(results)

    @classmethod
    def extract_text(cls, pdf_content, exclude_keywords=None, word_margin=0.5):
        """
        Extract text from a PDF file, excluding text under sections that contain specific keywords and filtering the smallest font.

        Parameters:
            pdf_content (bytes): The PDF file content in binary format.
            exclude_keywords (list): Keywords that indicate sections to exclude. If None, no sections are excluded.

        Returns:
            str: The extracted text with specified sections excluded.
        """
        extracted_text = ""

        if exclude_keywords is None:
            exclude_keywords = []

        size_threshold = None
        try:
            font_sizes = cls.get_fonts(pdf_content)
            if font_sizes:
                size_threshold = font_sizes[0]
        except Exception as e:
            print(f"An error occurred getting fonts: {e}")
        try:
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                # Calculate document-level font threshold
                for page in pdf.pages:
                    if size_threshold:
                        page = page.filter(lambda obj: cls.filter_by_font_size(obj, size_threshold))
                    # Adjusting the word margin to handle spacing issues
                    text = page.extract_text(x_tolerance=word_margin, y_tolerance=word_margin)
                    print(text)
                    if text:
                        for keyword in exclude_keywords:
                            if keyword in text:
                                text = text.split(keyword)[0]
                            extracted_text += text + "\n"
        except Exception as e:
            print(f"An error occurred in PDF extraction: {e}")

        return extracted_text
