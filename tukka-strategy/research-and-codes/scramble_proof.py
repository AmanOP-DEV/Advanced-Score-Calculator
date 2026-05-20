"""
POST-SCRAMBLE ANALYSIS: What patterns survive option randomization?

In JEE Advanced CBT, options A/B/C/D are shuffled per candidate.
So letter-based patterns are USELESS.

What IS still valid:
1. Numerical answer values (content, not labels)
2. Multi-correct: HOW MANY options are correct
3. Multi-correct: typical combos (adjacent pairs, etc)
4. Content-based patterns (answer magnitudes, signs, etc)
5. Marking scheme EV math
6. Question difficulty by position
"""
from collections import Counter, defaultdict
import re

# ============================================================
# NUMERICAL ANSWER DEEP DIVE (THIS IS THE GOLD MINE)
# These are actual VALUES — unaffected by option scrambling
# ============================================================

# Complete numerical answers from all years
NUMERICALS = {
    # 2017 P1
    "2017_P1_PHY": [6, 5, 8, 6, 5],
    "2017_P1_CHEM": [2, 6, 6, 5],
    "2017_P1_MATH": [2, 2, 1, 5, 6],
    
    # 2018 P1
    "2018_P1_PHY": [2, 8, 0.75, 2.09, 1.5, 1.2, 130, 4],
    "2018_P1_CHEM": [1, 2992, 3, 10, 2.22, 19, 4.47, 0.05],
    "2018_P1_MATH": [8, 625, 3748, 2, 1, 3, 0.5, 4],
    
    # 2019 P1 (Q13-18 numerical per subject, data incomplete — use search data)
    
    # 2020 P1
    "2020_P1_PHY": [25.6, 3.75, 1.5, 1.78, 0.63, 6.4],
    "2020_P1_CHEM": [0.11, 0.25, 13.3, 6.1, 1.2, 18],
    "2020_P1_MATH": [8, 1, 1, 108, 5, 1],
    
    # 2022 P1
    "2022_P1_PHY": [2.3, 2.32, 8, 6, 0.52, 2.85, 4, 0.95],
    "2022_P1_CHEM": [90.39, 0.77, 10.02, 0.32, 2.38, 1.5, 1.31, 136],
    "2022_P1_MATH": [2.35, 0.5, 0.8, 0.5, 4, 18900, 569, 0.83],
    
    # 2024 P1
    "2024_P1_PHY": [25000, 12, 8, 200, 3, 18],
    "2024_P1_CHEM": [8120, 3, 18, 1, 909, 1],
    "2024_P1_MATH": [8, 20, 16, 665, 5, 42],
    
    # 2024 P2
    "2024_P2_PHY": [3, 2, 3, 12, 171, 96, 600, 24, 0.75, 4.25],
    "2024_P2_CHEM": [2500, 150, 41, 143, 3, 12, 2, 93018, 3, 3],
    "2024_P2_MATH": [51, 11, 1, 2, 12, 5, 20, 36, 0, 0.25],
    
    # 2025 P1
    "2025_P1_PHY": [2, 23, 3, 0.625, 77, 72],  # midpoints of ranges
    "2025_P1_CHEM": [100, 2.25, -7.1, 29.88, 280, 175],
    "2025_P1_MATH": [105, 1.2, 762, 2.4, 96, 2],
    
    # 2025 P2
    "2025_P2_PHY": [1.66, 11.8, 1.6, 2.35, 0.2, 1.2, 169, 30],
    "2025_P2_CHEM": [11, 4, 16, 4.1, 105.5, 2.47, 7.65, 2],
    "2025_P2_MATH": [0.75, 6, 0.3, -2, -2, 0.25, 3, 21],
}

out = []
def p(s=""): out.append(s)

p("=" * 80)
p(" POST-SCRAMBLE INTELLIGENCE REPORT")
p(" What actually works when options are randomized")
p("=" * 80)

# ── 1. NUMERICAL VALUE DISTRIBUTION ──
p("\n" + "█" * 70)
p(" 1. NUMERICAL ANSWER VALUE ANALYSIS")
p("█" * 70)

all_nums = []
for key, vals in NUMERICALS.items():
    for v in vals:
        all_nums.append({'key': key, 'val': v, 'abs_val': abs(v)})

p(f"\n  Total numerical answers analyzed: {len(all_nums)}")

# Integer analysis (answers that ARE integers)
integers = [e for e in all_nums if e['val'] == int(e['val'])]
p(f"  Of those, exact integers: {len(integers)} ({len(integers)/len(all_nums)*100:.0f}%)")

# Value range distribution
p(f"\n  VALUE RANGE DISTRIBUTION:")
ranges = [(0, 0, "Exactly 0"), (1, 1, "Exactly 1"), (2, 2, "Exactly 2"), 
          (3, 3, "Exactly 3"), (4, 5, "4-5"), (6, 10, "6-10"), 
          (11, 50, "11-50"), (51, 200, "51-200"), (201, 1000, "201-1000"), (1001, 100000, "1000+")]
for lo, hi, label in ranges:
    count = len([e for e in all_nums if lo <= e['abs_val'] <= hi])
    pct = count/len(all_nums)*100
    bar = '█' * int(pct)
    p(f"    {label:>12s}: {count:3d} ({pct:5.1f}%)  {bar}")

# Single digit integers (0-9)
single_digits = [int(e['val']) for e in all_nums if 0 <= e['val'] <= 9 and e['val'] == int(e['val'])]
p(f"\n  SINGLE DIGIT INTEGERS (0-9): {len(single_digits)}")
dc = Counter(single_digits)
for d in range(10):
    c = dc.get(d, 0)
    pct = c/len(single_digits)*100 if single_digits else 0
    bar = '█' * int(pct)
    p(f"    {d}: {c:3d} ({pct:5.1f}%)  {bar}")

# Small integers (1-20)
small_ints = [int(e['val']) for e in all_nums if 1 <= e['val'] <= 20 and e['val'] == int(e['val'])]
p(f"\n  SMALL INTEGERS (1-20): {len(small_ints)}")
si_c = Counter(small_ints)
for d in range(1, 21):
    c = si_c.get(d, 0)
    if c > 0:
        bar = '█' * (c * 2)
        p(f"    {d:3d}: {c:3d}  {bar}")

# Negative numbers
negatives = [e for e in all_nums if e['val'] < 0]
p(f"\n  NEGATIVE ANSWERS: {len(negatives)} ({len(negatives)/len(all_nums)*100:.1f}%)")
for n in negatives:
    p(f"    {n['key']}: {n['val']}")

# Decimals
decimals = [e for e in all_nums if e['val'] != int(e['val'])]
p(f"\n  DECIMAL (non-integer) ANSWERS: {len(decimals)} ({len(decimals)/len(all_nums)*100:.1f}%)")

# Subject breakdown
p(f"\n  SUBJECT-WISE MEDIAN VALUES:")
for subj in ['PHY', 'CHEM', 'MATH']:
    vals = [e['val'] for e in all_nums if subj in e['key']]
    if vals:
        vals_sorted = sorted(vals)
        median = vals_sorted[len(vals_sorted)//2]
        mean = sum(vals)/len(vals)
        p(f"    {subj}: median={median:.1f}, mean={mean:.1f}, range=[{min(vals):.1f}, {max(vals):.1f}]")

# ── 2. MULTI-CORRECT: # OF CORRECT OPTIONS ──
p("\n" + "█" * 70)
p(" 2. MULTI-CORRECT: HOW MANY OPTIONS ARE CORRECT?")
p("   (This survives scrambling — it's about the QUESTION, not the labels)")
p("█" * 70)

# Re-import from master data
multi_counts = {
    "overall": {2: 81, 3: 61, 4: 2},
    "paper1": {2: 59, 3: 56, 4: 2},
    "paper2": {2: 22, 3: 5, 4: 0},
    "PHY": {2: 26, 3: 23, 4: 2},
    "CHEM": {2: 28, 3: 18, 4: 0},
    "MATH": {2: 27, 3: 20, 4: 0},
}

for label, dist in multi_counts.items():
    total = sum(dist.values())
    pcts = {k: v/total*100 for k, v in dist.items()}
    p(f"\n  {label} (n={total}):")
    for n in [2, 3, 4]:
        bar = '█' * int(pcts.get(n, 0)/2)
        p(f"    {n} correct: {dist.get(n,0):3d} ({pcts.get(n,0):5.1f}%)  {bar}")

# ── 3. EV CALCULATIONS (always valid) ──
p("\n" + "█" * 70)
p(" 3. EXPECTED VALUE (EV) CALCULATIONS FOR EVERY SCENARIO")
p("█" * 70)

p(f"""
  SINGLE MCQ (+3 correct, -1 wrong, 0 skip):
  ───────────────────────────────────────────
    Random guess (4 options):  EV = 3*(1/4) + (-1)*(3/4) = 0.00
    After eliminating 1:       EV = 3*(1/3) + (-1)*(2/3) = +0.33 ← GUESS!
    After eliminating 2:       EV = 3*(1/2) + (-1)*(1/2) = +1.00 ← ALWAYS GUESS!
    Skip:                      EV = 0.00

  MULTI-CORRECT (+4 all correct, partial +1 each, -2 any wrong):
  ──────────────────────────────────────────────────────────────
    If 2 are correct (56% likely):
      Marking 1 random option:     EV = (2/4)*1 + (2/4)*(-2) = -0.50 ← BAD
      Marking 2 random options:    EV = complex, roughly -0.33 ← BAD  
      SKIP if no clue:             EV = 0.00 ← BEST when clueless
      
    If you KNOW 1 correct option:
      Mark only that 1:            EV = +1.00 ← GOOD! Guaranteed partial
      Mark that 1 + guess 1 more:  EV = +1 + (1/3)*1 + (2/3)*(-2) = +0.33 ← OK

  NUMERICAL (+3 correct, 0 wrong/skip):
  ─────────────────────────────────────
    Guessing integer 0-9 (if ans is single digit):
      Best guess "6" or "2":   EV ≈ 3 * 0.208 = +0.625 per question
      Random digit:            EV = 3 * 0.1 = +0.30 per question
      SKIP:                    EV = 0.00 ← NEVER DO THIS
      
    EVEN FOR NON-INTEGER: entering 3 has a ~5% chance of being right
      EV = 3 * 0.05 = +0.15 ← still better than skipping!
""")

# ── 4. WHAT OPTION-SCRAMBLE-PROOF STRATEGIES ACTUALLY WORK ──
p("\n" + "█" * 70)
p(" 4. SCRAMBLE-PROOF STRATEGIES THAT ACTUALLY WORK")
p("█" * 70)

p("""
  A. READ THE OPTIONS — even if you can't solve the problem:
  ──────────────────────────────────────────────────────────
     1. "Always/Never/Only/All" statements → usually WRONG (eliminate)
     2. Longest/most-detailed option → often CORRECT
     3. If 2 options are opposites of each other → one of them is correct
     4. If 3 options look similar + 1 outlier → outlier is usually WRONG
     5. In numerical options: extreme values (highest/lowest) → usually WRONG
     6. If option says "zero" or "infinity" → almost always WRONG
     
  B. USE DIMENSIONAL ANALYSIS even if you can't solve:
  ────────────────────────────────────────────────────
     Physics: check if the units make sense (force = kg*m/s²)
     Chemistry: check moles, concentrations, pressure units
     Maths: check if the answer should be positive/negative, integer/fraction
     
  C. BOUNDARY/EXTREME CASE testing:
  ─────────────────────────────────
     Plug in x=0, x=1, x=∞ into options to eliminate impossible ones
     Even without solving, this can kill 1-2 options
     
  D. MULTI-CORRECT SAFE PLAY:
  ───────────────────────────
     If you're SURE of 1 option → mark ONLY that one → +1 guaranteed
     NEVER randomly mark multiple options → -2 risk dominates
     
  E. NUMERICAL: ALWAYS FILL IN SOMETHING
  ───────────────────────────────────────
     Integer range 0-9: try 2, 5, or 6
     Larger range: try 3, 5, or 12
     Decimal: try 0.5, 1.5, or 2.5
     NEVER leave blank — there is NO penalty
""")

outpath = r"d:\Jee Advanced Tukka Research\SCRAMBLE_PROOF_ANALYSIS.txt"
with open(outpath, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Analysis written to {outpath}")
