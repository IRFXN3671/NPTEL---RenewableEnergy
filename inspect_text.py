import fitz
import re
import os

folder = 'Questions'
files = sorted([f for f in os.listdir(folder) if 'Assignment' in f and f.endswith('.pdf')])

def extract_content(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

for file in files:
    path = os.path.join(folder, file)
    text = extract_content(path)
    print(f"[{file}] First 500 chars:")
    print(text[:500].replace('\n', ' '))
    print("-" * 20)
