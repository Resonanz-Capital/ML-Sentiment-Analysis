import io
import os
import re
import statistics

import pandas as pd
import pdfplumber

from pdf_extractor_lib import PDFExtractor
from utils import get_reports


def filter_by_font_size(obj, threshold):
    """ Returns True if the object's font size is above the threshold. """
    if obj['object_type'] != 'char':
        return False
    return float(obj['size']) > threshold


def extract_text_without_sections(pdf_content, exclude_keywords=None, word_margin=0.5):
    """
    Extract text from a PDF file, excluding text under sections that contain specific keywords.

    Parameters:
        pdf_path (str): Path to the PDF file.
        exclude_keywords (list): Keywords that indicate sections to exclude. If None, no sections are excluded.

    Returns:
        str: The extracted text with specified sections excluded.
    """
    extracted_text = ""
    exclude = False

    if exclude_keywords is None:
        exclude_keywords = []

    font_sizes = set()
    try:
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                words = page.extract_words(extra_attrs=['size'])
                if words:
                    font_sizes.update(set([int(word['size']) for word in words]))

            # Calculate document-level font threshold
            if font_sizes:
                size_threshold = sorted(font_sizes)[0]

            for page in pdf.pages:
                # Adjusting the word margin to handle spacing issues
                if size_threshold:
                    page = page.filter(lambda obj: filter_by_font_size(obj, size_threshold))
                text = page.extract_text(x_tolerance=word_margin, y_tolerance=word_margin)
                if text:
                    # Apply a regex to separate words that are stuck together
                    # text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
                    for keyword in exclude_keywords:
                        if keyword in text:
                            text = text.split(keyword)[0]
                    if not exclude:
                        extracted_text += text + "\n"
                    exclude = False  # Reset for next page/check
    except Exception as e:
        print(f"An error occurred: {e}")

    return extracted_text


def extract_tables_to_dataframes(pdf_path):
    """
    Extracts all tables from a PDF file and converts them into pandas DataFrames.

    Parameters:
        pdf_path (str): Path to the PDF file.

    Returns:
        list of pandas.DataFrame: A list containing all tables found in the PDF as DataFrames.
    """
    dataframes = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract tables from the page
                tables = page.extract_tables()
                for table in tables:
                    # Convert the table (list of lists) into a DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0])
                    dataframes.append(df)
    except Exception as e:
        print(f"An error occurred: {e}")

    return dataframes


def extract_text_without_sections_and_footnotes(pdf_path, exclude_keywords=None, word_margin=0.5):
    if exclude_keywords is None:
        exclude_keywords = []
    font_sizes = set()

    with pdfplumber.open(pdf_path) as pdf:
        # First, gather all data from the document
        for page in pdf.pages:
            words = page.extract_words(extra_attrs=['size'])
            if words:
                font_sizes.update(set([int(word['size']) for word in words]))

        # Calculate document-level thresholds
        if font_sizes:
            size_threshold = sorted(font_sizes)[1]

        processed_texts = []
        discarded_texts = []
        excluded_texts = []
        for page in pdf.pages:
            words = page.extract_words(x_tolerance=word_margin, y_tolerance=word_margin, extra_attrs=['size'])
            page_text = []
            excluded_text = []
            for idx, word in enumerate(words):
                if any([word['text'].find(x) != -1 for x in exclude_keywords]):
                    excluded_text = [word['text'] for word in words[idx:]]
                    break
                if float(word['size']) > size_threshold:
                    page_text.append(word['text'])
            discarded_text = [word['text'] for word in words if float(word['size']) <= size_threshold]
            processed_texts.append(" ".join(page_text))
            discarded_texts.append(" ".join(discarded_text))
            excluded_texts.append(" ".join(excluded_text))
        return processed_texts, discarded_texts, excluded_texts


# processed_texts, discarded_texts, excluded_texts = extract_text_without_sections_and_footnotes(
#     "reports/Nordea 1 Alpha 15 MA Fund_Monthly Report_290224_rec_220324.pdf",
#     exclude_keywords=["Disclosure", "Disclosures", "Disclaimer", "Notes"]
# )

# Example usage:
# dfs = extract_tables_to_dataframes("path_to_your_pdf.pdf")
# for df in dfs:
#     print(df)


# txt = extract_text_without_sections("report.pdf", exclude_keywords=["Disclosure", "Disclaimer"])
# print(text)
# Example usage:
# extract_text_without_sections_and_footnotes(
#     "reports/Nordea 1 Alpha 15 MA Fund_Monthly Report_290224_rec_220324.pdf",
#     exclude_keywords=["Disclosure", "Disclaimer", "Notes"])
texts = {}
with open("report.pdf", 'rb') as pdf_content:
    text = PDFExtractor.extract_text(pdf_content.read(), exclude_keywords=["Disclosure", "Disclaimer"], word_margin=0.5)

# for filename in get_reports():
# for filename in ['ProVex SA SICAV RAIF Convergence_Monthly Report_290224_rec_220324.pdf']:
#     path = os.path.join("reports", filename)
#     with open(path, 'rb') as pdf_content:
#         processed_text = extract_text_without_sections(pdf_content.read(),
#                                                        exclude_keywords=[
#                                                             "Disclosure",
#                                                             "Disclaimer",
#                                                             "Note"], word_margin=0.001)
#     texts[filename] = processed_text
print()
