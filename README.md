# A Divisor-Residue Criterion for Bounded A-Parameters in the Erdős–Straus Conjecture

[![Verify](https://github.com/pottertech/erdos-straus-divisor-residue/actions/workflows/verify.yml/badge.svg)](https://github.com/pottertech/erdos-straus-divisor-residue/actions/workflows/verify.yml)

**Author:** Kevin Potter

This repository contains the manuscript, verification code, computational
results, and research analysis for the divisor-residue approach to the
Erdős–Straus conjecture.

> **⚠️ Status:** This is a research note / preprint. It is **NOT** a proof of
> the Erdős–Straus conjecture. It presents a new framework, proven partial
> results, strong computational evidence, and honestly identified open
> problems.

## Contents

- `paper/` — manuscript source (`manuscript.md`, `manuscript.tex`)
- `docs/manuscript.pdf` — compiled PDF
- `code/verify.py` — SymPy verification of key theorems and computational results
- `code/search_solutions.py` — exhaustive search for Erdős–Straus solutions
- `code/verify_lemma.py` — verification of the Partial −1 Route (proven subcases + failure categorization)
- `verify_all.py` — one-click verification script (fast / full / full-10m modes)
- `docs/research-journey.html` — narrative account of the research process
- `results/` — pre-generated computational artifacts (search results, distributions, outliers)
- `analysis/` — research analysis scripts and findings, organized by topic
- `references/` — reference notes
- `CITATION.cff` — citation metadata
- `.github/workflows/verify.yml` — automated verification on push (fast smoke test)

## Proven Results

- **Theorem 1 (Divisor-Residue Criterion):** Exact criterion — T ∈ D_A if and
  only if A yields an Erdős–Straus solution for n.
- **Theorem 2 (n ≡ 5 mod 8):** Prime n ≡ 5 (mod 8) always admits A = 3 (direct proof).
- **Theorem 5 (Legendre Identity):** Legendre symbol identity for the m-route.
- **Theorem 3 Converse:** No QNR → T ∉ D_A (unconditional).
- **Partial −1 Route Result:** Proven for h=2 and order-2 QNR cases. The general
  implication −1 ∈ H(A) ⇒ −1 ∈ D_A fails in 821 tested cases, so the forward
  direction must be proved by direct T ∈ D_A, centered-set, or alternative
  divisor-path methods.

## Computational Results (Verified, Not Proven)

- **Theorem 3 forward direction:** Computationally supported; 10,096 positive
  (−1 ∈ D_A) cases classified, with 821 -1-route failure / alternative-path cases
  identified.
- **Theorem 6 (A ≤ 31, n ≤ 100K):** All admissible n ≤ 100,000 covered with A ≤ 31.
- **Theorem 7 (A ≤ 99, n ≤ 10M):** 666,665 of 666,666 cases up to 10,000,000
  covered with A ≤ 99. Single outlier: n = 8,803,369 (requires A = 107).
- **Theorem 9 (Covering Set, n ≤ 100K):** The prime covering set
  {3, 7, 11, 19, 23, 31} suffices for all n ≤ 100,000.
- **Theorem 9a (A ≤ 59, n ≤ 10M):** Extended covering verified to 10,000,000
  with A ≤ 59 (see `results/covering_set_10m.json`).
- **Theorem 10 (Parity Obstruction):** Parity-based obstruction identified for
  certain residue classes.

## Open Problems

1. **General −1 Route / Centered Residue:** The original −1-route fails in 821
   cases. Prove a direct criterion, likely through the centered divisor-residue
   set C_A(N). See `analysis/item1_lemma/` for computational groundwork.
2. **Shifted Divisor-Residue Set:** **RESOLVED — dead end.** The shifted set
   D_A^(nm) approach produces zero successes among anomalous cases. See
   `analysis/item2_gap/shifted_set_findings.md`.
3. **Constant Bound Conjecture:** A ≤ C for all n (computational evidence
   supports but does not prove).
4. **Covering System Proof:** Extend the covering set {3, 7, 11, 19, 23, 31}
   to all n, not just n ≤ 100K. This is the current research frontier. See
   `analysis/covering_set/` for verification scripts and results.
5. **Burgess Bound Route:** Fully sourced analytic argument via Burgess-type
   bounds for the least quadratic non-residue. See
   `analysis/proof_artifacts/proposition8_sourced.md` for the complete argument
   with references.

## Analysis Directory Structure

| Subdirectory | Contents |
|---|---|
| `analysis/item1_lemma/` | Centered residue analysis, computational cases, lemma findings |
| `analysis/item2_gap/` | Shifted set analysis, Kneser gap analysis, anomalous case classification, trivial stabilizer analysis |
| `analysis/item2_quotient/` | Quotient gap analysis, quotient deep analysis, quotient lifting analysis |
| `analysis/covering_set/` | Covering set verification (100K & 10M), covering system proof, per-h analysis, m-route sufficiency |
| `analysis/proof_artifacts/` | Case-by-case proof, short signed representation analysis, Proposition 8 (Burgess) sourced argument |

## Verification

The repo distinguishes **fast CI smoke tests** from **full verification runs**.

### Environment

- Python 3.12+
- SymPy ≥ 1.13.1 (exact rational arithmetic — no floating point)
- See `requirements.txt` for pinned dependencies

### One-click verification

```bash
pip install -r requirements.txt

# Fast smoke test (n ≤ 1000, ~30s) — what CI runs
python3 verify_all.py

# Full verification (n ≤ 100,000, ~2min)
python3 verify_all.py --full

# Complete verification (n ≤ 10,000,000, ~10min)
python3 verify_all.py --full-10m
```

### Fast CI (runs on every push, ~30s)

```bash
pip install -r requirements.txt
python3 code/verify.py
```

Checks all theorems on a small subset (n ≤ 1000, Theorem 1 on n ≤ 500)
for quick feedback. This is what GitHub Actions runs.

### Full computational verification (requires local run)

```bash
# Theorem 6: A ≤ 31 covers all n ≤ 100,000
python3 code/search_solutions.py 100000 31 results/search_100k.json

# Theorem 7: A ≤ 99 covers all but 1 of 666,666 cases up to 10,000,000
python3 code/search_solutions.py 10000000 99 results/search_10m_summary.json

# Partial −1 Route (full categorization)
python3 code/verify_lemma.py 100000

# Witness for the outlier n = 8,803,369
python3 code/search_solutions.py --witness 8803369 200
```

Pre-generated result artifacts are committed in `results/` (see below).

## Result Artifacts

Pre-generated computational artifacts are committed in `results/`:

| File | Description |
|------|-------------|
| `results/search_100k.json` | Theorem 6: all n ≤ 100,000 covered with A ≤ 31 |
| `results/search_10m_summary.json` | Theorem 7: 666,666 cases up to 10M, A ≤ 99 |
| `results/outlier_8803369.json` | Witness for the single outlier n = 8,803,369 |
| `results/a_distribution_100k.csv` | A-value distribution for n ≤ 100,000 |
| `results/anomalous_cases_verified.json` | Cases where −1 ∈ D_A but −1 ∉ D_A^(nm) (shifted set failures) |
| `results/covering_set_10m.json` | Theorem 9a: covering set verification up to 10,000,000 |
| `results/README.md` | How artifacts were generated |

Regenerate with the commands in the **Full computational verification** section above.

## Known Outlier

The single outlier **n = 8,803,369** requires **A = 107** (exceeding the A ≤ 99 bound).
This is documented in `results/outlier_8803369.json` with full witness details:

- x = 2,200,869, y = 181,085,300,330, z = 3,293,760,527,702,370
- Verified: 4/8803369 = 1/2200869 + 1/181085300330 + 1/3293760527702370 ✅

This is a **verified manual exception**, not a code bug. If you run the 10M search
and see 1 uncovered case, this is expected.

## License

MIT — see `LICENSE` for details.

## AI Assistance Disclosure

This research was developed with the assistance of AI tools (OpenClaw / Claude).
All mathematical arguments were reviewed, verified computationally with exact
arithmetic (SymPy), and checked by the author. The AI assisted with computational
verification, manuscript preparation, and code development. The mathematical
content, analysis, and conclusions are the responsibility of the author.