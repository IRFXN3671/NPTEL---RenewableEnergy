import fitz
import re
import os

folder = 'Questions'
files = sorted([f for f in os.listdir(folder) if 'Assignment' in f and f.endswith('.pdf')])

def extract_answers(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    results = []
    
    # Strategy 1: Look for "Ans: [text]" or "Answer: [text]" or "Answer. [text]"
    # We want to catch the first word or letter after the colon/period.
    matches = re.finditer(r'(?:Ans:|Answer:|Answer\.|Correct option:)\s*([a-dA-D0-9\.]+|[A-Za-z]+)', text, re.IGNORECASE)
    for match in matches:
        ans = match.group(1).strip()
        # If it's a long word, maybe it's the option text. Let's keep it brief.
        if len(ans) > 20: 
            ans = ans[:20] + "..."
        results.append(ans)
    
    # Strategy 2: If no results, look for "Solution:" patterns or "Correct choice is (a)"
    if not results:
        # Looking for "(a)" or "(1)" following a solution marker
        matches = re.finditer(r'Solution:.*?\(?([a-d])\)?', text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            results.append(match.group(1))

    return results

for file in files:
    path = os.path.join(folder, file)
    answers = extract_answers(path)
    print(f"--- {file} ---")
    if answers:
        # Format output: Q1: ans, Q2: ans...
        out = [f"Q{i+1}: {a}" for i, a in enumerate(answers)]
        print(", ".join(out))
    else:
        print("No answers found/Reliability: UNKNOWN")
