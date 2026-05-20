import random
from master_analysis import DATA
from scramble_proof import NUMERICALS
from collections import Counter

# ENHANCED NUMERICAL ANALYSIS
print("--- ENHANCED NUMERICAL ANALYSIS ---")
all_nums = []
for key, vals in NUMERICALS.items():
    for v in vals:
        subj = key.split('_')[2]
        all_nums.append({'subj': subj, 'val': v})

for subj in ['PHY', 'CHEM', 'MATH']:
    vals = [e['val'] for e in all_nums if e['subj'] == subj]
    ints = [int(v) for v in vals if v == int(v) and 0 <= v <= 9]
    c = Counter(ints)
    total = len(vals)
    print(f"{subj}: Total answers={total}, Single-digit integers={len(ints)}")
    for d, count in c.most_common(3):
        print(f"  Digit {d}: {count} times ({count/total*100:.1f}%)")

print("\n--- MONTE CARLO SIMULATION (Target: 37 agg, 3 per subj) ---")
# Strategy A: Pure random guessing on everything
# Strategy B: Optimized (Longest option for single MCQ (+0.33 EV), skip multi-correct, best digit for numerical)
# Strategy C: Conservative (only guess numericals, skip all MCQs)

def sim(strategy, trials=10000):
    success = 0
    total_scores = []
    
    # 51 questions per paper: 17 per subject
    # Assuming: 4 single MCQ, 3 para MCQ (treat as single), 4 multi, 6 numerical per subject per paper
    # So per subject total: 14 single MCQs, 8 multi, 12 numericals (across both papers)
    
    for _ in range(trials):
        subj_scores = [0, 0, 0] # PHY, CHEM, MATH
        
        for subj_idx in range(3):
            score = 0
            
            # Single MCQs (14 per subject)
            for _ in range(14):
                if strategy == 'A':
                    # Pure random: 1/4 chance to get +3, 3/4 to get -1
                    if random.random() < 0.25: score += 3
                    else: score -= 1
                elif strategy == 'B':
                    # Optimized: Longest option (say 31% hit rate)
                    if random.random() < 0.31: score += 3
                    else: score -= 1
                elif strategy == 'C':
                    # Skip
                    pass
            
            # Multi-correct (8 per subject)
            for _ in range(8):
                if strategy == 'A':
                    # Guess 2 options randomly (usually negative EV, let's say roughly 1/6 chance +4, 5/6 chance -2)
                    # For simplicity, let's approximate pure random on multi: EV is negative.
                    # P(correct 2 options out of 4) = 1/6. If we guess exactly those 2: +4. Otherwise -2.
                    if random.random() < (1/6): score += 4
                    else: score -= 2
                elif strategy == 'B':
                    # Skip multi-correct
                    pass
                elif strategy == 'C':
                    # Skip
                    pass
            
            # Numerical (12 per subject)
            for _ in range(12):
                if strategy == 'A':
                    # Random digit 0-9: ~10% hit rate
                    if random.random() < 0.10: score += 3
                elif strategy == 'B':
                    # Best digit relative to ALL answers: 
                    # PHY: 8 (~7.0%)
                    # CHEM: 3 (~8.9%)
                    # MATH: 1 (~10.5%)
                    hit_rate = [0.070, 0.089, 0.105][subj_idx]
                    if random.random() < hit_rate: score += 3
                elif strategy == 'C':
                    hit_rate = [0.070, 0.089, 0.105][subj_idx]
                    if random.random() < hit_rate: score += 3
            
            subj_scores[subj_idx] = score
            
        total_score = sum(subj_scores)
        total_scores.append(total_score)
        
        if total_score >= 37 and all(s >= 3 for s in subj_scores):
            success += 1
            
    mean_score = sum(total_scores) / trials
    return success / trials * 100, mean_score

for strat in ['A', 'B', 'C']:
    prob, mean_s = sim(strat)
    names = {'A': 'Pure Random', 'B': 'Optimized (Longest Opt, Skip Multi, Best Num)', 'C': 'Conservative (Only Num)'}
    print(f"Strategy {names[strat]}:")
    print(f"  Mean Score: {mean_s:.2f}")
    print(f"  Prob of qualifying (37 agg, 3/subj): {prob:.2f}%\n")
