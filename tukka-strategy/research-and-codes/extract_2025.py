import fitz
import os
import re

folder = r"d:\Jee Advanced Tukka Research"

# Extract ALL "Answer:" lines from 2025 papers with proper question mapping
for paper in [1, 2]:
    filename = f"JEE_Advanced_2025_Paper_{paper}_English.pdf"
    filepath = os.path.join(folder, filename)
    doc = fitz.open(filepath)
    
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    
    print(f"\n{'='*60}")
    print(f"2025 Paper {paper} — FULL ANSWER EXTRACTION")
    print(f"{'='*60}")
    
    # Find all "Answer:" lines and map them to questions
    lines = full_text.split('\n')
    
    q_num = 0
    section = ""
    subject = ""
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track subject
        if 'PHYSICS' in stripped.upper():
            subject = 'PHY'
        elif 'CHEMISTRY' in stripped.upper():
            subject = 'CHEM'  
        elif 'MATHEMATICS' in stripped.upper():
            subject = 'MATH'
        
        # Track sections
        if 'SECTION' in stripped.upper():
            section = stripped[:50]
        
        # Track question numbers
        qmatch = re.match(r'^Q\.?\s*(\d+)', stripped)
        if qmatch:
            q_num = int(qmatch.group(1))
        
        # Extract answers
        if stripped.startswith('Answer:'):
            ans = stripped.replace('Answer:', '').strip()
            print(f"  {subject} Q{q_num}: {ans}")
            q_num += 1  # increment for next

# Also extract from 2018-2024 - check all PDFs for "Answer:" pattern
print(f"\n\n{'='*60}")
print(f"CHECKING 2018-2024 for embedded answers...")
print(f"{'='*60}")

for year in range(2018, 2025):
    for paper in [1, 2]:
        filename = f"JEE_Advanced_{year}_Paper_{paper}_English.pdf"
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            continue
        
        doc = fitz.open(filepath)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        
        # Count answer lines
        answer_lines = re.findall(r'Answer\s*:\s*(.+?)(?:\n|$)', full_text)
        ans_lines = [l for l in full_text.split('\n') if 'Ans' in l and 'Q' in l]
        
        if answer_lines or ans_lines:
            print(f"\n  {year} Paper {paper}: {len(answer_lines)} 'Answer:' lines, {len(ans_lines)} 'Ans Q' lines")
            for al in (answer_lines + [l.strip() for l in ans_lines])[:5]:
                print(f"    {al[:100]}")
        else:
            print(f"  {year} Paper {paper}: NO embedded answers found")
