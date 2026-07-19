# A Divisor-Residue Criterion for Bounded A-Parameters in the Erdős–Straus Conjecture

[![Verify](https://github.com/pottertech/erdos-straus-divisor-residue/actions/workflows/verify.yml/badge.svg)](https://github.com/pottertech/erdos-straus-divisor-residue/actions/workflows/verify.yml)

This repository contains the manuscript, verification code, and research
documentation for the divisor-residue approach to the Erdős–Straus conjecture.

## Contents

- `paper/` — manuscript source (`manuscript.md`) and compiled PDF
- `code/verify.py` — SymPy verification of key theorems and computational results
- `code/search_solutions.py` — exhaustive search for Erdős–Straus solutions
- `code/verify_lemma.py` — verification of the Bounded Divisor-Residue Lemma
- `docs/research-journey.html` — narrative account of the research process
- `references/` — reference notes
- `CITATION.cff` — citation metadata
- `results/` — pre-generated computational artifacts (search results, distributions, outliers)
- `references/` — reference notes
- `CITATION.cff` — citation metadata
- `.github/workflows/verify.yml` — automated verification on push (fast smoke test)

## Summary

We present a divisor-residue criterion for the Erdős–Straus conjecture in the
residue class n ≡ 1 (mod 12), n ≢ 0 (mod 5). We introduce a parameter A = 4x − n
and reduce the conjecture to a **bounded divisor-residue condition**: for each
admissible n, there must exist bounded A ≡ 3 (mod 4) and a divisor P of
(n(n+A)/4)² satisfying P ≡ −n²·4⁻¹ (mod A) with positive y, z.

**Proven results:**
- Theorem 1: Exact divisor-residue criterion (T ∈ D_A iff A works)
- Theorem 2: n ≡ 5 (mod 8) always admits A = 3 (direct proof)
- Theorem 4: Composite n with factor ≡ 3 (mod 4) (Mballa 2026)
- Theorem 5: Legendre symbol identity for the m-route
- Theorem 3 converse: No QNR → T ∉ D_A (unconditional)
- Bounded Divisor-Residue Lemma: Proven for h=2 and order-2 QNR cases (92.4%)

**Computational results (verified, not proven):**
- Theorem 3 forward direction: T ∈ D_A iff QNR exists (0 mismatches, 6,473 cases)
- Theorem 6: A ≤ 31 covers all n ≤ 100,000
- Theorem 7: A ≤ 99 covers all but 1 of 666,666 cases up to 10,000,000

**Open gaps (honestly identified):**
1. Bounded Divisor-Residue Lemma in full generality (7.6% of cases computational only)
2. D_A closure / shifted divisor-residue set (T ∈ D_A directly, not via −1 factorization)
3. Constant bound conjecture (A ≤ C for all n)
4. Covering system proof ({3,7,11,15,19,23,31} for all n, not just n ≤ 100K)

## Verification

The repo distinguishes **fast CI smoke tests** from **full verification runs**.

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

# Bounded Divisor-Residue Lemma (full categorization)
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
| `results/README.md` | How artifacts were generated |

Regenerate with the commands in the **Full computational verification** section above.

## Status

## Status

This manuscript is a research note / preprint and has not been peer reviewed.
It does NOT claim a proof of the Erdős–Straus conjecture. It presents a new
framework, proven partial results, and strong computational evidence with
honestly identified gaps.

## License

MIT — see `LICENSE` for details.
