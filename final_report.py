import fitz
import re
import os

folder = 'Questions'
# Get files matching Assignment or Week and number from 1 to 12
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
    # Combine markers
    # Ans: Answer: Answer. Correct Option: Correct answer: Correct Option. Solution:
    # Also handle multiple lines if possible, but keep it simple
    matches = re.finditer(r'(?:Ans:|Answer:|Answer\.|Correct choice is|Correct answer:|Correct choice:|Correct Option:)\s*([a-dA-D0-9\.]+|[A-Z]+[a-z]*)', text, re.IGNORECASE)
    last_pos = 0
    for match in matches:
        ans = match.group(1).strip()
        results.append(ans)
        last_pos = match.end()

    # Special case for "Solution: (a)"
    remaining_text = text[last_pos:]
    if not results:
        sol_matches = re.finditer(r'Solution:\s*\(?([a-d])\)?', text, re.IGNORECASE)
        for m in sol_matches:
            results.append(m.group(1))

    return results

print("Final Concised Report:")
for num, file in target_files:
    path = os.path.join(folder, file)
    answers = extract_answers(path)
    ans_str = ", ".join([f"{i+1}:{a}" for i, a in enumerate(answers)]) if answers else "UNKNOWN"
    print(f"Assign {num}: {ans_str}")
