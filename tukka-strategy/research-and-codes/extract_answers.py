import fitz  # PyMuPDF
import os
import re
import sys

folder = r"d:\Jee Advanced Tukka Research"
outfile = os.path.join(folder, "raw_answers_dump.txt")

with open(outfile, "w", encoding="utf-8") as f:
    for year in range(2017, 2026):
        for paper in [1, 2]:
            filename = f"JEE_Advanced_{year}_Paper_{paper}_English.pdf"
            filepath = os.path.join(folder, filename)
            if not os.path.exists(filepath):
                f.write(f"--- MISSING: {filename} ---\n")
                continue
            
            f.write(f"\n{'='*80}\n")
            f.write(f"  {year} PAPER {paper}\n")
            f.write(f"{'='*80}\n")
            
            doc = fitz.open(filepath)
            total_pages = len(doc)
            
            # Extract ALL text from entire document
            full_text = ""
            for i, page in enumerate(doc):
                text = page.get_text()
                full_text += text
            
            # Find all answer lines using regex
            # Common patterns: "Ans for Q.X:", "Answer:", "Q.X  A" etc.
            ans_patterns = [
                r'Ans\.?\s*(?:for\s*)?(?:Q\.?\s*)?(\d+)\s*[:\.]\s*(.*?)(?:\n|$)',
                r'Answer\s*(?:for\s*)?(?:Q\.?\s*)?(\d+)\s*[:\.]\s*(.*?)(?:\n|$)',
                r'Q\.?\s*(\d+)\s*[:\.]\s*\(?([A-D](?:\s*,\s*[A-D])*)\)?\s*$',
                r'(\d+)\s*\.\s*\(?([A-D](?:\s*,\s*[A-D])*)\)?\s*$',
                r'Ans\s*(?:for\s+)?Q\.(\d+)\s*:\s*(.*)',
            ]
            
            f.write(f"  Total pages: {total_pages}\n\n")
            
            # Write full text for analysis
            f.write("--- FULL TEXT DUMP ---\n")
            # Only write portions containing "Ans" or "answer" or answer-key-like content
            lines = full_text.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower().strip()
                if any(kw in line_lower for kw in ['ans ', 'ans.', 'answer', 'correct', 'key', 'option']):
                    # Write context: 1 line before and after
                    for j in range(max(0, i-1), min(len(lines), i+2)):
                        f.write(f"  L{j}: {lines[j]}\n")
                    f.write("  ---\n")
            
            doc.close()

print(f"Done! Output written to {outfile}")
