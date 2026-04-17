import fitz  # PyMuPDF
import re
import os

folder = 'Questions'
files = sorted([f for f in os.listdir(folder) if f.endswith('.pdf')])

patterns = [
    r'Ans:\s*([a-d])',
    r'Answer:\s*([a-d])',
    r'Correct answer:\s*([a-d])',
    r'Answer:\s*([0-9\.]+)',
    r'Ans:\s*([0-9\.]+)'
]

def extract_answers(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    # Try to find questions and answers
    # Simple strategy: look for "Q" followed by digits, then search for answer markers near it
    # Or just find all occurrences of markers
    
    results = []
    # Find all "Ans:" or "Answer:" occurrences
    matches = re.finditer(r'(Ans:|Answer:|Correct answer|Correct Option:)\s*([a-d]|[0-9\.]+)', text, re.IGNORECASE)
    for i, match in enumerate(matches, 1):
        results.append(f"{i}: {match.group(2)}")
    
    return results

for file in files:
    if 'Assignment' in file:
        path = os.path.join(folder, file)
        answers = extract_answers(path)
        print(f"--- {file} ---")
        if answers:
            print(", ".join(answers))
        else:
            print("No answers found/Reliability: UNKNOWN")
