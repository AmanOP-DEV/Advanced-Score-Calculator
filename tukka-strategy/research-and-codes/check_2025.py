import fitz
import os
import re

folder = r"d:\Jee Advanced Tukka Research"

# Check 2025 PDFs for embedded answers
for paper in [1, 2]:
    filename = f"JEE_Advanced_2025_Paper_{paper}_English.pdf"
    filepath = os.path.join(folder, filename)
    doc = fitz.open(filepath)
    
    print(f"\n{'='*60}")
    print(f"2025 Paper {paper} — searching for answers...")
    print(f"{'='*60}")
    
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    # Search for answer patterns
    for pattern_name, pattern in [
        ("Ans for Q", r'Ans\s+for\s+Q\.?\s*(\d+)\s*:\s*(.+?)(?:\r?\n|$)'),
        ("Answer:", r'Answer\s*:\s*(.+?)(?:\r?\n|$)'),
        ("Correct Answer", r'Correct\s+Answer\s*[:\-]\s*(.+?)(?:\r?\n|$)'),
        ("correct option", r'correct\s+option[s]?\s*[:\-]\s*(.+?)(?:\r?\n|$)'),
        ("(A) or (B) style", r'Q\.?\s*(\d+)\s*\.\s*\(([A-D])\)'),
    ]:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            print(f"\n  Pattern '{pattern_name}' found {len(matches)} matches:")
            for m in matches[:10]:
                print(f"    {m}")
    
    # Also dump lines containing "ans" or "answer" or "correct"
    lines = full_text.split('\n')
    ans_lines = []
    for i, line in enumerate(lines):
        ll = line.lower().strip()
        if 'ans' in ll or 'correct answer' in ll or 'key' in ll:
            ans_lines.append((i, line.strip()))
    
    if ans_lines:
        print(f"\n  Lines with 'ans/answer/key' ({len(ans_lines)} found):")
        for idx, line in ans_lines[:30]:
            print(f"    L{idx}: {line[:120]}")
    else:
        print(f"\n  No 'ans/answer/key' lines found in text extraction.")
    
    doc.close()
