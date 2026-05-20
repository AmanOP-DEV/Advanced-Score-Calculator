import fitz
import os
import re

folder = r"d:\Jee Advanced Tukka Research"
outfile = os.path.join(folder, "full_text_dump_2018_2025.txt")

with open(outfile, "w", encoding="utf-8") as f:
    for year in range(2018, 2026):
        for paper in [1, 2]:
            filename = f"JEE_Advanced_{year}_Paper_{paper}_English.pdf"
            filepath = os.path.join(folder, filename)
            if not os.path.exists(filepath):
                continue
            
            f.write(f"\n{'='*80}\n")
            f.write(f"  {year} PAPER {paper}\n")
            f.write(f"{'='*80}\n")
            
            doc = fitz.open(filepath)
            total_pages = len(doc)
            f.write(f"  Total pages: {total_pages}\n\n")
            
            # Dump ALL text from every page
            for i, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    f.write(f"\n--- Page {i+1}/{total_pages} ---\n")
                    f.write(text)
                    f.write("\n")
            
            doc.close()

print(f"Done! Full text dump written to {outfile}")
