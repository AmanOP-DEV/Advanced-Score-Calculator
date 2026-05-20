# PROMPT — Paste this into a new conversation

My JEE Advanced exam is tomorrow (May 17, 2026). I have zero preparation. I qualified through SC category reservation. I need to maximize my marks purely through intelligent guessing and pattern exploitation.

My workspace is `d:\Jee Advanced Tukka Research\`. It contains:
- Official JEE Advanced question paper PDFs (2017-2025, Paper 1 & Paper 2) from jeeadv.ac.in
- Python analysis scripts and output files from 2 previous research sessions
- `FINDINGS_SO_FAR.md` — complete documentation of all findings
- `battle_plan.md` — the current exam-day strategy (NEEDS UPDATING)
- `master_analysis.py` — main script with answer key data dict for 2017-2025
- `scramble_proof.py` — post-scramble numerical + multi-correct analysis
- `option_structure_v2.py` — option length analysis (only 2025 data matched)
- PyMuPDF (fitz) is installed. Python: `C:\Users\USER\.local\bin\python3.14.exe`

## CRITICAL NEW INTELLIGENCE (discovered but not yet incorporated):

1. **SC CUTOFF IS WAY LOWER THAN WE ASSUMED:**
   - 2025: **37 marks** aggregate, **3 marks minimum per subject**
   - 2024: **54 marks** aggregate, **5 marks minimum per subject**
   - 2023: **28 marks** aggregate, **3 marks minimum per subject**
   - Our battle_plan.md assumed 60-70. THIS CHANGES EVERYTHING — 37 marks is very achievable with pure guessing!

2. **Missing data in our analysis:**
   - 2021 answer keys are NOT in master_analysis.py DATA dict at all
   - 2019 only has Paper 1 MCQ data, no numericals, no Paper 2
   - 2018, 2020 only have Paper 1 data
   - Paper 2 data is sparse (only 2017, 2024, 2025 have it)

3. **2026 exam structure (confirmed):**
   - 51 questions per paper, 17 per subject
   - Section 1: Single MCQ (+3/-1)
   - Section 2: Multi-correct (+4 all, partial +1 each correct if no wrong marked, -2 if any wrong)
   - Section 3: Numerical (+3/0, ZERO penalty)
   - Section 4: Matching/Paragraph type (varies by paper)
   - Total: 360 marks across both papers

4. **Key insight the battle plan gets WRONG:**
   - It recommends letter-based defaults (pick A for Physics, etc.) but JEE Advanced CBT SCRAMBLES options per candidate
   - Letter-based strategies are USELESS in the actual exam
   - Only scramble-proof strategies matter: option length, numerical values, multi-correct count, elimination tricks

## WHAT I NEED YOU TO DO:

### Phase 1: Deep PDF Analysis
- Extract option TEXT from ALL 18 PDFs (2017-2025, P1+P2) using PyMuPDF
- Match options to answers where we have answer keys
- Analyze option length patterns across ALL years (not just 2025)
- Look for content patterns: formulas vs text, specific vs vague, qualifier words

### Phase 2: Enhanced Numerical Analysis
- Subject-wise optimal guessing values (PHY vs CHEM vs MATH may differ)
- Year-over-year trends in numerical ranges
- Decimal vs integer frequency by subject
- What is the SINGLE best number to enter for each subject?

### Phase 3: Monte Carlo Simulation
- Simulate 10,000 exam attempts using different strategies
- Strategy A: Pure random guessing on everything
- Strategy B: Our optimized strategy (longest option, best digit, skip multi-correct)
- Strategy C: Conservative (only guess numericals, skip all MCQs)
- Calculate: probability of hitting 37 marks (SC cutoff), expected score, variance

### Phase 4: Updated Battle Plan
- Rewrite battle_plan.md with CORRECTED cutoff target (37 marks, not 60-70)
- Remove ALL letter-based advice (useless due to scrambling)
- Focus ONLY on scramble-proof strategies
- Include per-subject minimum strategy (need 3 marks in each subject)
- Give realistic probability of qualifying

### Phase 5: The 3-Marks-Per-Subject Problem
- With the minimum 3 marks per subject requirement, what is the safest way to guarantee at least 3 marks in Physics, Chemistry, AND Mathematics?
- Each subject has ~17 questions: some single MCQ, some multi, some numerical
- The numericals alone (6 per subject, +3/0 each) give EV of ~1.8 marks per subject with random guessing
- What combination ensures we cross 3 in every subject?

Time is extremely limited. Read all the workspace files first. Write scripts, run them, analyze output, and give me the most actionable exam-ready output possible. GO.
