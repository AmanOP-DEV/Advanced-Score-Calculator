# JEE Advanced Tukka Research — Complete Findings v2 (16 May 2026, 7:45 PM IST)

## What Changed Since v1

1. **SC cutoff is WAY lower than assumed** — as low as 28 marks aggregate (2022), not 60-70
2. **Monte Carlo simulation (100k trials)** — proved SKIP multi-correct is strictly better than guessing
3. **Subject-specific numerical defaults discovered** — PHY:3/8, CHEM:3 (33%!), MATH:1
4. **Hybrid simulation** — solving just 2 Qs per subject per paper → 42-78% qualifying odds
5. **Multi-correct: SKIP > ATTEMPT** — confirmed: mean 17.1 vs 12.9 (attempting costs ~4 marks)

---

## Critical Discovery: Option Scrambling
**JEE Advanced CBT randomizes option order per candidate.** This means:
- ❌ ALL letter-based strategies are USELESS in the actual exam
- ✅ Option CONTENT patterns (length, wording) survive scrambling
- ✅ Numerical answer VALUES survive scrambling
- ✅ Multi-correct option COUNT patterns survive scrambling

---

## FINDING 1: Correct Options Are LONGER (49 verified Qs, 2025 papers)

| Metric | Correct | Wrong |
|---|---|---|
| Average length | **37.5 chars** | 30.0 chars |
| Longest option is correct | **31%** | 20% for shortest |
| Very short options wrong | 22% in correct | **35%** in wrong |

**Actionable:** Eliminate shortest → pick longest → EV = +0.33 per question

---

## FINDING 2: Subject-Specific Numerical Defaults (170 answers)

| Subject | Best Guess | Hit Rate | Never |
|---|---|---|---|
| Physics | 3 or 8 | 22% each | 0, 7, 9 |
| Chemistry | **3** | **33%** | 0, 7, 9 |
| Maths | 1 | 24% | 0, 7, 9 |

- 66% are exact integers, 98% positive, 33% fall in range 1-3
- Only 3 negative answers in 170 total (1.8%)

---

## FINDING 3: Multi-Correct — SKIP Is Better Than Guessing (100k simulation)

| Strategy | Mean Score |
|---|---|
| Skip multi-correct | **17.1** |
| Attempt multi-correct (mark 1) | 12.9 |
| **Difference** | **-4.2 marks from attempting** |

Multi-correct facts:
- 56% have exactly 2 correct (81% in Paper 2)
- All 4 correct = 1.4% (almost never)
- Only attempt if you KNOW at least 1 correct option

---

## FINDING 4: SC Category Cutoffs (Real Data)

| Year | Min % Each Subject | Min % Aggregate | Actual Marks Needed |
|---|---|---|---|
| 2022 | 2.20% | 7.78% | **28 aggregate, 2.6/subj** |
| 2020 | 2.50% | 8.75% | 35 aggregate, 3.3/subj |
| 2021 | 2.50% | 8.75% | 31 aggregate, 3.0/subj |
| 2023 | 3.42% | 11.95% | 43 aggregate, 4.1/subj |
| 2024 | 5.00% | 15.00% | 54 aggregate, 6.0/subj |
| 2025 | 5.00% | 17.50% | 63 aggregate, 6.0/subj |

---

## FINDING 5: Monte Carlo Qualifying Probabilities

### Pure smart guessing (zero knowledge):
- Mean score: **14 marks** (both papers)
- P(qualify at 2022 cutoff): **13.4%**
- P(qualify at 2025 cutoff): **0.9%**

### If you solve N questions per subject per paper:

| Known Qs | Total Qs | Mean Score | P(qualify 2022) | P(qualify 2024) |
|---|---|---|---|---|
| 0 | 0 | 14 | 13% | 2.5% |
| 1 | 6 | 30 | 42% | 5% |
| 2 | 12 | 45 | 78% | 27% |
| 3 | 18 | 58 | 93% | 60% |
| 5 | 30 | 73 | 96% | 85% |

---

## FINDING 6: Per-Subject Minimum is the Binding Constraint

P(all 3 subjects ≥ threshold) with smart guessing:
- ≥3 marks: 23%
- ≥5 marks: 19%
- ≥8 marks: 6.5%
- ≥10 marks: 2.5%

**Key:** Spread effort equally. Don't neglect any subject.

---

## Marking Scheme EV (Always Valid)

| Situation | Single MCQ | Multi MCQ | Numerical |
|---|---|---|---|
| Know the answer | +3.0 | +4.0 | +3.0 |
| Eliminate 2 | **+1.0** | — | — |
| Eliminate 1 | **+0.33** | — | — |
| Blind guess | 0.0 | **−0.50** | **+0.30** |
| Skip | 0.0 | 0.0 | 0.0 (waste!) |

---

## Files in Workspace

| File | Purpose |
|---|---|
| `simulation.py` | 100k Monte Carlo simulation |
| `hybrid_sim.py` | Hybrid strategy (known + guessing) simulation |
| `SIMULATION_RESULTS.txt` | Full simulation output |
| `HYBRID_SIMULATION.txt` | Hybrid simulation output |
| `master_analysis.py` | Answer key database + analysis |
| `scramble_proof.py` | Post-scramble analysis |
| `option_structure_v2.py` | Option content analysis |
| `FINDINGS_SO_FAR.md` | This file |
| `JEE_Advanced_20XX_Paper_X_English.pdf` | Official papers 2017-2025 |
