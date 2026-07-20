# Short Signed Representation Analysis

## Overview

Analysis of the centered divisor-residue set Σ_A(N) = {Σ s_i·δ_i mod h : −e_i ≤ δ_i ≤ e_i}
for all 10,917 prime-A cases with h even. The centered criterion h/2 ∈ Σ_A(N) is perfectly
equivalent to T ∈ D_A across all 14,244 tested cases (0 mismatches).

## Shortest Signed Representation Length

| Length | Count | Percentage of successes |
|--------|-------|------------------------|
| 1 | 3,779 | 41.0% |
| 2 | 4,540 | 49.2% |
| 3 | 878 | 9.5% |
| 4 | 34 | 0.4% |
| **Total successful** | **9,231** | |
| **Failures** | **1,686** | |

## Length 1: Order-2 QNR (3,779 cases)

A single prime p_i with s_i = h/2, meaning p_i ≡ −1 (mod A).
Using δ_i = 1 gives s_i · 1 = h/2. Already proven (Case 2a).

Distribution: primes from m dominate (3,021) over primes from n (758).

## Length 2: Complementary Pairs (4,540 cases)

Two clean structural patterns, both verified computationally:

### Pattern A: Product ≡ −1 (1,555 cases)
- Dlogs satisfy s_i + s_j ≡ h/2 (mod h)
- Equivalently: p_i · p_j ≡ −1 (mod A)
- Witness: δ_i = δ_j = 1 (or both −1)
- One prime is QNR, the other is QR (since QNR · QR = QNR, and −1 is QNR for A ≡ 3 mod 4)

### Pattern B: Ratio ≡ −1 (1,339 cases)
- Dlogs satisfy s_i − s_j ≡ ±h/2 (mod h)
- Equivalently: p_i ≡ −p_j (mod A)
- Witness: δ_i = 1, δ_j = −1 (or vice versa)

### Higher deltas (1,646 cases)
- |δ| > 1 for at least one prime
- Most common: (−1, −1) with |δ|=1 still dominant
- |δ|=1 accounts for 7,419 of 8,532 deltas (87%)

## Source Distribution

Which part of N = n · m do the primes come from?

| Length | m-only | n+m | n-only |
|--------|--------|-----|--------|
| 1 | 3,021 (80%) | — | 758 (20%) |
| 2 | 3,440 (76%) | 1,100 (24%) | 0 |
| 3 | 549 (63%) | 329 (37%) | 0 |
| 4 | 5 (15%) | 29 (85%) | 0 |

m-primes dominate because m = (n+A)/4 grows with A and typically has more prime factors.

## Critical Correlation: Pairs Predict Success

| | Has complementary pair | No pair |
|---|---|---|
| **Success** | 6,836 | 2,395 |
| **Failure** | 0 | 1,686 |

**Zero failures have a complementary pair.** Every case with a pair (s_i + s_j = h/2 or s_i − s_j = h/2) succeeds. The pair is a **witness**, not just a correlation.

## Failure Analysis (1,686 cases)

### What doesn't explain failures:
- **GCD obstruction:** All failures have GCD(dlogs, h) = 1 — h/2 is structurally reachable
- **Subgroup coverage:** 32% of failures generate the full additive group Z/hZ
- **Total width:** Failures have mean Σ(2e+1) = 16.2 vs 25.1 for successes, but many failures have width > h

### What does explain failures:
- **No complementary pair exists:** No two dlogs sum or differ to h/2
- **No single generator reaches h/2:** 0 of 1,686 failures have a generator that individually reaches h/2
- **Fewer generators:** Mean 2.97 generators (vs 3.87 for successes)
- **Large h with few generators:** Concentrated at A=31/h=30 (690) and A=19/h=18 (600)

### Failure distribution by (A, h):

| A | h | Failures |
|---|---|---------|
| 31 | 30 | 690 |
| 19 | 18 | 600 |
| 23 | 22 | 147 |
| 11 | 10 | 111 |
| 7 | 6 | 105 |
| 31 | 10 | 33 |

## Theorem Candidates

### Theorem A (Pair Witness — trivially true)
If there exist prime factors p_i, p_j of N with p_i · p_j ≡ −1 (mod A) or p_i ≡ −p_j (mod A),
and e_i, e_j ≥ 1, then h/2 ∈ Σ_A(N), i.e., A works.

This is trivially true — the pair IS the witness with δ = ±1. It covers 2,894 cases directly.

### Theorem B (Open — Pair Existence)
For prime A ≡ 3 (mod 4) and N = n·(n+A)/4, if H(A) has even order and contains −1,
under what conditions do there exist prime factors p_i, p_j of N with s_i + s_j ≡ h/2 (mod h)?

This is the key open question. It may be attackable via character sum / reciprocity arguments.

### Theorem C (Open — Bounded Coverage)
For prime A ≡ 3 (mod 4), if Σ(2e_i + 1) ≥ h + k − 1 and the additive stabilizer of Σ_A(N)
in Z/hZ is trivial, then h/2 ∈ Σ_A(N).

This is the centered Kneser approach. Currently 0 tested cases fall into the trivial-stabilizer
bucket after corrected discrete-log computation, so this condition is not currently useful
but remains a valid sufficient condition.

## Next Steps

1. **Attack Theorem B:** When do complementary dlog pairs exist? This could connect to
   quadratic reciprocity, character sums, or the distribution of Legendre symbols among
   prime factors of linear forms.

2. **Analyze the 2,395 successes without pairs:** These use length 3+ representations.
   What structural patterns do they use? Can we find a second-tier witness?

3. **Understand the 1,686 failures:** These have no pair and no short representation.
   Are they concentrated in specific residue classes? Do they correlate with n being
   QR mod all small primes?

4. **Centered Kneser with relaxed stabilizer:** Even with non-trivial stabilizer, if the
   coset structure aligns, h/2 might still be reachable. Investigate which cosets the
   sumset lands in.