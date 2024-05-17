from PyPDF2 import PdfReader

reader = PdfReader("report.pdf")
page = reader.pages[1]

parts = []
# reader = PdfReader(pdf_content)
number_of_pages = len(reader.pages)
full_text_list = []
for i in range(number_of_pages):
    page = reader.pages[i]
    full_text_list.append(page.extract_text())
# return '\n'.join(full_text_list)

def visitor_body(text, cm, tm, font_dict, font_size):
    y = cm[5]
    if y > 50 and y < 720:
        parts.append(text)


page.extract_text(visitor_text=visitor_body)
text_body = "".join(parts)

print(text_body)