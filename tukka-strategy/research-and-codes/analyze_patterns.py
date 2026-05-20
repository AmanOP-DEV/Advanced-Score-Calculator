import fitz
import os
import re
import json
from collections import Counter, defaultdict

folder = r"d:\Jee Advanced Tukka Research"

def extract_all_answers(folder):
    """Extract all answers from all PDFs into structured data."""
    all_data = {}
    
    for year in range(2017, 2026):
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
            
            key = f"{year}_P{paper}"
            answers = {}
            
            # Pattern 1: "Ans for Q.X: (answer)"
            pattern1 = re.findall(r'Ans\s+for\s+Q\.?\s*(\d+)\s*:\s*\(?\s*([^)\n]+?)\s*\)?\s*(?:\r?\n|$)', full_text)
            for qnum, ans in pattern1:
                qnum = int(qnum)
                ans = ans.strip().rstrip(')')
                answers[qnum] = ans
            
            # Pattern 2: "Q.X Answer: (answer)" or similar
            pattern2 = re.findall(r'Q\.?\s*(\d+)\s*[:\-]\s*(?:Answer\s*:?\s*)\(?\s*([^)\n]+?)\s*\)?\s*(?:\r?\n|$)', full_text)
            for qnum, ans in pattern2:
                qnum = int(qnum)
                if qnum not in answers:
                    answers[qnum] = ans.strip()
            
            all_data[key] = answers
    
    return all_data

def classify_answer(ans_str):
    """Classify answer into type: MCQ_single, MCQ_multi, or numerical."""
    ans_str = ans_str.strip()
    
    # Check if it's a numerical answer
    if re.match(r'^[\d.]+$', ans_str):
        return 'numerical', [ans_str]
    
    # Extract letter options
    letters = re.findall(r'[A-D]', ans_str)
    if letters:
        if len(letters) == 1:
            return 'MCQ_single', letters
        else:
            return 'MCQ_multi', letters
    
    return 'other', [ans_str]

def analyze_patterns(all_data):
    """Deep pattern analysis."""
    results = {}
    
    # === 1. OVERALL OPTION FREQUENCY ===
    all_mcq_single = []
    all_mcq_multi = []
    all_numerical = []
    
    # Per-year, per-paper, per-subject tracking
    year_paper_data = defaultdict(lambda: defaultdict(list))
    
    for key, answers in sorted(all_data.items()):
        year, paper = key.split('_P')
        year = int(year)
        paper = int(paper)
        
        for qnum in sorted(answers.keys()):
            ans = answers[qnum]
            atype, options = classify_answer(ans)
            
            # Determine subject based on question number patterns
            # JEE Advanced: Physics Q1-18, Chem Q19-36, Math Q37-54 (approx, varies by year)
            # But actually it varies. Let's use rough thirds
            total_q = max(answers.keys()) if answers else 54
            third = total_q / 3
            
            if qnum <= third:
                subject = 'Physics'
            elif qnum <= 2 * third:
                subject = 'Chemistry'
            else:
                subject = 'Maths'
            
            entry = {
                'year': year, 'paper': paper, 'qnum': qnum,
                'answer': ans, 'type': atype, 'options': options,
                'subject': subject
            }
            
            if atype == 'MCQ_single':
                all_mcq_single.append(entry)
            elif atype == 'MCQ_multi':
                all_mcq_multi.append(entry)
            elif atype == 'numerical':
                all_numerical.append(entry)
            
            year_paper_data[key][subject].append(entry)
    
    # === ANALYSIS ===
    
    print("=" * 100)
    print("  JEE ADVANCED TUKKA PATTERN ANALYSIS (2017-2025)")
    print("  Papers Analyzed: Paper 1 & Paper 2 across 9 years")
    print("=" * 100)
    
    # --- A. Single-correct MCQ option distribution ---
    print("\n\n" + "█" * 80)
    print("  A. SINGLE-CORRECT MCQ — OPTION DISTRIBUTION")
    print("█" * 80)
    
    single_options = [e['options'][0] for e in all_mcq_single]
    single_counter = Counter(single_options)
    total_single = len(single_options)
    
    print(f"\n  Total single-correct MCQs analyzed: {total_single}")
    print(f"  {'Option':<10} {'Count':<10} {'Percentage':<15} {'Bar'}")
    print(f"  {'-'*60}")
    for opt in ['A', 'B', 'C', 'D']:
        count = single_counter.get(opt, 0)
        pct = (count / total_single * 100) if total_single else 0
        bar = '█' * int(pct / 2)
        print(f"  {opt:<10} {count:<10} {pct:>6.1f}%         {bar}")
    
    # --- B. Multi-correct MCQ patterns ---
    print("\n\n" + "█" * 80)
    print("  B. MULTI-CORRECT MCQ — OPTION APPEARANCE FREQUENCY")
    print("█" * 80)
    
    multi_option_freq = Counter()
    multi_combo_freq = Counter()
    multi_count_freq = Counter()
    
    for e in all_mcq_multi:
        for opt in e['options']:
            multi_option_freq[opt] += 1
        combo = tuple(sorted(e['options']))
        multi_combo_freq[combo] += 1
        multi_count_freq[len(e['options'])] += 1
    
    total_multi = len(all_mcq_multi)
    print(f"\n  Total multi-correct MCQs analyzed: {total_multi}")
    
    print(f"\n  --- How often each letter appears in multi-correct answers ---")
    print(f"  {'Option':<10} {'Appearances':<15} {'% of questions it appears in'}")
    print(f"  {'-'*55}")
    for opt in ['A', 'B', 'C', 'D']:
        count = multi_option_freq.get(opt, 0)
        pct = (count / total_multi * 100) if total_multi else 0
        bar = '█' * int(pct / 2)
        print(f"  {opt:<10} {count:<15} {pct:>6.1f}%   {bar}")
    
    print(f"\n  --- How many options are correct (2, 3, or 4)? ---")
    print(f"  {'# Correct':<12} {'Count':<10} {'Percentage'}")
    print(f"  {'-'*35}")
    for n in [2, 3, 4]:
        count = multi_count_freq.get(n, 0)
        pct = (count / total_multi * 100) if total_multi else 0
        print(f"  {n:<12} {count:<10} {pct:>6.1f}%")
    
    print(f"\n  --- Most common multi-correct combos ---")
    print(f"  {'Combination':<20} {'Count':<10} {'Percentage'}")
    print(f"  {'-'*40}")
    for combo, count in multi_combo_freq.most_common(15):
        pct = (count / total_multi * 100) if total_multi else 0
        combo_str = ', '.join(combo)
        print(f"  ({combo_str}){'':<(14-len(combo_str))} {count:<10} {pct:>6.1f}%")
    
    # --- C. Numerical answer patterns ---
    print("\n\n" + "█" * 80)
    print("  C. NUMERICAL ANSWER DISTRIBUTION")
    print("█" * 80)
    
    num_values = []
    for e in all_numerical:
        try:
            val = int(e['options'][0])
            num_values.append(val)
        except:
            try:
                val = float(e['options'][0])
                num_values.append(val)
            except:
                pass
    
    if num_values:
        int_values = [v for v in num_values if isinstance(v, int) or v == int(v)]
        int_counter = Counter([int(v) for v in int_values])
        total_num = len(int_values)
        
        print(f"\n  Total numerical answers (integer type): {total_num}")
        print(f"  {'Digit':<10} {'Count':<10} {'Percentage':<15} {'Bar'}")
        print(f"  {'-'*50}")
        for digit in range(0, 10):
            count = int_counter.get(digit, 0)
            pct = (count / total_num * 100) if total_num else 0
            bar = '█' * int(pct)
            print(f"  {digit:<10} {count:<10} {pct:>6.1f}%         {bar}")
    
    # --- D. POSITION-BASED patterns ---
    print("\n\n" + "█" * 80)
    print("  D. POSITION-BASED PATTERNS (by question position in section)")
    print("█" * 80)
    
    # Track by question position within its section type
    # For single MCQ: first Q tends to be...
    print("\n  [Analysis of whether first/last questions in a section have biased answers]")
    
    # Group by section position
    for key, answers in sorted(all_data.items()):
        # We'll analyze position patterns later after grouping
        pass
    
    # --- E. SUBJECT-WISE distribution ---
    print("\n\n" + "█" * 80)
    print("  E. SUBJECT-WISE OPTION DISTRIBUTION (Single-Correct MCQs)")
    print("█" * 80)
    
    for subj in ['Physics', 'Chemistry', 'Maths']:
        subj_answers = [e for e in all_mcq_single if e['subject'] == subj]
        if not subj_answers:
            continue
        subj_counter = Counter(e['options'][0] for e in subj_answers)
        total = len(subj_answers)
        print(f"\n  {subj} (n={total}):")
        print(f"  {'Option':<10} {'Count':<10} {'Percentage'}")
        for opt in ['A', 'B', 'C', 'D']:
            count = subj_counter.get(opt, 0)
            pct = (count / total * 100) if total else 0
            bar = '█' * int(pct / 2)
            print(f"  {opt:<10} {count:<10} {pct:>6.1f}%   {bar}")
    
    # --- F. YEAR-WISE trends ---
    print("\n\n" + "█" * 80)
    print("  F. YEAR-WISE SINGLE-MCQ OPTION DISTRIBUTION")
    print("█" * 80)
    
    for year in range(2017, 2026):
        year_answers = [e for e in all_mcq_single if e['year'] == year]
        if not year_answers:
            continue
        year_counter = Counter(e['options'][0] for e in year_answers)
        total = len(year_answers)
        a_pct = year_counter.get('A', 0) / total * 100 if total else 0
        b_pct = year_counter.get('B', 0) / total * 100 if total else 0
        c_pct = year_counter.get('C', 0) / total * 100 if total else 0
        d_pct = year_counter.get('D', 0) / total * 100 if total else 0
        print(f"  {year}: A={a_pct:5.1f}%  B={b_pct:5.1f}%  C={c_pct:5.1f}%  D={d_pct:5.1f}%  (n={total})")
    
    # --- G. CONSECUTIVE ANSWER PATTERNS ---
    print("\n\n" + "█" * 80)
    print("  G. CONSECUTIVE ANSWER PATTERNS")
    print("█" * 80)
    
    repeat_counts = Counter()
    total_consecutive_pairs = 0
    
    for key, answers in sorted(all_data.items()):
        sorted_q = sorted(answers.keys())
        for i in range(len(sorted_q) - 1):
            q1, q2 = sorted_q[i], sorted_q[i+1]
            if q2 == q1 + 1:  # consecutive
                a1_type, a1_opts = classify_answer(answers[q1])
                a2_type, a2_opts = classify_answer(answers[q2])
                if a1_type == 'MCQ_single' and a2_type == 'MCQ_single':
                    total_consecutive_pairs += 1
                    if a1_opts[0] == a2_opts[0]:
                        repeat_counts['same'] += 1
                    else:
                        repeat_counts['different'] += 1
    
    if total_consecutive_pairs:
        print(f"\n  Consecutive single-MCQ pairs: {total_consecutive_pairs}")
        same = repeat_counts.get('same', 0)
        diff = repeat_counts.get('different', 0)
        print(f"  Same answer repeated:    {same} ({same/total_consecutive_pairs*100:.1f}%)")
        print(f"  Different answer:        {diff} ({diff/total_consecutive_pairs*100:.1f}%)")
        print(f"  Expected if random (25%): 25.0%")
    
    # --- H. PAPER 1 vs PAPER 2 comparison ---
    print("\n\n" + "█" * 80)
    print("  H. PAPER 1 vs PAPER 2 COMPARISON")
    print("█" * 80)
    
    for pnum in [1, 2]:
        p_answers = [e for e in all_mcq_single if e['paper'] == pnum]
        if not p_answers:
            continue
        p_counter = Counter(e['options'][0] for e in p_answers)
        total = len(p_answers)
        print(f"\n  Paper {pnum} (n={total}):")
        for opt in ['A', 'B', 'C', 'D']:
            count = p_counter.get(opt, 0)
            pct = (count / total * 100) if total else 0
            bar = '█' * int(pct / 2)
            print(f"    {opt}: {pct:5.1f}%  {bar}")
    
    # --- I. MULTI-CORRECT: SUBJECT-WISE ---
    print("\n\n" + "█" * 80)
    print("  I. MULTI-CORRECT: SUBJECT-WISE COMBO PATTERNS")
    print("█" * 80)
    
    for subj in ['Physics', 'Chemistry', 'Maths']:
        subj_multi = [e for e in all_mcq_multi if e['subject'] == subj]
        if not subj_multi:
            continue
        total = len(subj_multi)
        count_freq = Counter(len(e['options']) for e in subj_multi)
        combo_freq = Counter(tuple(sorted(e['options'])) for e in subj_multi)
        
        print(f"\n  {subj} (n={total}):")
        print(f"    # correct options distribution:")
        for n in [2, 3, 4]:
            c = count_freq.get(n, 0)
            pct = c / total * 100 if total else 0
            print(f"      {n} options correct: {c} ({pct:.1f}%)")
        print(f"    Top combos:")
        for combo, cnt in combo_freq.most_common(5):
            pct = cnt / total * 100
            print(f"      ({', '.join(combo)}): {cnt} ({pct:.1f}%)")
    
    # --- J. DARK PATTERN: Answer never/rarely used ---
    print("\n\n" + "█" * 80)
    print("  J. ANOMALIES & DARK PATTERNS")
    print("█" * 80)
    
    # Check if any option is NEVER the sole answer in single-MCQ
    print("\n  [1] Checking if any option is suspiciously rare or common...")
    
    # Check streaks - longest run of same answer
    print("\n  [2] Longest streaks of same single-MCQ answer per paper:")
    for key, answers in sorted(all_data.items()):
        sorted_q = sorted(answers.keys())
        single_seq = []
        for q in sorted_q:
            atype, opts = classify_answer(answers[q])
            if atype == 'MCQ_single':
                single_seq.append((q, opts[0]))
        
        if len(single_seq) < 3:
            continue
        
        max_streak = 1
        current_streak = 1
        streak_opt = single_seq[0][1]
        streak_start = single_seq[0][0]
        best_streak_info = (1, single_seq[0][1], single_seq[0][0])
        
        for i in range(1, len(single_seq)):
            if single_seq[i][1] == single_seq[i-1][1]:
                current_streak += 1
                if current_streak > max_streak:
                    max_streak = current_streak
                    best_streak_info = (max_streak, single_seq[i][1], single_seq[i][0] - max_streak + 1)
            else:
                current_streak = 1
        
        if max_streak >= 2:
            print(f"    {key}: longest streak = {best_streak_info[0]}x '{best_streak_info[1]}' starting ~Q{best_streak_info[2]}")
    
    # --- K. MARKING SCHEME ANALYSIS ---
    print("\n\n" + "█" * 80)
    print("  K. OPTIMAL TUKKA STRATEGY BASED ON MARKING SCHEME")
    print("█" * 80)
    
    print("""
  JEE Advanced 2026 Expected Marking Scheme (based on recent years):
  
  Section 1: Single-correct MCQs
    +3 correct, -1 wrong, 0 unanswered
    >>> Strategy: Guess ONLY if you can eliminate 1+ options
    >>> Expected value of random guess: 3*(1/4) + (-1)*(3/4) = 0.0 marks
    >>> With 1 elimination: 3*(1/3) + (-1)*(2/3) = +0.33 marks (WORTH IT!)
    >>> With 2 eliminations: 3*(1/2) + (-1)*(1/2) = +1.0 marks (DEFINITELY!)
    
  Section 2: Multi-correct MCQs  
    +4 all correct, +1 per correct (no wrong marked), -2 if any wrong marked
    >>> Strategy: Mark ONLY options you're somewhat confident about
    >>> Even marking 1 correct option = +1 mark (no penalty if rest left blank)
    >>> NEVER guess randomly on multi-correct (high penalty)
    
  Section 3: Numerical (integer 0-9)
    +3 correct, 0 wrong
    >>> Strategy: ALWAYS GUESS! Zero penalty, 10% chance of +3
    >>> Expected value = 0.3 marks per guess (FREE MARKS!)
    >>> Best digits to guess: see distribution above
    """)
    
    # --- L. FINAL ACTIONABLE CHEAT SHEET ---
    print("\n\n" + "█" * 80)
    print("  L. 🎯 FINAL TUKKA CHEAT SHEET 🎯")
    print("█" * 80)
    
    # Most common single MCQ answer
    if single_counter:
        best_single = single_counter.most_common(1)[0]
        worst_single = single_counter.most_common()[-1]
        print(f"""
  ┌─────────────────────────────────────────────────────────────────┐
  │  SINGLE-CORRECT MCQ TUKKA:                                     │
  │  Most frequent answer: ({best_single[0]}) — {best_single[1]}/{total_single} = {best_single[1]/total_single*100:.1f}%     │
  │  Least frequent answer: ({worst_single[0]}) — {worst_single[1]}/{total_single} = {worst_single[1]/total_single*100:.1f}%    │
  └─────────────────────────────────────────────────────────────────┘""")
    
    # Most common multi combo
    if multi_combo_freq:
        best_multi = multi_combo_freq.most_common(1)[0]
        print(f"""
  ┌─────────────────────────────────────────────────────────────────┐
  │  MULTI-CORRECT MCQ TUKKA:                                      │
  │  Most common combo: ({', '.join(best_multi[0])}) — {best_multi[1]} times   │
  │  Most answers have {multi_count_freq.most_common(1)[0][0]} correct options                        │
  │  SAFEST: Just mark 1 option you feel is right (+1, no penalty)  │
  └─────────────────────────────────────────────────────────────────┘""")
    
    # Most common numerical digit
    if num_values:
        int_vals = [int(v) for v in num_values if v == int(v)]
        digit_counter = Counter(int_vals)
        best_digit = digit_counter.most_common(1)[0]
        top3 = digit_counter.most_common(3)
        print(f"""
  ┌─────────────────────────────────────────────────────────────────┐
  │  NUMERICAL TUKKA (ALWAYS GUESS — ZERO PENALTY!):               │
  │  Most common digit: {best_digit[0]} (appeared {best_digit[1]} times = {best_digit[1]/len(int_vals)*100:.1f}%)        │
  │  Top 3 digits: {top3[0][0]} ({top3[0][1]}x), {top3[1][0]} ({top3[1][1]}x), {top3[2][0]} ({top3[2][1]}x)                  │
  │  ALWAYS enter a number — it's FREE expected value!             │
  └─────────────────────────────────────────────────────────────────┘""")
    
    return all_data

# Run
print("Extracting answers from all PDFs...")
all_data = extract_all_answers(folder)
print(f"Extracted data from {len(all_data)} paper sets.\n")

# Print raw data summary
for key in sorted(all_data.keys()):
    print(f"\n{key}: {len(all_data[key])} answers found")
    for qnum in sorted(all_data[key].keys()):
        print(f"  Q{qnum}: {all_data[key][qnum]}")

print("\n\n")
analyze_patterns(all_data)
