import math

import fitz


def get_fonts(filePath):
    results = set()  # list of tuples that store the information as (text, font size, font name)
    pdf = fitz.open(filePath)  # filePath is a string that contains the path to the pdf
    for page in pdf:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        results.add(math.ceil(lines['size'] * 10)/10)
                            # lines['text'] -> string, lines['size'] -> font size, lines['font'] -> font name
    return sorted(results)

s = get_fonts("report.pdf")
print(s)