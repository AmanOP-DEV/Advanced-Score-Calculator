"""
ANALYZE STRUCTURAL FEATURES OF CORRECT vs INCORRECT OPTIONS
Extract actual option text from 2025 + 2017 PDFs (which have embedded answers)
and find what makes correct options LOOK different.
"""
import fitz
import re
from collections import Counter, defaultdict

folder = r"d:\Jee Advanced Tukka Research"

def extract_options_and_answers(filepath):
    """Extract questions with their options and correct answers from PDF."""
    doc = fitz.open(filepath)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    
    lines = full_text.split('\n')
    
    questions = []
    current_q = None
    current_options = {}
    current_answer = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect option lines: (A) ... or (B) ... etc
        opt_match = re.match(r'^\(([A-D])\)\s*(.*)', stripped)
        if opt_match:
            letter = opt_match.group(1)
            text = opt_match.group(2).strip()
            # Grab continuation lines
            j = i + 1
            while j < len(lines) and not re.match(r'^\([A-D]\)', lines[j].strip()) and not lines[j].strip().startswith('Answer:') and not re.match(r'^Q\.', lines[j].strip()) and j < i + 5:
                if lines[j].strip():
                    text += " " + lines[j].strip()
                j += 1
            current_options[letter] = text
        
        # Detect answer lines
        if stripped.startswith('Answer:') and not 'evaluated' in stripped.lower() and not 'numerical' in stripped.lower():
            ans_text = stripped.replace('Answer:', '').strip()
            if current_options:
                questions.append({
                    'options': dict(current_options),
                    'answer': ans_text,
                })
                current_options = {}
    
    return questions

out = []
def p(s=""): out.append(s)

p("=" * 80)
p(" CORRECT vs INCORRECT OPTION STRUCTURAL ANALYSIS")
p(" Looking for visual/textual patterns that survive scrambling")
p("=" * 80)

all_correct_opts = []
all_wrong_opts = []
all_questions = []

for year in [2025, 2017]:
    for paper in [1, 2]:
        filename = f"JEE_Advanced_{year}_Paper_{paper}_English.pdf"
        filepath = f"{folder}\\{filename}"
        try:
            questions = extract_options_and_answers(filepath)
        except:
            continue
        
        p(f"\n  {year} Paper {paper}: Found {len(questions)} questions with options+answers")
        
        for q in questions:
            opts = q['options']
            ans = q['answer'].strip()
            
            if not opts or len(opts) < 2:
                continue
            
            # Determine which options are correct
            correct_letters = []
            for letter in 'ABCD':
                if letter in ans or letter.lower() in ans.lower():
                    correct_letters.append(letter)
            
            # If answer is just a letter or comma-separated letters
            if not correct_letters:
                # might be a numerical or non-standard format
                continue
            
            q_data = {'options': opts, 'correct': correct_letters, 'answer': ans}
            all_questions.append(q_data)
            
            for letter, text in opts.items():
                entry = {
                    'letter': letter,
                    'text': text,
                    'length': len(text),
                    'word_count': len(text.split()),
                    'has_number': bool(re.search(r'\d', text)),
                    'has_formula': bool(re.search(r'[=<>≤≥±∞√∫∑]|sin|cos|log|ln', text)),
                    'has_negative': bool(re.search(r'(not|no |never|neither|cannot|doesn)', text.lower())),
                    'has_absolute': bool(re.search(r'(always|all |every|only|must|exactly)', text.lower())),
                    'has_qualifier': bool(re.search(r'(may|can |could|some|certain|under|if )', text.lower())),
                    'has_increase': bool(re.search(r'(increase|greater|more|higher|larger|above)', text.lower())),
                    'has_decrease': bool(re.search(r'(decrease|less|lower|smaller|below|reduce)', text.lower())),
                    'starts_with_number': bool(re.match(r'^[\d\-\+]', text)),
                    'is_correct': letter in correct_letters,
                }
                if letter in correct_letters:
                    all_correct_opts.append(entry)
                else:
                    all_wrong_opts.append(entry)

p(f"\n  Total questions analyzed: {len(all_questions)}")
p(f"  Total correct options: {len(all_correct_opts)}")
p(f"  Total wrong options: {len(all_wrong_opts)}")

# ── ANALYSIS ──
p("\n" + "█" * 70)
p(" STRUCTURAL COMPARISON: CORRECT vs WRONG OPTIONS")
p("█" * 70)

if all_correct_opts and all_wrong_opts:
    # 1. LENGTH ANALYSIS
    avg_len_correct = sum(e['length'] for e in all_correct_opts) / len(all_correct_opts)
    avg_len_wrong = sum(e['length'] for e in all_wrong_opts) / len(all_wrong_opts)
    avg_words_correct = sum(e['word_count'] for e in all_correct_opts) / len(all_correct_opts)
    avg_words_wrong = sum(e['word_count'] for e in all_wrong_opts) / len(all_wrong_opts)
    
    p(f"\n  1. OPTION LENGTH:")
    p(f"     Correct options avg: {avg_len_correct:.1f} chars, {avg_words_correct:.1f} words")
    p(f"     Wrong options avg:   {avg_len_wrong:.1f} chars, {avg_words_wrong:.1f} words")
    if avg_len_correct > avg_len_wrong:
        p(f"     → CORRECT options are {avg_len_correct/avg_len_wrong:.1f}x LONGER! ✓")
    else:
        p(f"     → WRONG options are {avg_len_wrong/avg_len_correct:.1f}x longer")
    
    # 2. FEATURE COMPARISON
    features = ['has_number', 'has_formula', 'has_negative', 'has_absolute', 
                'has_qualifier', 'has_increase', 'has_decrease', 'starts_with_number']
    
    p(f"\n  2. CONTENT FEATURES (% of options with each feature):")
    p(f"     {'Feature':<25s} {'Correct':>10s} {'Wrong':>10s} {'Signal':>10s}")
    p(f"     {'-'*60}")
    
    for feat in features:
        c_pct = sum(1 for e in all_correct_opts if e[feat]) / len(all_correct_opts) * 100
        w_pct = sum(1 for e in all_wrong_opts if e[feat]) / len(all_wrong_opts) * 100
        diff = c_pct - w_pct
        signal = "→ CORRECT" if diff > 5 else ("→ WRONG" if diff < -5 else "→ neutral")
        p(f"     {feat:<25s} {c_pct:8.1f}%  {w_pct:8.1f}%  {signal}")
    
    # 3. LENGTH BUCKETS
    p(f"\n  3. CORRECT OPTION BY LENGTH QUARTILE:")
    # Sort all options by length within each question
    for q in all_questions:
        opts_sorted = sorted(q['options'].items(), key=lambda x: len(x[1]))
        positions = {letter: i+1 for i, (letter, _) in enumerate(opts_sorted)}
        
    # Which position (shortest=1, longest=4) is most often correct?
    position_counts = Counter()
    total_q = 0
    for q in all_questions:
        if len(q['options']) < 4: continue
        opts_sorted = sorted(q['options'].items(), key=lambda x: len(x[1]))
        positions = {letter: i+1 for i, (letter, _) in enumerate(opts_sorted)}
        for cl in q['correct']:
            if cl in positions:
                position_counts[positions[cl]] += 1
                total_q += 1
    
    if total_q:
        p(f"     (1=shortest option, 4=longest option)")
        for pos in [1,2,3,4]:
            c = position_counts.get(pos, 0)
            pct = c/total_q*100
            bar = '█' * int(pct)
            label = {1:"Shortest", 2:"2nd shortest", 3:"2nd longest", 4:"Longest"}
            p(f"     {pos} ({label[pos]:>14s}): {c:3d} ({pct:5.1f}%)  {bar}")
    
    # 4. Sample correct vs wrong
    p(f"\n  4. SAMPLE CORRECT OPTIONS (what do they look like?):")
    for e in all_correct_opts[:8]:
        p(f"     ✓ [{len(e['text']):3d} chars] {e['text'][:100]}")
    
    p(f"\n  5. SAMPLE WRONG OPTIONS:")
    for e in all_wrong_opts[:8]:
        p(f"     ✗ [{len(e['text']):3d} chars] {e['text'][:100]}")

    # 5. Is the correct option often the MIDDLE length?
    p(f"\n  6. POSITION PATTERN FOR SINGLE-CORRECT Qs:")
    pos_single = Counter()
    total_single = 0
    for q in all_questions:
        if len(q['correct']) != 1 or len(q['options']) < 4: continue
        opts_sorted = sorted(q['options'].items(), key=lambda x: len(x[1]))
        positions = {letter: i+1 for i, (letter, _) in enumerate(opts_sorted)}
        cl = q['correct'][0]
        if cl in positions:
            pos_single[positions[cl]] += 1
            total_single += 1
    
    if total_single:
        p(f"     Single-correct Qs only (n={total_single}):")
        for pos in [1,2,3,4]:
            c = pos_single.get(pos, 0)
            pct = c/total_single*100
            bar = '█' * int(pct/2)
            p(f"     Position {pos}: {c:3d} ({pct:5.1f}%)  {bar}")

outpath = r"d:\Jee Advanced Tukka Research\OPTION_STRUCTURE_ANALYSIS.txt"
with open(outpath, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Analysis written to {outpath}")
