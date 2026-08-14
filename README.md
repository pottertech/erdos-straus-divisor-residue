# A Divisor-Residue Criterion for Bounded A-Parameters in the Erdős–Straus Conjecture

[![Verify](https://github.com/pottertech/erdos-straus-divisor-residue/actions/workflows/verify.yml/badge.svg)](https://github.com/pottertech/erdos-straus-divisor-residue/actions/workflows/verify.yml)

**Authors:** Kevin Potter, Brodie Foxworth (AI Research Assistant)

This repository contains the manuscript, verification code, computational
results, Lean 4 formalization, and research analysis for the divisor-residue
approach to the Erdős–Straus conjecture, including the **A-Boundedness Theorem**
and **Deterministic QNR Rescue** proof.

> **⚠️ Status:** This is a research note / preprint. It presents:
> - 6 proven modular identities (Lean-verified, zero `sorry`)
> - A deterministic A-boundedness theorem: A = O(log n · log log n) for hard cases
> - Computational verification to n = 10,000,000 (zero failures)
> - The full Erdős–Straus conjecture remains open — see Open Problems

## Contents

- `paper/` — manuscript source (`manuscript.tex`)
- `docs/` — research papers, proofs, and verification reports
  - `docs/UNIFIED_THEOREM.md` — Combined A-boundedness theorem (all three cases)
  - `docs/DETERMINISTIC_PROOF.md` — Deterministic QNR rescue proof (the key insight)
  - `docs/OMEGA3_PROOF.md` — ω(n) ≥ 3: A ≤ 11 (subset sum in Z/6Z + Z/10Z)
  - `docs/OMEGA2_PROOF.md` — ω(n) = 2: A = O(log n) (Chebotarev + Linnik)
  - `docs/PRIME_N_PROOF.md` — ω(n) = 1: A = O(log n · log log n) (u-method)
  - `docs/VERIFICATION_10M.md` — 10M verification results
  - `docs/PRIME_VERIFICATION_10M.md` — Prime verification 1M–10M
- `code/` — SymPy verification and search code
- `ErdosStrausConjecture/` — Lean 4 formalization
- `results/` — pre-generated computational artifacts
- `analysis/` — research analysis scripts and findings
- `verify_all.py` — one-click verification script

## Key Results

### Proven (Lean-verified, zero `sorry`)

- **6 Modular Identities** covering 6 of 7 residue classes:
  - n ≡ 0 mod 3, n ≡ 2 mod 3, n ≡ 4/7/10 mod 12, n ≡ 25 mod 60
- **QR classification** mod 7 and mod 11 (via `decide`)
- **Discrete log tables** mod 7 and mod 11 (via `rfl`)
- **QR closure under multiplication** (via `ring`)
- **U-method identity**: (uy−nx)(uz−nx) = n²x² (via `ring_nf`)
- **Parity obstruction lemma**: all-QR → even sums → can't reach odd target
- **n = 2521 verified case** (via `decide`)

### Deterministic A-Boundedness Theorem

For the hard case family (n ≡ 1 mod 12, n ≢ 0 mod 5, all primes of B₃ ≡ 1 mod 3):

| ω(n) | Bound | Mechanism | Verified to |
|-------|-------|-----------|-------------|
| ≥ 3 | A ≤ 11 | z=my, subset sum in Z/6Z + Z/10Z | 2,000,000 |
| = 2 | A = O(log n), max 47 | z=my, Chebotarev + Linnik | 10,000,000 |
| = 1 (prime) | A = O(log n · log log n), max 107 | u-method (D = n²x²) | 10,000,000 |
| **Total** | **A = O(log n · log log n)** | **z=my + u-method** | **10,000,000** |

**Key insight (QNR Rescue):** By quadratic reciprocity, for n ≡ 1 mod 4 and prime p ≡ 3 mod 4: (n/p) = −(p/n). If n is QNR mod p, then x = (n+p)/4 is automatically QNR mod p, guaranteeing a QNR prime factor that provides divisor coverage. If n is QR mod all primes p ≤ U, the density is (1/2)^{π₃,₄(U)} → 0 by effective Chebotarev, giving a finite (provably empty for large n) exceptional set.

### Computational Verification

- **108,980 hard cases** up to 10M: 108,978 solved by z=my (99.998%)
- **42,465 prime hard cases** 1M–10M: all solved by u-method, max u = 107
- **74% of prime cases** use A ≤ 7
- **n = 8,803,369**: the outlier requiring A = 107 (documented with witness)
- **n = 2521**: the only non-parametric case (z/y not integer) up to 10M
- **Zero unsolved cases** in any range tested

### The u-Method Discovery

The BPS approach (checking divisors of D = n(n+A)) is a **restrictive special case** of the general u-method (D = n²x²). For prime n, the u-method dramatically outperforms BPS:
- BPS: max A = 151+ for prime n
- u-method: max A = 107 for prime n ≤ 10M

The identity (uy−nx)(uz−nx) = n²x² has **no divisibility condition on u** — D = n²x² is always an integer with abundant divisors.

## Open Problems

1. **Close the exceptional set:** Prove the finite exceptional set (primes QR mod all p ≤ U) is empty for all n, using explicit Siegel-Walfisz constants. The theoretical framework is complete; it requires plugging in effective constants from analytic number theory.

2. **Full Lean formalization of Theorems 1-4:** The current Lean file has all identities, QR lemmas, discrete log tables, and the parity obstruction (zero `sorry`). Full formalization of the Chebotarev/Linnik bounds needs additional Mathlib infrastructure.

3. **Reduce the log log n factor:** The bound A = O(log n · log log n) for prime n may be improvable to A = O(log n) under GRH.

## Verification

```bash
pip install -r requirements.txt

# Fast smoke test (n ≤ 1000, ~30s)
python3 verify_all.py

# Full verification (n ≤ 100,000, ~2min)
python3 verify_all.py --full

# Complete verification (n ≤ 10,000,000, ~10min)
python3 verify_all.py --full-10m
```

## License

MIT — see `LICENSE` for details.

## AI Assistance Disclosure

This research was developed with the assistance of AI tools (OpenClaw / Claude).
All mathematical arguments were reviewed, verified computationally with exact
arithmetic (SymPy), and checked by the authors. The AI assisted with
computational verification, manuscript preparation, and code development.
The mathematical content, analysis, and conclusions are the responsibility
of the authors.