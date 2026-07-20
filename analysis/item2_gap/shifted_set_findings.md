# Item 2: D_A Closure / Shifted Divisor-Residue Set — Structural Analysis

## Problem Statement

The Bounded Divisor-Residue Lemma requires showing that T = −nm mod A lies in D_A (the bounded divisor-residue set with bound 2e). The original proof strategy attempts this via the factorization:

  T = (−1) · nm,  so  −1 ∈ D_A  AND  −1 ∈ D_A^(nm)  ⟹  T ∈ D_A

where D_A^(nm) is the "shifted set" with tight bound e (exponents a_i ≤ e_i).

The question: **what happens when −1 ∈ D_A but −1 ∉ D_A^(nm)?**

## Computational Scan

- **n range:** 13 to 100,000
- **n conditions:** n prime, n ≡ 1 (mod 12), n ≢ 0 (mod 5)
- **A values:** {3, 7, 11, 19, 23, 31} (prime, ≡ 3 mod 4)
- **Total prime-A cases scanned:** 14,244

## Results

| Category | Count | Percentage |
|----------|-------|------------|
| Total prime-A cases | 14,244 | 100% |
| −1 ∈ D_A | 10,917 | 76.6% |
| Anomalous (−1 ∈ D_A, −1 ∉ D_A^(nm)) | 2,213 | 15.5% |
| T ∈ D_A (alternative path found) | 1,322 | 59.7% of anomalous |
| T ∉ D_A (lemma fails) | 891 | 40.3% of anomalous |
| T ∈ D_A^(nm) (shifted set) | 0 | 0.0% of anomalous |

### By A value

| A | Anomalous | T ∈ D_A | T ∉ D_A |
|---|-----------|---------|---------|
| 7 | 170 | 156 | 14 |
| 11 | 228 | 168 | 60 |
| 19 | 547 | 316 | 231 |
| 23 | 533 | 406 | 127 |
| 31 | 735 | 276 | 459 |

## Key Structural Finding

**In 100% of the 1,322 cases where T ∈ D_A:**

1. **T is NOT in the shifted set D_A^(nm)** — zero cases have T reachable with tight bound
2. **The standard path (−1)·nm fails** — the −1 witness always has some exponent a_i > e_i, making a_i + e_i > 2e_i (overflow)
3. **T reaches D_A via a genuinely different divisor path** — the T-witness uses exponents b_i ≤ 2e_i that are NOT equal to (a_i + e_i) for any −1-witness
4. **The dlog identity holds** — Σ b_i·s_i ≡ h/2 + dlog(nm) (mod h) directly, without factoring through −1

### Exceedance Pattern

In the T-witnesses, how many primes exceed the tight bound e_i:
- 1 prime exceeds: 415/500 (83%)
- 2 primes exceed: 83/500 (16.6%)
- 3 primes exceed: 2/500 (0.4%)

## Conclusion

**The shifted set D_A^(nm) is the wrong tool for the anomalous cases.**

The correct proof strategy is **direct construction**: find exponents b_i ≤ 2e_i with

  Σ b_i · s_i ≡ h/2 + dlog(nm)  (mod h)

This is a strictly weaker condition than requiring −1 ∈ D_A^(nm), because the bounded sumset with bound 2e is larger than the bounded sumset with bound e. The sumset {Σ b_i·s_i : 0 ≤ b_i ≤ 2e_i} can contain the target h/2 + dlog(nm) even when {Σ a_i·s_i : 0 ≤ a_i ≤ e_i} does not contain h/2.

### What still fails

The 891 cases where T ∉ D_A remain genuine lemma failures. These are the same cases identified in the Item 1 analysis as "computational-only" cases requiring case-by-case verification.

### Implications for the manuscript

The shifted set D_A^(nm) should be mentioned as a sufficient condition (when it works, the proof is clean), but NOT as a necessary condition. The proof structure should be:

1. **Case 1 (h=2):** Direct — proven
2. **Case 2a (order-2 QNR):** Direct — proven
3. **Case 2b-Kneser (trivial stabilizer):** Size bound — proven
4. **Case 2b-Size-only:** Direct construction in D_A (not via shifted set) — computational
5. **Computational-only:** Case-by-case verification — computational (see Item 1 analysis)

The shifted set approach covers ~35% of computational-only cases but misses the rest. The direct construction approach covers ~60% of anomalous cases but still leaves 891 genuine failures requiring computational verification.
