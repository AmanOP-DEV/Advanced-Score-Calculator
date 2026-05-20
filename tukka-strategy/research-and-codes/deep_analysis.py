"""
MILITARY-GRADE JEE ADVANCED PATTERN ANALYSIS
Deep statistical analysis for optimal guessing strategy
"""
from collections import Counter, defaultdict
import json

# ============================================================
# COMPLETE DATABASE — All MCQ answers organized by SECTION TYPE
# Section 1: Single MCQ (4 Qs per subject = 12 total)
# Section 2: Multi-correct (3-4 Qs per subject)  
# Section 3: Numerical (6-8 Qs per subject)
# Section 4: Single MCQ paragraph-based (if exists)
# ============================================================

# Structured: {year: {paper: [list of (subject, section_type, q_position_in_section, answer)]}}
# section_type: "S" = single, "M" = multi, "N" = numerical, "P" = paragraph single

ALL = []

def add(year, paper, subj, sec_type, pos, ans):
    ALL.append({
        'year': year, 'paper': paper, 'subj': subj,
        'sec': sec_type, 'pos': pos, 'ans': ans,
        'letters': [c.strip() for c in ans.split(',') if c.strip() in ['A','B','C','D']],
        'is_single': len([c.strip() for c in ans.split(',') if c.strip() in ['A','B','C','D']]) == 1,
        'is_multi': len([c.strip() for c in ans.split(',') if c.strip() in ['A','B','C','D']]) > 1,
    })

# === 2024 P1 (most recent complete, highest weight) ===
# Section 1: Single MCQ Q1-4 per subject
for s, answers in [("PHY",["A","A","B","C"]),("CHEM",["D","A","B","C"]),("MATH",["B","C","B","A"])]:
    for i, a in enumerate(answers): add(2024,1,s,"S",i+1,a)
# Section 2: Multi Q5-7
for s, answers in [("PHY",["A,B,C","A,C,D","A,B"]),("CHEM",["A,B,C","A,B,D","A,D"]),("MATH",["A,C,D","B,C,D","A,B,C"])]:
    for i, a in enumerate(answers): add(2024,1,s,"M",i+1,a)
# Section 4: Paragraph single Q14-17
for s, answers in [("PHY",["B","C","A","A"]),("CHEM",["C","B","A","C"]),("MATH",["C","C","C","C"])]:
    for i, a in enumerate(answers): add(2024,1,s,"P",i+1,a)

# === 2024 P2 ===
for s, answers in [("PHY",["A","A","A","A"]),("CHEM",["B","D","D","B"]),("MATH",["B","B","B","D"])]:
    for i, a in enumerate(answers): add(2024,2,s,"S",i+1,a)
for s, answers in [("PHY",["B,D","A,B,D","A,B"]),("CHEM",["A,C","C,D","B,D"]),("MATH",["B,C","A,C","A,C"])]:
    for i, a in enumerate(answers): add(2024,2,s,"M",i+1,a)

# === 2025 P1 ===
for s, answers in [("PHY",["C","A","D","A"]),("CHEM",["A","A","B","B"]),("MATH",["C","C","",""])]:
    for i, a in enumerate(answers):
        if a: add(2025,1,s,"S",i+1,a)
for s, answers in [("PHY",["B,D","D","A,D"]),("CHEM",["B,C","A,B","B"]),("MATH",["A,C","A,D","A,D"])]:
    for i, a in enumerate(answers): add(2025,1,s,"M",i+1,a)
for s, answers in [("PHY",["C","A","C"]),("CHEM",["A","B","B"]),("MATH",["C","B","A"])]:
    for i, a in enumerate(answers): add(2025,1,s,"P",i+1,a)

# === 2025 P2 ===
for s, answers in [("PHY",["B","C","C",""]),("CHEM",["A","A","D","C"]),("MATH",["C","B","C","A"])]:
    for i, a in enumerate(answers):
        if a: add(2025,2,s,"S",i+1,a)
for s, answers in [("PHY",["A,B,C","A,B","A","A,B,C"]),("CHEM",["C,D","B,D","A,C","B,C"]),("MATH",["A,B","A,C","A,C","B,C,D"])]:
    for i, a in enumerate(answers): add(2025,2,s,"M",i+1,a)

# === 2023 P1 ===
for s, answers in [("PHY",["A","B","A","A"]),("CHEM",["C","A","B","B"]),("MATH",["C","A","B","A"])]:
    for i, a in enumerate(answers): add(2023,1,s,"S",i+1,a)
for s, answers in [("PHY",["A,C,D","A,C,D","A,B,C,D"]),("CHEM",["B,C,D","C,D","B"]),("MATH",["A,C,D","A,C","B,C,D"])]:
    for i, a in enumerate(answers): add(2023,1,s,"M",i+1,a)
for s, answers in [("PHY",["A","C","B","D"]),("CHEM",["D","D","B","D"]),("MATH",["A","A","B","B"])]:
    for i, a in enumerate(answers): add(2023,1,s,"P",i+1,a)

# === 2022 P1 (partial — MCQ sections) ===
for s, answers in [("PHY",["C","C","C"]),("CHEM",["A","D","A"]),("MATH",["B","A","B"])]:
    for i, a in enumerate(answers): add(2022,1,s,"P",i+1,a)
for s, answers in [("PHY",["B","A,B,C,D","B","A,B","A,B,C","A,B,D"]),
                   ("CHEM",["A,D","A,D","B,C,D","A,D","B,C,D","A,B,C"]),
                   ("MATH",["C,D","B,C","A,B,D","A,B,C","B,C,D","A,C"])]:
    for i, a in enumerate(answers): add(2022,1,s,"M",i+1,a)

# === 2020 P1 ===
for s, answers in [("PHY",["A","B","B","B","A","B"]),("CHEM",["B","B","A","C","D","C"]),("MATH",["D","C","A","A","B","C"])]:
    for i, a in enumerate(answers): add(2020,1,s,"S",i+1,a)
for s, answers in [("PHY",["B,C","B,C,D","A,B","B,C","A,C,D","A,B,C"]),
                   ("CHEM",["A,B,C","A,B,C","B,D","A,C","A,B,D","A,C"]),
                   ("MATH",["A,C","B,C,D","B,C","B,C","A,B","A,B,D"])]:
    for i, a in enumerate(answers): add(2020,1,s,"M",i+1,a)

# === 2019 P1 ===
for s, answers in [("PHY",["A","C","A","B"]),("CHEM",["A","C","C","B"]),("MATH",["A","C","B","A"])]:
    for i, a in enumerate(answers): add(2019,1,s,"S",i+1,a)
for s, answers in [("PHY",["A,B,C","B,C,D","A,B,C","A,B,C","A,C","B,C,D","A,B,C","B,C"]),
                   ("CHEM",["A,B","A,B,D","C,D","A,C,D","B,D","A,B,D","A,C,D","C,D"]),
                   ("MATH",["A,B,C","A,B,D","A,B","A,C,D","B,C","B,C,D","A,B","A,B,C"])]:
    for i, a in enumerate(answers): add(2019,1,s,"M",i+1,a)

# === 2018 P1 ===
for s, answers in [("PHY",["C","D","B","C"]),("CHEM",["C","A","A","B"]),("MATH",["A","D","A","C"])]:
    for i, a in enumerate(answers): add(2018,1,s,"P",i+1,a)
for s, answers in [("PHY",["B,C","A,C","A,C","B,D","A,B,D","B,C,D"]),
                   ("CHEM",["B,C","B,C","A,B,C","B","A,B,D","B,C"]),
                   ("MATH",["A,B,D","B,C,D","C,D","A,B,D","B,C","B,C"])]:
    for i, a in enumerate(answers): add(2018,1,s,"M",i+1,a)

# === 2017 P1 ===
for s, answers in [("PHY",["D","A","B","D","B","D"]),("CHEM",["C","A","C","A","C","D"]),("MATH",["B","C","D","B","B","C"])]:
    for i, a in enumerate(answers): add(2017,1,s,"P",i+1,a)
for s, answers in [("PHY",["A,B,D","B,C","A,D","C","B,D","B,C","A,C,D"]),
                   ("CHEM",["A,B,C","B,D","A,B,D","C,D","B,C,D","A,B","B,D"]),
                   ("MATH",["A,B,C","C","A,B","B,D","A,B","A,B",""])]:
    for i, a in enumerate(answers):
        if a: add(2017,1,s,"M",i+1,a)

# === 2017 P2 ===
for s, answers in [("PHY",["A","B","D","A","A","B","B"]),
                   ("CHEM",["A","C","A","C","C","C","C"]),
                   ("MATH",["C","B","A","D","C","D","A","D","B","D","B","A","B","B","D"])]:
    for i, a in enumerate(answers): add(2017,2,s,"S",i+1,a)
for s, answers in [("PHY",["A,B","A,D","A,D","B,C","A,C,D","B,D","A,D"]),
                   ("CHEM",[]),("MATH",[])]:
    for i, a in enumerate(answers): add(2017,2,s,"M",i+1,a)

# ============================================================
# DEEP ANALYSIS
# ============================================================
out = []
def p(s=""): out.append(s)

p("=" * 80)
p(" MILITARY-GRADE JEE ADVANCED TUKKA INTELLIGENCE REPORT")
p(" Classification: TOP SECRET // FOR YOUR EYES ONLY")
p("=" * 80)

# Filter to only MCQ items
singles = [e for e in ALL if e['is_single']]
multis = [e for e in ALL if e['is_multi']]

# ── 1. RECENT YEAR WEIGHTED ANALYSIS (2023-2025 = 2x weight) ──
p("\n" + "█" * 70)
p(" 1. RECENT-YEAR-WEIGHTED SINGLE MCQ ANALYSIS (2023-2025 = 2x)")
p("█" * 70)

weighted_singles = []
for e in singles:
    weight = 2 if e['year'] >= 2023 else 1
    for _ in range(weight):
        weighted_singles.append(e['letters'][0])

wc = Counter(weighted_singles)
wt = len(weighted_singles)
p(f"\n  Weighted total: {wt}")
for o in 'ABCD':
    c = wc.get(o,0)
    pct = c/wt*100
    bar = '█' * int(pct/2)
    p(f"  {o}: {c:4d} ({pct:5.1f}%)  {bar}")

# ── 2. SECTION-TYPE SPECIFIC PATTERNS ──
p("\n" + "█" * 70)
p(" 2. SECTION-TYPE PATTERNS")
p("█" * 70)

for sec_name, sec_code in [("Section 1: Single MCQ","S"), ("Section 4: Paragraph Single","P")]:
    items = [e for e in singles if e['sec']==sec_code]
    if not items: continue
    ct = Counter(e['letters'][0] for e in items)
    t = len(items)
    p(f"\n  {sec_name} (n={t}):")
    for o in 'ABCD':
        c = ct.get(o,0); pct = c/t*100
        p(f"    {o}: {c:3d} ({pct:5.1f}%)")

# ── 3. POSITION-IN-SECTION ANALYSIS ──
p("\n" + "█" * 70)
p(" 3. POSITION-IN-SECTION ANALYSIS (which Q# in section is which letter?)")
p("█" * 70)

for sec_code, sec_name in [("S","Single MCQ"),("P","Paragraph")]:
    items = [e for e in singles if e['sec']==sec_code]
    if not items: continue
    p(f"\n  {sec_name}:")
    by_pos = defaultdict(list)
    for e in items:
        by_pos[e['pos']].append(e['letters'][0])
    for pos in sorted(by_pos.keys()):
        if pos > 6: break
        answers = by_pos[pos]
        ct = Counter(answers)
        t = len(answers)
        best = ct.most_common(1)[0]
        dist = " ".join(f"{o}={ct.get(o,0)}" for o in 'ABCD')
        p(f"    Q{pos} in section: {dist}  → BEST: ({best[0]}) {best[1]}/{t}={best[1]/t*100:.0f}%")

# ── 4. MULTI-CORRECT POSITION ANALYSIS ──
p("\n" + "█" * 70)
p(" 4. MULTI-CORRECT: POSITION & SUBJECT DEEP DIVE")
p("█" * 70)

for subj in ['PHY','CHEM','MATH']:
    items = [e for e in multis if e['subj']==subj]
    if not items: continue
    t = len(items)
    
    # Count distribution
    cd = Counter(len(e['letters']) for e in items)
    # Letter frequency
    lf = Counter()
    for e in items:
        for l in e['letters']: lf[l] += 1
    # Combo frequency
    cf = Counter(tuple(sorted(e['letters'])) for e in items)
    
    p(f"\n  {subj} Multi-Correct (n={t}):")
    p(f"    # correct: 2={cd.get(2,0)}({cd.get(2,0)/t*100:.0f}%) 3={cd.get(3,0)}({cd.get(3,0)/t*100:.0f}%) 4={cd.get(4,0)}({cd.get(4,0)/t*100:.0f}%)")
    p(f"    Letter freq: " + " ".join(f"{o}={lf.get(o,0)}({lf.get(o,0)/t*100:.0f}%)" for o in 'ABCD'))
    p(f"    Top combos: " + ", ".join(f"({','.join(c)})={n}" for c,n in cf.most_common(5)))

# ── 5. FIRST-QUESTION-OF-EACH-SUBJECT BIAS ──
p("\n" + "█" * 70)
p(" 5. FIRST QUESTION OF EACH SECTION/SUBJECT BIAS")
p("█" * 70)

first_q = [e for e in singles if e['pos'] == 1]
if first_q:
    ct = Counter(e['letters'][0] for e in first_q)
    t = len(first_q)
    p(f"\n  First question of section (n={t}):")
    for o in 'ABCD':
        c = ct.get(o,0)
        p(f"    {o}: {c} ({c/t*100:.1f}%)")

# ── 6. LAST QUESTION BIAS ──
last_q = [e for e in singles if e['pos'] >= 4]
if last_q:
    ct = Counter(e['letters'][0] for e in last_q)
    t = len(last_q)
    p(f"\n  Last questions of section (pos>=4, n={t}):")
    for o in 'ABCD':
        c = ct.get(o,0)
        p(f"    {o}: {c} ({c/t*100:.1f}%)")

# ── 7. PAPER 1 vs PAPER 2 DEEP ──
p("\n" + "█" * 70)
p(" 7. PAPER 1 vs PAPER 2 — MULTI-CORRECT DIFFERENCES")
p("█" * 70)

for pn in [1,2]:
    items = [e for e in multis if e['paper']==pn]
    if not items: continue
    t = len(items)
    cd = Counter(len(e['letters']) for e in items)
    lf = Counter()
    for e in items:
        for l in e['letters']: lf[l] += 1
    p(f"\n  Paper {pn} Multi (n={t}):")
    p(f"    2-opt={cd.get(2,0)}({cd.get(2,0)/t*100:.0f}%) 3-opt={cd.get(3,0)}({cd.get(3,0)/t*100:.0f}%) 4-opt={cd.get(4,0)}({cd.get(4,0)/t*100:.0f}%)")
    p(f"    Letters: " + " ".join(f"{o}={lf.get(o,0)/t*100:.0f}%" for o in 'ABCD'))

# ── 8. CROSS-SUBJECT: If PHY=A, what's CHEM? ──
p("\n" + "█" * 70)
p(" 8. CROSS-SUBJECT CORRELATION (Same Q position)")
p("█" * 70)

# Group by (year, paper, sec, pos) → see if subjects correlate
from itertools import combinations
groups = defaultdict(dict)
for e in singles:
    key = (e['year'], e['paper'], e['sec'], e['pos'])
    groups[key][e['subj']] = e['letters'][0]

same_count = 0
diff_count = 0
for key, subj_answers in groups.items():
    subjects = list(subj_answers.keys())
    for s1, s2 in combinations(subjects, 2):
        if subj_answers[s1] == subj_answers[s2]:
            same_count += 1
        else:
            diff_count += 1

total_cross = same_count + diff_count
if total_cross:
    p(f"\n  Cross-subject same-position pairs: {total_cross}")
    p(f"  Same answer: {same_count} ({same_count/total_cross*100:.1f}%) — expected 25%")
    p(f"  Different:   {diff_count} ({diff_count/total_cross*100:.1f}%)")

# ── 9. 2024+2025 ONLY (most predictive for 2026) ──
p("\n" + "█" * 70)
p(" 9. 2024-2025 PATTERNS ONLY (most predictive for 2026)")
p("█" * 70)

recent_singles = [e for e in singles if e['year'] >= 2024]
if recent_singles:
    ct = Counter(e['letters'][0] for e in recent_singles)
    t = len(recent_singles)
    p(f"\n  Recent single MCQs (n={t}):")
    for o in 'ABCD':
        c = ct.get(o,0)
        p(f"    {o}: {c} ({c/t*100:.1f}%)")
    
    # By subject
    for subj in ['PHY','CHEM','MATH']:
        items = [e for e in recent_singles if e['subj']==subj]
        if not items: continue
        ct2 = Counter(e['letters'][0] for e in items)
        t2 = len(items)
        best = ct2.most_common(1)[0]
        p(f"    {subj}: best=({best[0]}) {best[1]}/{t2}={best[1]/t2*100:.0f}%")

recent_multis = [e for e in multis if e['year'] >= 2024]
if recent_multis:
    t = len(recent_multis)
    cd = Counter(len(e['letters']) for e in recent_multis)
    lf = Counter()
    for e in recent_multis:
        for l in e['letters']: lf[l] += 1
    cf = Counter(tuple(sorted(e['letters'])) for e in recent_multis)
    p(f"\n  Recent multi MCQs (n={t}):")
    p(f"    2-opt={cd.get(2,0)}({cd.get(2,0)/t*100:.0f}%) 3-opt={cd.get(3,0)}({cd.get(3,0)/t*100:.0f}%)")
    p(f"    Letters: " + " ".join(f"{o}={lf.get(o,0)/t*100:.0f}%" for o in 'ABCD'))
    p(f"    Top combos: " + ", ".join(f"({','.join(c)})={n}" for c,n in cf.most_common(5)))

# Write
outpath = r"d:\Jee Advanced Tukka Research\DEEP_ANALYSIS.txt"
with open(outpath, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Deep analysis written to {outpath}")
