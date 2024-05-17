import pdfplumber

from get_fonts import get_fonts

doc_name = "report.pdf"


# texts = []
# discarded = []
# sizes = set()
# with pdfplumber.open(doc_name) as pdf:
#     heading_size = get_fonts(doc_name)[-3]
#     for page in pdf.pages:
#         words = [{x.get('text'): x} for x in page.extract_words(x_tolerance_ratio=0.1, extra_attrs=['size']) if
#                  x["size"] >= heading_size]
#         print(words)


# if 'Disclosures' in words:
#     texts = text.split('Disclosures')
#     text = texts[0]
#     discarded.append(texts[1:])
# texts.append(text)
# print(text)


def get_headings_sentences(page):
    from itertools import takewhile, dropwhile
    DELIMITERS = ".!?"
    FONTSTYLE = "BOLD"
    FONTSIZE = get_fonts(doc_name)[-3]
    chars = iter(page.chars)
    while True:
        sentence = "".join(
            char["text"] for char in takewhile(
                lambda char: char["text"] not in DELIMITERS,
                dropwhile(
                    lambda char: char["size"] > FONTSIZE,
                    chars)
            )
        )
        if sentence:
            yield sentence
        else:
            break


FONTSIZE = get_fonts(doc_name)[-6]


def get_headings(PDFplumberPage):
    # , startsWith='PROP:"bold"', endsWith='CHAR:"."'):
    lstDct = PDFplumberPage.chars
    lstSentences = []
    strSentence = ''
    y_position = (0, 0)
    for dct in lstDct:
        if dct['size'] >= FONTSIZE:
            if y_position == (0, 0):
                y_position = (dct['y0'], dct['y1'])

            char = dct['text']
            if y_position == (dct['y0'], dct['y1']):
                strSentence += char
            else:
                lstSentences.append(strSentence)
                strSentence = f'{char}'
                y_position = (dct['y0'], dct['y1'])
    return lstSentences


import pdfplumber

with pdfplumber.open(doc_name) as pdf:
    # for page in pdf.pages:
    page = pdf.pages[1]
    print(*get_headings(page), sep=", ")
    print()
