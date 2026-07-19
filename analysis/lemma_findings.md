# Bounded Divisor-Residue Lemma: Computational-Only Cases Analysis

## Overview

This document presents a detailed computational analysis of the "computational-only"
cases of the Bounded Divisor-Residue Lemma. These are cases where -1 ∈ H(A) and
-1 ∈ D_A (verified computationally), but the case does not fall into any of the
three proven categories:

1. **Case 1 (h=2):** |H(A)| = 2 — single QNR prime, direct proof
2. **Case 2a (order-2 QNR):** Some prime factor p of nx has order 2 mod A (p ≡ -1 mod A)
3. **Case 2b-Kneser:** Kneser's theorem applies — trivial stabilizer + Σ(2eᵢ+1) ≥ m+k-1

## Parameters

- **n range:** 13 to 100,000
- **n conditions:** n prime, n ≡ 1 (mod 12), n ≢ 0 (mod 5)
- **A values:** [3, 7, 11, 19, 23, 31] (prime, ≡ 3 mod 4)
- **Total prime-A cases with -1 ∈ H(A):** 10,917

## Categorization Results

| Category | Count | Percentage | Status |
|----------|-------|------------|--------|
| Case 1 (h=2) | 1,768 | 16.20% | PROVEN |
| Case 2a (order-2 QNR) | 1,919 | 17.58% | PROVEN |
| Case 2b-Kneser (trivial stab) | 194 | 1.78% | PROVEN |
| Case 2b-Size-only (non-trivial stab) | 4,414 | 40.43% | CANDIDATE |
| **Computational-only** | **1,801** | **16.50%** | **COMPUTATIONAL** |
| Failures (-1 ∉ D_A) | 821 | 7.52% | LEMMA FAILS |
| -1 in shifted D_A^(nm) | 7,883 | 72.20% | — |

**Proven total:** 3,881 (35.55%)
**Size-only (candidate):** 4,414 (40.43%)
**Computational-only:** 1,801 (16.50%)
**Failures:** 821 (7.52%) — cases where -1 ∈ H(A) but -1 ∉ D_A

### Note on "Failures"

The 821 failures are cases where -1 ∈ H(A) but -1 ∉ D_A. These are NOT computational-only
cases — they are genuine failures of the lemma. The lemma as stated (-1 ∈ H(A) ⟹ -1 ∈ D_A)
does NOT hold universally. The computational-only cases (1,801) are those where -1 IS in D_A
but cannot be proven by any of the three established proof strategies.

## Key Structural Finding: All Computational-Only Cases Have h = A-1

**Every single computational-only case has h = |H(A)| = A-1**, meaning H(A) = (Z/AZ)*
(the full multiplicative group). This is a critical structural insight.

The computational-only cases break down into exactly three (A, h) pairs:

| A | h = A-1 | Count | (Z/AZ)* structure |
|---|---------|-------|-------------------|
| 19 | 18 | 308 | Cyclic group of order 18 |
| 23 | 22 | 507 | Cyclic group of order 22 |
| 31 | 30 | 986 | Cyclic group of order 30 |

**No computational-only cases exist for A ∈ {3, 7, 11}.** For these smaller primes,
all cases where -1 ∈ D_A are covered by the proven categories.

## Sub-Categories of Computational-Only Cases

The 1,801 computational-only cases split into three structural sub-categories:

### Sub-Category 1: Trivial Stabilizer + Kneser Fails (703 cases)

- Stabilizer of D_A in H(A) is trivial (size 1)
- Kneser size condition fails: Σ(2eᵢ+1) < m+k-1
- |D_A| < |H(A)| in most cases (ratio 0.30–0.97, mean 0.75)
- -1 is in D_A but D_A ≠ H(A), so a direct argument showing D_A = H is not available
- Shifted set: 135/703 (19.2%) have -1 ∈ D_A^(nm)
- Witness exceeds tight bound: 42/703 (6.0%)

### Sub-Category 2: Stabilizer = h (D_A = H = Full Group) (894 cases)

- Stabilizer = H(A) = (Z/AZ)*, meaning D_A is invariant under the full group
- This implies D_A = H(A) = (Z/AZ)*, so -1 is trivially in D_A
- Kneser size condition fails (the bound is too weak to prove |D_A| = |H|)
- **These are the "easy" computational cases** — the lemma holds trivially because
  D_A = (Z/AZ)*, but Kneser's theorem cannot prove it because the size bound is insufficient
- Shifted set: 470/894 (52.6%) have -1 ∈ D_A^(nm)
- Witness exceeds tight bound: 129/894 (14.4%)

### Sub-Category 3: Proper Non-Trivial Stabilizer (204 cases)

- Stabilizer is a proper subgroup of H(A) (1 < |Stab| < h)
- All 204 cases have A = 31 (with 9 exceptions having A = 19)
- Stabilizer subgroups are cyclic:
  - Order 3: {1, 5, 25} — 72 cases
  - Order 5: {1, 2, 4, 8, 16} — 100 cases  
  - Order 6: {1, 5, 6, 25, 26, 30} — 32 cases
- Shifted set: 15/204 (7.4%) have -1 ∈ D_A^(nm)
- Witness exceeds tight bound: 51/204 (25.0%)

## Kneser Gap Analysis

The Kneser gap = (m + k - 1) - Σ(2eᵢ+1), where m = h/2:

| Gap | Count | Fraction |
|-----|-------|----------|
| 2 | 786 | 43.6% |
| 4 | 323 | 17.9% |
| 6 | 362 | 20.1% |
| 8 | 280 | 15.5% |
| 10 | 50 | 2.8% |

- **Minimum gap:** 2
- **Maximum gap:** 10
- **Mean gap:** 4.32

The gap is always positive (all computational-only cases fail the Kneser size condition).
The gap is relatively small (2–10), suggesting the bound is "almost" met.

## Shifted Set D_A^(nm) Analysis

The shifted set D_A^(nm) uses the tighter bound aᵢ ≤ eᵢ (instead of 2eᵢ):

| Status | Count | Fraction |
|--------|-------|----------|
| -1 ∈ D_A^(nm) | 620 | 34.4% |
| -1 ∉ D_A^(nm) | 1,181 | 65.6% |

**The shifted set does NOT capture all computational-only cases.** Only 34.4% of cases
have -1 in the shifted set. The majority (65.6%) require the full bound (aᵢ ≤ 2eᵢ).

### By sub-category:

| Sub-Category | -1 ∈ D_A^(nm) | Total | % |
|--------------|---------------|-------|---|
| Trivial stabilizer | 135 | 703 | 19.2% |
| Stab = h (full) | 470 | 894 | 52.6% |
| Stab < h (proper) | 15 | 204 | 7.4% |

## Witness Exponent Analysis

### How many primes are used in witnesses?

| Pattern | Count | Fraction |
|---------|-------|----------|
| Two primes | 1,002 | 55.6% |
| Three primes | 691 | 38.4% |
| Four+ primes | 108 | 6.0% |
| Single prime | 0 | 0.0% |

**No single-prime witnesses exist** — all witnesses require at least 2 primes.
This rules out a simple "one prime suffices" argument.

### Do witness exponents exceed the tight bound (aᵢ > eᵢ)?

- **Within tight bound (aᵢ ≤ eᵢ):** 1,579 (87.7%)
- **Exceeds tight bound (aᵢ > eᵢ):** 222 (12.3%)

When exponents exceed the tight bound, the excess is almost always exactly 1
(aᵢ = eᵢ + 1), with only 3 cases where aᵢ = eᵢ + 2.

**The primes that most often exceed the tight bound** are small primes (5, 7, 3, 19, 11),
suggesting that when the tight bound fails, it's typically because a small prime factor
needs one extra power.

## Hypothesis Testing Results

### Hypothesis A: -1 ∈ D_A^(nm) for ALL computational-only cases

**RESULT: REFUTED.** Only 620/1,801 (34.4%) of computational-only cases have -1 ∈ D_A^(nm).
The shifted set D_A^(nm) with tight bound aᵢ ≤ eᵢ is NOT sufficient to capture all cases.
1,181 cases require the full bound (aᵢ ≤ 2eᵢ).

### Hypothesis B: Multi-Kneser Argument

A "multi-Kneser" approach (apply Kneser to a subset, then extend) could work for:
- **Stab = h cases (894):** Since D_A = H = (Z/AZ)*, a completely different argument is
  needed — not an extension of Kneser but a direct proof that D_A = (Z/AZ)*
- **Stab < h cases (204):** Quotient by the stabilizer and apply Kneser in the quotient
  group. The stabilizer subgroups are small (order 3, 5, 6), so the quotient is large.
- **Trivial stab cases (703):** Kneser fails on size, so a different counting argument
  or direct construction is needed.

### Hypothesis C: Witness exponents always satisfy aᵢ ≤ eᵢ

**RESULT: REFUTED.** 222 cases (12.3%) have witness exponents exceeding the tight bound
(aᵢ > eᵢ for some prime). The excess is typically 1 (aᵢ = eᵢ + 1). This confirms that
the shifted set D_A^(nm) is NOT the right object for a complete proof.

### Hypothesis D: Simple witness patterns (≤2 primes)

**RESULT: PARTIAL.** 1,002/1,801 (55.6%) of witnesses use exactly 2 primes.
691 (38.4%) use 3 primes, and 108 (6.0%) use 4+ primes. A "2-prime argument"
would cover over half the cases but not all.

## Potential Proof Strategies

### Strategy 1: Direct Proof for D_A = (Z/AZ)* (894 cases, 49.6%)

For the 894 cases where D_A = H(A) = (Z/AZ)*, the lemma holds trivially.
The challenge is proving that D_A = (Z/AZ)* under conditions where Kneser's
bound is insufficient. Key observations:
- All these cases have h = A-1 (H = full group)
- The generators (prime factors of nx mod A) generate the full group
- The exponent bounds (2eᵢ) are large enough to cover all residues

A potential approach: show that when the generators of (Z/AZ)* have sufficiently
large exponent bounds, the bounded product set must equal the full group. This
could use a "covering" argument: the geometric progression {g, g², ..., g^{2e}}
for a generator g must cover enough residues to force the product set to be everything.

### Strategy 2: Stabilizer Quotient for Proper Non-Trivial Stabilizer (204 cases, 11.3%)

For cases with stabilizer of order 3, 5, or 6 in (Z/31Z)*:
1. Quotient (Z/31Z)* by the stabilizer to get a smaller group
2. Apply Kneser's theorem in the quotient
3. Lift back to show -1 ∈ D_A

The quotient groups have orders 10, 6, and 5 respectively (since |(Z/31Z)*| = 30).
Kneser's bound in the quotient would be much easier to satisfy.

### Strategy 3: Direct Construction for Trivial Stabilizer (703 cases, 39.0%)

For cases with trivial stabilizer where Kneser's size condition fails:
- |D_A| is typically 30-97% of |H(A)|
- -1 is in D_A but D_A ≠ H(A)
- A direct construction showing which exponent combinations yield -1 mod A
  could be developed, potentially using the Chinese Remainder Theorem or
  properties of the specific A values (19, 23, 31)

Since only 3 values of A are involved (19, 23, 31), a case-by-case argument
for each A is feasible. The group structures are:
- (Z/19Z)* ≅ C₁₈ (cyclic, order 18)
- (Z/23Z)* ≅ C₂₂ (cyclic, order 22)
- (Z/31Z)* ≅ C₃₀ (cyclic, order 30)

### Strategy 4: Case-by-Case for A ∈ {19, 23, 31}

Since ALL computational-only cases have A ∈ {19, 23, 31}, a case-by-case proof
for each A value would close the gap entirely. For each A:

1. Characterize which n values lead to computational-only cases
2. Use the specific group structure of (Z/AZ)* to construct -1 explicitly
3. Show that the bounded exponent conditions always allow -1 to be reached

This is the most promising strategy given the extreme concentration in just
3 values of A.

## Summary of Key Findings

1. **1,801 computational-only cases** out of 10,917 total (where -1 ∈ H(A))
   = 16.50% of cases.

2. **Zero failures within computational-only cases:** All 1,801 cases have -1 ∈ D_A
   (by definition). The 821 separate failures are cases where the lemma itself fails.

3. **Extreme structural concentration:** ALL computational-only cases have:
   - h = A-1 (H(A) = full multiplicative group)
   - A ∈ {19, 23, 31} (only 3 prime moduli)

4. **Three sub-categories:**
   - Trivial stabilizer + Kneser fails: 703 cases (39.0%)
   - Stab = h (D_A = full group) + Kneser fails: 894 cases (49.6%)
   - Proper non-trivial stabilizer + Kneser fails: 204 cases (11.3%)

5. **Shifted set D_A^(nm) is NOT sufficient:** Only 34.4% of computational-only
   cases have -1 in the shifted set. 65.6% require the full bound (aᵢ ≤ 2eᵢ).

6. **Witness patterns:** 55.6% use 2 primes, 38.4% use 3 primes, 6.0% use 4+.
   No single-prime witnesses exist.

7. **Witness exponents exceed tight bound in 12.3% of cases**, always by exactly 1
   (with 3 exceptions where the excess is 2).

8. **Kneser gap ranges from 2 to 10** (mean 4.32), with 43.6% having gap = 2.

9. **Stabilizer subgroups for A=31:** Cyclic groups of order 3, 5, and 6,
   which are proper subgroups of (Z/31Z)* ≅ C₃₀.

## Recommended Next Steps

1. **Case-by-case proof for A ∈ {19, 23, 31}** — This is the most promising
   approach given the extreme concentration in just 3 values of A.

2. **Direct proof that D_A = (Z/AZ)* for the 894 "full group" cases** —
   These cases have D_A = H = (Z/AZ)*, so a proof that the bounded product
   set equals the full group under these conditions would close half the gap.

3. **Stabilizer quotient argument for the 204 proper non-trivial stabilizer cases** —
   Quotient by the stabilizer (order 3, 5, or 6) and apply Kneser in the quotient.

4. **Direct construction for the 703 trivial stabilizer cases** —
   Use the specific group structure of (Z/19Z)*, (Z/23Z)*, (Z/31Z)* to
   construct -1 explicitly as a bounded product.

5. **Investigate the 821 failures** (where -1 ∈ H(A) but -1 ∉ D_A) —
   These are NOT computational-only cases but genuine lemma failures.
   Understanding why the lemma fails for these cases could illuminate
   the boundary between proven and computational cases.

---
Generated by computational_cases.py
Date: 2026-07-19