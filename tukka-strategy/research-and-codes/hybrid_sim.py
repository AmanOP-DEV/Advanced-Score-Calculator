"""
HYBRID STRATEGY SIMULATION
What if you can solve 5, 10, or 15 questions?
"""
import random
import math

random.seed(42)

SC_CUTOFFS = {
    2019: (5.00, 17.50, 372),
    2020: (2.50, 8.75, 396),
    2021: (2.50, 8.75, 360),
    2022: (2.20, 7.78, 360),
    2023: (3.42, 11.95, 360),
    2024: (5.00, 15.00, 360),
    2025: (5.00, 17.50, 360),
}

NUM_GUESS_RIGHT = 0.065
SMART_SINGLE_RIGHT = 0.31

out = []
def p(s=""): out.append(s)

p("=" * 80)
p(" HYBRID STRATEGY: What if you actually know SOME questions?")
p("=" * 80)

def simulate_hybrid(num_known_per_subj, trials=100000):
    """
    num_known_per_subj: how many questions per subject per paper you can ACTUALLY solve
    These are distributed across single MCQ, para MCQ, and numerical
    """
    results = []
    subj_results_all = []
    
    for _ in range(trials):
        subj_marks_dict = {}
        total = 0
        for subj_idx in range(3):
            sm = 0
            for paper in range(2):
                known_left = num_known_per_subj
                
                # 6 numerical questions (+3/0)
                for q in range(6):
                    if known_left > 0 and random.random() < 0.3:  # 30% chance you know a numerical
                        sm += 3
                        known_left -= 1
                    elif random.random() < NUM_GUESS_RIGHT:
                        sm += 3
                
                # 7 single MCQs (4 regular + 3 paragraph) (+3/-1)
                for q in range(7):
                    if known_left > 0 and random.random() < 0.2:  # 20% chance you know an MCQ
                        sm += 3
                        known_left -= 1
                    elif random.random() < SMART_SINGLE_RIGHT:
                        sm += 3
                    else:
                        sm -= 1
                
                # 4 multi-correct (+4/+1/-2)
                for q in range(4):
                    r = random.random()
                    actual_correct = 2 if r < 0.562 else (3 if r < 0.986 else 4)
                    
                    if known_left > 0 and random.random() < 0.1:  # 10% chance you know multi
                        sm += 4
                        known_left -= 1
                    else:
                        # Smart: mark only 1 option
                        p_right = actual_correct / 4
                        if random.random() < p_right:
                            sm += 1
                        else:
                            sm -= 2
            
            subj_marks_dict[subj_idx] = sm
            total += sm
        
        results.append(total)
        subj_results_all.append(subj_marks_dict)
    
    return results, subj_results_all

for known in [0, 1, 2, 3, 5, 8, 10]:
    results, subj_results = simulate_hybrid(known)
    
    avg = sum(results)/len(results)
    sorted_r = sorted(results)
    median = sorted_r[len(sorted_r)//2]
    p5 = sorted_r[int(len(sorted_r)*0.05)]
    p95 = sorted_r[int(len(sorted_r)*0.95)]
    
    p(f"\n{'─'*70}")
    p(f"  KNOWN per subject per paper: {known} questions ({known*6} total across exam)")
    p(f"  Mean: {avg:.1f}  Median: {median}  P5-P95: [{p5}, {p95}]")
    
    # Qualifying probability
    for year in [2020, 2022, 2023, 2024, 2025]:
        min_subj_pct, min_agg_pct, total_marks = SC_CUTOFFS[year]
        min_subj = min_subj_pct / 100 * total_marks / 3
        min_agg = min_agg_pct / 100 * total_marks
        
        q_count = 0
        for i in range(len(results)):
            sm = subj_results[i]
            if (results[i] >= min_agg and 
                all(sm[s] >= min_subj for s in range(3))):
                q_count += 1
        
        prob = q_count / len(results) * 100
        p(f"    {year} ({min_agg:.0f} agg, {min_subj:.0f}/subj): {prob:.1f}% qualify")

# ============================================================
# OPTIMAL STRATEGY COMPARISON
# ============================================================
p(f"\n\n{'█' * 70}")
p(f" STRATEGY COMPARISON: SKIP MULTI-CORRECT vs ATTEMPT MULTI-CORRECT")
p(f"{'█' * 70}")

def sim_skip_multi(trials=100000):
    results = []
    subj_all = []
    for _ in range(trials):
        subj_marks = {}
        total = 0
        for s in range(3):
            sm = 0
            for paper in range(2):
                for q in range(6):  # numerical
                    if random.random() < NUM_GUESS_RIGHT: sm += 3
                for q in range(7):  # single MCQ
                    if random.random() < SMART_SINGLE_RIGHT: sm += 3
                    else: sm -= 1
                # SKIP multi-correct entirely
            subj_marks[s] = sm
            total += sm
        results.append(total)
        subj_all.append(subj_marks)
    return results, subj_all

def sim_attempt_multi(trials=100000):
    results = []
    subj_all = []
    for _ in range(trials):
        subj_marks = {}
        total = 0
        for s in range(3):
            sm = 0
            for paper in range(2):
                for q in range(6):
                    if random.random() < NUM_GUESS_RIGHT: sm += 3
                for q in range(7):
                    if random.random() < SMART_SINGLE_RIGHT: sm += 3
                    else: sm -= 1
                for q in range(4):  # multi: mark only 1
                    actual = 2 if random.random() < 0.562 else 3
                    p_right = actual / 4
                    if random.random() < p_right: sm += 1
                    else: sm -= 2
            subj_marks[s] = sm
            total += sm
        results.append(total)
        subj_all.append(subj_marks)
    return results, subj_all

r_skip, s_skip = sim_skip_multi()
r_attempt, s_attempt = sim_attempt_multi()

p(f"\n  Skip Multi:    Mean={sum(r_skip)/len(r_skip):.1f}, Median={sorted(r_skip)[50000]}")
p(f"  Attempt Multi: Mean={sum(r_attempt)/len(r_attempt):.1f}, Median={sorted(r_attempt)[50000]}")

for year in [2020, 2022, 2023, 2025]:
    min_subj_pct, min_agg_pct, total_marks = SC_CUTOFFS[year]
    min_subj = min_subj_pct / 100 * total_marks / 3
    min_agg = min_agg_pct / 100 * total_marks
    
    q_skip = sum(1 for i in range(len(r_skip)) 
                 if r_skip[i] >= min_agg and all(s_skip[i][s] >= min_subj for s in range(3)))
    q_att = sum(1 for i in range(len(r_attempt))
                if r_attempt[i] >= min_agg and all(s_attempt[i][s] >= min_subj for s in range(3)))
    
    p(f"  {year}: Skip={q_skip/1000:.1f}%  Attempt={q_att/1000:.1f}%  → {'SKIP better' if q_skip>q_att else 'ATTEMPT better'}")

outpath = r"d:\Jee Advanced Tukka Research\HYBRID_SIMULATION.txt"
with open(outpath, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Written to {outpath}")
