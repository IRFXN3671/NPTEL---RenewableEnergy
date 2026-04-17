import fitz
import re
import os

folder = 'Questions'
files = sorted([f for f in os.listdir(folder) if f.endswith('.pdf')])
target_files = []
for i in range(1, 13):
    pattern = re.compile(rf'Assignment\s*0?{i}\b|Week\s*{i}', re.IGNORECASE)
    for f in files:
        if pattern.search(f):
            target_files.append((i, f))
            break

def extract_answers(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    results = []
    # Strategy 1: Explicit Markers
    matches = re.finditer(r'(?:Ans:|Answer:|Answer\.|Correct option:|Correct choice:)\s*([a-dA-D0-9\.]+|[A-Z][a-z]+)', text, re.IGNORECASE)
    for match in matches:
        results.append(match.group(1).strip())

    # Strategy 2: Solution Blocks with (a), (b), etc.
    if not results:
        # Looking for (a) or (b) following "Solution:" or "Q1. ... (a)"
        # Let's try finding all occurrences of "Solution:" and taking the next bracketed letter
        solutions = re.split(r'Solution:', text, flags=re.IGNORECASE)
        for sol in solutions[1:]: # Skip text before first Solution:
            m = re.search(r'\(([a-d])\)', sol, re.IGNORECASE)
            if m:
                results.append(m.group(1))
            else:
                # Try just a lone [a-d] if it's right at the start
                m2 = re.search(r'^\s*([a-d])\b', sol, re.IGNORECASE | re.MULTILINE)
                if m2:
                    results.append(m2.group(1))

    return results

print("Revised Concised Report:")
for num, file in target_files:
    path = os.path.join(folder, file)
    answers = extract_answers(path)
    ans_str = ", ".join([f"{i+1}:{a}" for i, a in enumerate(answers)]) if answers else "UNKNOWN"
    print(f"Assign {num}: {ans_str}")
