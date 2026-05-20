import fitz
import re
from collections import Counter
from master_analysis import DATA

folder = r"d:\Jee Advanced Tukka Research"

def extract_all_options(filepath):
    """Extract ALL option texts grouped by question from PDF."""
    doc = fitz.open(filepath)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    
    lines = full_text.split('\n')
    questions = {}
    current_opts = {}
    
    # We need to track the question number somehow.
    # Questions usually start with a number like "1." or "Q.1"
    qnum = 0
    
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        
        q_match = re.match(r'^(?:Q\.?\s*)?(\d+)\s*\.', stripped)
        if q_match:
            qnum = int(q_match.group(1))
            
        opt_match = re.match(r'^\(([A-D])\)\s*(.*)', stripped)
        if opt_match:
            letter = opt_match.group(1)
            text = opt_match.group(2).strip()
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if re.match(r'^\([A-D]\)', next_line) or re.match(r'^(?:Q\.?\s*)?\d+\s*\.', next_line) or next_line.startswith('SECTION'):
                    break
                if next_line:
                    text += " " + next_line
                j += 1
                if j > i + 8: break
            
            current_opts[letter] = text
            
            if letter == 'D' and len(current_opts) >= 3 and qnum > 0:
                questions[qnum] = dict(current_opts)
                current_opts = {}
        
        i += 1
    
    return questions

all_correct_lens = []
all_wrong_lens = []
all_correct_positions = [] # 1=shortest, 4=longest

# Try to match across all years and subjects
for year, papers in DATA.items():
    for paper_num, subjects in papers.items():
        filename = f"JEE_Advanced_{year}_Paper_{paper_num}_English.pdf"
        filepath = f"{folder}\\{filename}"
        
        try:
            extracted_qs = extract_all_options(filepath)
        except: continue
        
        # We need to map qnum. BUT wait, qnum resets per subject or per section?
        # Typically qnums are 1-18 for PHY, 19-36 for CHEM, etc.
        # Let's iterate over subjects in DATA and check if qnum matches.
        for subj, answers in subjects.items():
            for qnum, ans in answers.items():
                if qnum in extracted_qs:
                    opts = extracted_qs[qnum]
                    # Only single correct
                    if len(ans) == 1 and ans in 'ABCD':
                        # Valid single correct question
                        correct_letter = ans
                        
                        sorted_opts = sorted(opts.items(), key=lambda x: len(x[1]))
                        length_positions = {}
                        for rank, (letter, text) in enumerate(sorted_opts):
                            length_positions[letter] = rank + 1
                            
                        for letter in 'ABCD':
                            if letter not in opts: continue
                            opt_len = len(opts[letter])
                            if letter == correct_letter:
                                all_correct_lens.append(opt_len)
                                if letter in length_positions:
                                    all_correct_positions.append(length_positions[letter])
                            else:
                                all_wrong_lens.append(opt_len)

print(f"Total single correct questions matched: {len(all_correct_positions)}")
if all_correct_positions:
    avg_c = sum(all_correct_lens)/len(all_correct_lens)
    avg_w = sum(all_wrong_lens)/len(all_wrong_lens)
    print(f"Correct Options Avg Length: {avg_c:.1f}")
    print(f"Wrong Options Avg Length: {avg_w:.1f}")
    
    ct = Counter(all_correct_positions)
    for pos in [1,2,3,4]:
        c = ct.get(pos, 0)
        pct = c / len(all_correct_positions) * 100
        labels = {1:"SHORTEST", 2:"2nd shortest", 3:"2nd longest", 4:"LONGEST"}
        print(f"Position {pos} ({labels[pos]}): {c} ({pct:.1f}%)")
