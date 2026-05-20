"""
COMPREHENSIVE MONTE CARLO SIMULATION + FINAL ANALYSIS
Simulates 100,000 exam attempts with different strategies
Against REAL SC category cutoffs
"""
import random
from collections import Counter, defaultdict
import math

random.seed(42)

# ============================================================
# SC CATEGORY CUTOFF HISTORY (REAL DATA)
# ============================================================
# Format: (min_pct_per_subject, min_pct_aggregate, total_marks_in_that_year)
SC_CUTOFFS = {
    2019: (5.00, 17.50, 372),  # 18.6 per subject, 65.1 aggregate  
    2020: (2.50, 8.75, 396),   # 9.9 per subject, 34.65 aggregate
    2021: (2.50, 8.75, 360),   # 9.0 per subject, 31.5 aggregate
    2022: (2.20, 7.78, 360),   # 7.92 per subject, 28 aggregate
    2023: (3.42, 11.95, 360),  # 12.3 per subject, 43 aggregate
    2024: (5.00, 15.00, 360),  # 18.0 per subject, 54 aggregate (from NEXT_PROMPT)
    2025: (5.00, 17.50, 360),  # 18.0 per subject, 63 aggregate
}

out = []
def p(s=""): out.append(s)

p("=" * 80)
p(" COMPREHENSIVE JEE ADVANCED TUKKA SIMULATION")
p(" 100,000 Monte Carlo trials per strategy")
p("=" * 80)

# ============================================================
# EXAM STRUCTURE FOR 2026 (typical pattern)
# ============================================================
# Per subject per paper:
#   Section 1: 4 single-correct MCQs (+3/-1)
#   Section 2: 4 multi-correct MCQs (+4 all, +1 partial each, -2 wrong)
#   Section 3: 6 numerical (+3/0)
#   Section 4: 3 paragraph single MCQs (+3/-1)
# = 17 questions per subject per paper
# = 51 questions per paper
# = 102 questions total

# Per subject per paper:
STRUCTURE = {
    "single": {"count": 4, "correct": 3, "wrong": -1, "options": 4},
    "para_single": {"count": 3, "correct": 3, "wrong": -1, "options": 4},
    "multi": {"count": 4, "correct_all": 4, "correct_partial": 1, "wrong": -2, "options": 4},
    "numerical": {"count": 6, "correct": 3, "wrong": 0},
}

# Maximum marks per subject per paper:
# 4*3 + 3*3 + 4*4 + 6*3 = 12+9+16+18 = 55 per subject per paper
# But for simulation we use the structure above

# ============================================================
# KNOWN DISTRIBUTIONS (from our data)
# ============================================================
# Multi-correct: how many are actually correct
MULTI_CORRECT_DIST = {2: 0.562, 3: 0.424, 4: 0.014}

# Numerical: probability of guessing right with our strategy
# If answer is single-digit integer (34% of numericals):
#   Guessing "3" hits 19% of the time → P = 0.34 * 0.19 = 0.065
# If answer is non-single-digit:
#   Near zero chance of guessing right
# Combined: ~6.5% chance of getting a numerical right by guessing "3"
NUM_GUESS_RIGHT_PROB = 0.065

# Single MCQ: with elimination tricks
# Baseline: 25% (random)
# With "pick longer option": ~31% 
# With 1 elimination (30% of Qs): ~33%
SINGLE_GUESS_RIGHT_PROB_RANDOM = 0.25
SINGLE_GUESS_RIGHT_PROB_SMART = 0.31  # longest option bias
SINGLE_GUESS_RIGHT_PROB_ELIM1 = 0.333  # eliminated 1 option

def simulate_paper(strategy, num_trials=100000):
    """Simulate a single paper (51 questions, 3 subjects)"""
    results = []
    subject_results = []
    
    for _ in range(num_trials):
        total_marks = 0
        subj_marks = {"PHY": 0, "CHEM": 0, "MATH": 0}
        
        for subj in ["PHY", "CHEM", "MATH"]:
            subj_total = 0
            
            # --- SINGLE MCQs (4 questions) ---
            for q in range(4):
                if strategy == "skip_all":
                    pass  # 0 marks
                elif strategy == "random":
                    if random.random() < 0.25:
                        subj_total += 3
                    else:
                        subj_total -= 1
                elif strategy == "smart":
                    # 20% of the time can eliminate 1 option
                    if random.random() < 0.20:
                        p_right = 1/3
                    else:
                        p_right = SINGLE_GUESS_RIGHT_PROB_SMART
                    if random.random() < p_right:
                        subj_total += 3
                    else:
                        subj_total -= 1
                elif strategy == "conservative":
                    pass  # skip MCQs
                    
            # --- PARAGRAPH SINGLE MCQs (3 questions) ---
            for q in range(3):
                if strategy == "skip_all":
                    pass
                elif strategy == "random":
                    if random.random() < 0.25:
                        subj_total += 3
                    else:
                        subj_total -= 1
                elif strategy == "smart":
                    if random.random() < 0.20:
                        p_right = 1/3
                    else:
                        p_right = SINGLE_GUESS_RIGHT_PROB_SMART
                    if random.random() < p_right:
                        subj_total += 3
                    else:
                        subj_total -= 1
                elif strategy == "conservative":
                    pass
                    
            # --- MULTI-CORRECT (4 questions) ---
            for q in range(4):
                # Determine actual number of correct options
                r = random.random()
                if r < 0.562:
                    actual_correct = 2
                elif r < 0.562 + 0.424:
                    actual_correct = 3
                else:
                    actual_correct = 4
                
                if strategy == "skip_all":
                    pass
                elif strategy == "random":
                    # Randomly mark 2 options (most common strategy)
                    marked = random.sample([0,1,2,3], 2)
                    correct_set = set(range(actual_correct))
                    marked_set = set(marked)
                    
                    correct_marked = len(marked_set & correct_set)
                    wrong_marked = len(marked_set - correct_set)
                    
                    if wrong_marked > 0:
                        subj_total -= 2
                    elif correct_marked == actual_correct:
                        subj_total += 4
                    else:
                        subj_total += correct_marked  # partial
                elif strategy == "smart":
                    # Mark only 1 option (safest)
                    # Probability that our 1 pick is correct:
                    p_one_correct = actual_correct / 4
                    if random.random() < p_one_correct:
                        subj_total += 1  # partial credit
                    else:
                        subj_total -= 2
                elif strategy == "conservative":
                    pass  # skip
                    
            # --- NUMERICAL (6 questions) ---
            for q in range(6):
                if strategy == "skip_all":
                    pass
                elif strategy in ["random", "smart", "conservative"]:
                    # Always guess — zero penalty!
                    if random.random() < NUM_GUESS_RIGHT_PROB:
                        subj_total += 3
                    # else: 0 marks (no penalty)
                    
            subj_marks[subj] = subj_total
            total_marks += subj_total
        
        results.append(total_marks)
        subject_results.append(subj_marks)
    
    return results, subject_results

def analyze_results(results, subject_results, strategy_name):
    """Analyze simulation results against real SC cutoffs"""
    p(f"\n{'█' * 70}")
    p(f" STRATEGY: {strategy_name}")
    p(f"{'█' * 70}")
    
    # Both papers combined (multiply by 2)
    combined = [r * 2 for r in results]
    
    avg = sum(combined) / len(combined)
    median = sorted(combined)[len(combined)//2]
    std = math.sqrt(sum((x-avg)**2 for x in combined) / len(combined))
    min_score = min(combined)
    max_score = max(combined)
    
    p(f"\n  Score distribution (both papers combined, out of 360):")
    p(f"    Mean:   {avg:.1f}")
    p(f"    Median: {median:.1f}")
    p(f"    StdDev: {std:.1f}")
    p(f"    Range:  [{min_score}, {max_score}]")
    
    # Percentiles
    sorted_c = sorted(combined)
    for pctl in [5, 10, 25, 50, 75, 90, 95]:
        idx = int(len(sorted_c) * pctl / 100)
        p(f"    P{pctl:2d}:    {sorted_c[idx]}")
    
    # Score buckets
    p(f"\n  Score distribution:")
    buckets = [(-100,0), (1,10), (11,20), (21,30), (31,40), (41,50), (51,60), (61,80), (81,100), (101,150)]
    for lo, hi in buckets:
        count = sum(1 for x in combined if lo <= x <= hi)
        pct = count/len(combined)*100
        bar = '█' * int(pct/2)
        p(f"    {lo:4d} to {hi:4d}: {pct:5.1f}%  {bar}")
    
    # Probability of qualifying (per year's cutoff)
    p(f"\n  Probability of qualifying (SC category):")
    for year in sorted(SC_CUTOFFS.keys()):
        min_subj_pct, min_agg_pct, total = SC_CUTOFFS[year]
        # Scale to our simulation's total (need both papers)
        # Per subject marks in one paper = subj_marks, total per subject = 2 * subj_marks
        # Max per subject per paper ≈ 55
        # Min per subject aggregate = min_subj_pct/100 * total/3
        min_subj_marks = min_subj_pct / 100 * total / 3
        min_agg_marks = min_agg_pct / 100 * total
        
        qualified = 0
        for i in range(len(results)):
            sm = subject_results[i]
            # Simulate paper 2 as same distribution
            sm2 = {s: results[random.randint(0,len(results)-1)] // 3 for s in ['PHY','CHEM','MATH']}
            
            # Use paper 1 subject marks * 2 as approximation
            total_both = combined[i]
            phy_both = sm['PHY'] * 2
            chem_both = sm['CHEM'] * 2
            math_both = sm['MATH'] * 2
            
            if (total_both >= min_agg_marks and 
                phy_both >= min_subj_marks and 
                chem_both >= min_subj_marks and 
                math_both >= min_subj_marks):
                qualified += 1
        
        prob = qualified / len(results) * 100
        p(f"    {year} cutoff ({min_agg_marks:.0f} agg, {min_subj_marks:.1f}/subj): {prob:.1f}%")

# ============================================================
# RUN SIMULATIONS
# ============================================================

p("\n  Exam structure assumed per paper:")
p("    Single MCQ: 4/subj × 3 subj = 12 (±3/−1)")
p("    Paragraph:  3/subj × 3 subj = 9  (±3/−1)")
p("    Multi:      4/subj × 3 subj = 12 (±4/+1/−2)")
p("    Numerical:  6/subj × 3 subj = 18 (±3/0)")
p("    Total: 51 questions per paper")
p(f"\n  Running 100,000 simulations per strategy...")

for strategy, name in [
    ("skip_all", "SKIP EVERYTHING (baseline)"),
    ("conservative", "CONSERVATIVE (only guess numericals, skip all MCQs)"),
    ("random", "RANDOM (guess everything randomly)"),
    ("smart", "SMART (longest option for single, mark-1 for multi, guess '3' for numerical)"),
]:
    results, subj_results = simulate_paper(strategy)
    analyze_results(results, subj_results, name)

# ============================================================
# SUBJECT-WISE NUMERICAL ANALYSIS
# ============================================================
p("\n" + "█" * 70)
p(" SUBJECT-WISE NUMERICAL OPTIMAL GUESS")
p("█" * 70)

# From scramble_proof.py data
NUMERICALS_BY_SUBJ = {
    "PHY": [6,5,8,6,5, 2,8,0.75,2.09,1.5,1.2,130,4, 25.6,3.75,1.5,1.78,0.63,6.4,
            2.3,2.32,8,6,0.52,2.85,4,0.95, 25000,12,8,200,3,18,
            3,2,3,12,171,96,600,24,0.75,4.25, 2,23,3,0.625,77,72,
            1.66,11.8,1.6,2.35,0.2,1.2,169,30],
    "CHEM": [2,6,6,5, 1,2992,3,10,2.22,19,4.47,0.05, 0.11,0.25,13.3,6.1,1.2,18,
             90.39,0.77,10.02,0.32,2.38,1.5,1.31,136, 8120,3,18,1,909,1,
             2500,150,41,143,3,12,2,93018,3,3, 100,2.25,-7.1,29.88,280,175,
             11,4,16,4.1,105.5,2.47,7.65,2],
    "MATH": [2,2,1,5,6, 8,625,3748,2,1,3,0.5,4, 8,1,1,108,5,1,
             2.35,0.5,0.8,0.5,4,18900,569,0.83, 8,20,16,665,5,42,
             51,11,1,2,12,5,20,36,0,0.25, 105,1.2,762,2.4,96,2,
             0.75,6,0.3,-2,-2,0.25,3,21],
}

for subj, vals in NUMERICALS_BY_SUBJ.items():
    p(f"\n  {subj} ({len(vals)} answers):")
    
    # Single digits
    single_d = [int(v) for v in vals if v == int(v) and 0 <= v <= 9]
    if single_d:
        dc = Counter(single_d)
        total_sd = len(single_d)
        best = dc.most_common(3)
        p(f"    Single-digit integers (n={total_sd}):")
        for d, c in sorted(dc.items()):
            p(f"      {d}: {c} ({c/total_sd*100:.0f}%)")
        p(f"    → BEST GUESS for {subj}: {best[0][0]} ({best[0][1]}/{total_sd}={best[0][1]/total_sd*100:.0f}%)")
    
    # All values - median and common ranges
    sorted_vals = sorted(vals)
    median_v = sorted_vals[len(sorted_vals)//2]
    ints = [int(v) for v in vals if v == int(v) and v > 0]
    int_counter = Counter(ints)
    p(f"    Median value: {median_v}")
    p(f"    Most common integers: {int_counter.most_common(5)}")

# ============================================================
# THE 3-MARKS-PER-SUBJECT GUARANTEE
# ============================================================
p("\n" + "█" * 70)
p(" THE 3-MARKS-PER-SUBJECT GUARANTEE ANALYSIS")
p("█" * 70)

p("""
  Per subject per paper you have:
    6 numerical questions × +3/0 = your SAFEST source of marks
    
  With 6 numericals and guessing "3" (P=6.5% each):
    Expected per paper per subject = 6 × 0.065 × 3 = 1.17 marks
    Over both papers per subject   = 2.34 marks
    
  Probability of getting AT LEAST 1 numerical right per subject (12 questions over 2 papers):
    P(≥1) = 1 - (1-0.065)^12 = 1 - 0.935^12 = 1 - 0.447 = 55.3%
    
  Probability of getting 0 numericals right in a subject:
    P(0) = 0.935^12 = 44.7%
    
  If you get 1 right = 3 marks. You need ≥3 per subject to qualify.
  
  PROBLEM: 44.7% chance of getting 0 in a subject purely from numericals.
  
  SOLUTION: You ALSO attempt single MCQs.
    - 7 single MCQs per subject per paper = 14 over both papers
    - Even at 25% random accuracy: 3.5 right × +3 = 10.5 marks
      BUT: 10.5 wrong × -1 = -10.5 marks → net ≈ 0
    - At 31% smart accuracy: 4.34 right = 13 marks, 9.66 wrong = -9.66 → net ≈ +3.4
    
  COMBINED (numerical + smart single MCQ):
    Per subject over both papers:
      Numerical contribution: 2.34 marks (expected)
      Single MCQ contribution: ~3.4 marks (expected with smart strategy)
      Total expected per subject: ~5.7 marks
      
  The per-subject minimum for most years is 3-18 marks.
  At 5.7 expected per subject, we exceed 3 marks in most scenarios.
""")

# Simulate the per-subject probability
trials = 100000
min3_count = 0
for _ in range(trials):
    all_pass = True
    for subj in range(3):
        subj_marks = 0
        # 2 papers × (6 numerical + 7 single MCQ)
        for paper in range(2):
            # Numericals
            for q in range(6):
                if random.random() < NUM_GUESS_RIGHT_PROB:
                    subj_marks += 3
            # Single MCQs (4 section1 + 3 paragraph = 7)
            for q in range(7):
                if random.random() < 0.31:
                    subj_marks += 3
                else:
                    subj_marks -= 1
        if subj_marks < 3:
            all_pass = False
            break
    if all_pass:
        min3_count += 1

p(f"  Simulation: P(all 3 subjects ≥ 3 marks) = {min3_count/trials*100:.1f}%")

# Also simulate for different per-subject thresholds
for thresh in [3, 5, 8, 10, 15, 18]:
    count = 0
    for _ in range(trials):
        all_pass = True
        for subj in range(3):
            sm = 0
            for paper in range(2):
                for q in range(6):
                    if random.random() < NUM_GUESS_RIGHT_PROB: sm += 3
                for q in range(7):
                    if random.random() < 0.31: sm += 3
                    else: sm -= 1
            if sm < thresh:
                all_pass = False
                break
        if all_pass:
            count += 1
    p(f"  P(all 3 subjects ≥ {thresh:2d} marks) = {count/trials*100:.1f}%")

outpath = r"d:\Jee Advanced Tukka Research\SIMULATION_RESULTS.txt"
with open(outpath, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Written to {outpath}")
