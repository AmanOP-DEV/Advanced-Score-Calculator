"""
DEEPER OPTION STRUCTURE ANALYSIS
Improved parser + analysis of ALL PDFs with questions
"""
import fitz
import re
from collections import Counter

folder = r"d:\Jee Advanced Tukka Research"

def extract_all_options(filepath):
    """Extract ALL option texts grouped by question from PDF."""
    doc = fitz.open(filepath)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    
    lines = full_text.split('\n')
    
    questions = []
    current_opts = {}
    answers_after = []
    
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        
        # Match option line: (A) text or (A)text  
        opt_match = re.match(r'^\(([A-D])\)\s*(.*)', stripped)
        if opt_match:
            letter = opt_match.group(1)
            text = opt_match.group(2).strip()
            # Grab continuation
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if re.match(r'^\([A-D]\)', next_line) or next_line.startswith('Answer:') or re.match(r'^Q\.', next_line) or next_line.startswith('SECTION'):
                    break
                if next_line:
                    text += " " + next_line
                j += 1
                if j > i + 8: break
            
            current_opts[letter] = text
            
            # If we've seen D, save the question
            if letter == 'D' and len(current_opts) >= 3:
                questions.append(dict(current_opts))
                current_opts = {}
        
        # Track answer
        if stripped.startswith('Answer:') and 'evaluated' not in stripped.lower() and 'numerical' not in stripped.lower() and 'keypad' not in stripped.lower():
            ans_text = stripped.replace('Answer:', '').strip()
            if ans_text and len(ans_text) < 20:
                answers_after.append(ans_text)
        
        i += 1
    
    return questions, answers_after

out = []
def p(s=""): out.append(s)

p("=" * 80)
p(" OPTION CONTENT SIMILARITY ANALYSIS v2")
p("=" * 80)

all_opt_lengths_by_position = {1:[], 2:[], 3:[], 4:[]}  # sorted by length
all_correct_positions = []  # which length-position is correct
all_correct_lens = []
all_wrong_lens = []

for year in range(2017, 2026):
    for paper in [1, 2]:
        filename = f"JEE_Advanced_{year}_Paper_{paper}_English.pdf"
        filepath = f"{folder}\\{filename}"
        try:
            questions, answers = extract_all_options(filepath)
        except Exception as e:
            continue
        
        p(f"\n  {year} P{paper}: {len(questions)} questions with 4 options, {len(answers)} answers found")
        
        # Match answers to questions (answers come after questions in 2025 papers)
        if answers and year in [2025, 2017]:
            for qi in range(min(len(questions), len(answers))):
                q = questions[qi]
                a = answers[qi] if qi < len(answers) else ""
                
                # Which letters are correct
                correct_letters = [c for c in 'ABCD' if c in a]
                if not correct_letters: continue
                
                # Sort options by length
                sorted_opts = sorted(q.items(), key=lambda x: len(x[1]))
                length_positions = {}
                for rank, (letter, text) in enumerate(sorted_opts):
                    length_positions[letter] = rank + 1  # 1=shortest, 4=longest
                
                for letter in 'ABCD':
                    if letter not in q: continue
                    opt_len = len(q[letter])
                    if letter in correct_letters:
                        all_correct_lens.append(opt_len)
                        if letter in length_positions:
                            all_correct_positions.append(length_positions[letter])
                    else:
                        all_wrong_lens.append(opt_len)
        
        # For ALL years: just collect option length distributions
        for q in questions:
            if len(q) < 4: continue
            sorted_by_len = sorted(q.values(), key=len)
            for rank, text in enumerate(sorted_by_len):
                all_opt_lengths_by_position[rank+1].append(len(text))

# ── RESULTS ──
p("\n" + "█" * 70)
p(" KEY FINDINGS")
p("█" * 70)

if all_correct_lens and all_wrong_lens:
    avg_c = sum(all_correct_lens)/len(all_correct_lens)
    avg_w = sum(all_wrong_lens)/len(all_wrong_lens)
    median_c = sorted(all_correct_lens)[len(all_correct_lens)//2]
    median_w = sorted(all_wrong_lens)[len(all_wrong_lens)//2]
    
    p(f"\n  OPTION LENGTH (characters):")
    p(f"    Correct options: avg={avg_c:.1f}, median={median_c}")
    p(f"    Wrong options:   avg={avg_w:.1f}, median={median_w}")
    p(f"    Ratio: correct is {avg_c/avg_w:.2f}x the length of wrong")
    
    # Length distribution
    p(f"\n  LENGTH BUCKETS:")
    buckets = [(0,10,"Very short 0-10"),(11,25,"Short 11-25"),(26,50,"Medium 26-50"),
               (51,100,"Long 51-100"),(101,500,"Very long 101+")]
    for lo,hi,label in buckets:
        cc = sum(1 for l in all_correct_lens if lo<=l<=hi)
        wc = sum(1 for l in all_wrong_lens if lo<=l<=hi)
        c_pct = cc/len(all_correct_lens)*100
        w_pct = wc/len(all_wrong_lens)*100
        p(f"    {label:>20s}: correct={c_pct:5.1f}%  wrong={w_pct:5.1f}%")

if all_correct_positions:
    p(f"\n  CORRECT ANSWER'S LENGTH-RANK POSITION (1=shortest, 4=longest):")
    p(f"  n={len(all_correct_positions)}")
    ct = Counter(all_correct_positions)
    for pos in [1,2,3,4]:
        c = ct.get(pos,0)
        pct = c/len(all_correct_positions)*100
        bar = '█' * int(pct/2)
        labels = {1:"SHORTEST opt", 2:"2nd shortest", 3:"2nd longest", 4:"LONGEST opt"}
        p(f"    {pos} ({labels[pos]:>14s}): {c:3d} ({pct:5.1f}%)  {bar}")
    
    p(f"\n  INTERPRETATION:")
    best_pos = ct.most_common(1)[0]
    worst_pos = ct.most_common()[-1]
    p(f"    → The {['','shortest','2nd shortest','2nd longest','longest'][best_pos[0]]} option is correct {best_pos[1]/len(all_correct_positions)*100:.0f}% of the time")
    p(f"    → The {['','shortest','2nd shortest','2nd longest','longest'][worst_pos[0]]} option is correct only {worst_pos[1]/len(all_correct_positions)*100:.0f}% of the time")

# Compare option text patterns across ALL years (even without answers)
p(f"\n  OPTION LENGTH STATISTICS ACROSS ALL YEARS:")
for rank in [1,2,3,4]:
    lengths = all_opt_lengths_by_position[rank]
    if lengths:
        avg = sum(lengths)/len(lengths)
        p(f"    Position {rank} (by length): avg={avg:.1f} chars, n={len(lengths)}")

outpath = r"d:\Jee Advanced Tukka Research\OPTION_SIMILARITY_v2.txt"
with open(outpath, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Written to {outpath}")
