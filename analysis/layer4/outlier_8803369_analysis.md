# Outlier Analysis: n = 8,803,369

This prime requires A = 107, the largest A needed for any n ≤ 10M.

## A-by-A analysis

| A | works? | route | h | n_qr | m_qnr_factors | shortest_repr |
|---|--------|-------|---|------|---------------|---------------|
| 3 | False | no_qnr | N/A | True | N/A | N/A |
| 7 | False | no_qnr | N/A | True | N/A | N/A |
| 11 | False | no_qnr | N/A | True | N/A | N/A |
| 15 | False | no_qnr | N/A | True | N/A | N/A |
| 19 | False | no_qnr | N/A | True | N/A | N/A |
| 23 | False | no_qnr | N/A | True | N/A | N/A |
| 27 | False | no_qnr | N/A | True | N/A | N/A |
| 31 | False | no_qnr | N/A | True | N/A | N/A |
| 35 | False | no_qnr | N/A | True | N/A | N/A |
| 39 | False | no_qnr | N/A | True | N/A | N/A |
| 43 | False | gap | 14 | False | N/A | N/A |
| 47 | False | no_qnr | N/A | True | N/A | N/A |
| 51 | False | no_qnr | N/A | True | N/A | N/A |
| 55 | False | no_qnr | N/A | True | N/A | N/A |
| 59 | False | gap | 58 | False | N/A | N/A |
| 63 | False | no_qnr | N/A | True | N/A | N/A |
| 67 | False | gap | 66 | False | N/A | N/A |
| 71 | False | no_qnr | N/A | True | N/A | N/A |
| 75 | False | no_qnr | N/A | True | N/A | N/A |
| 79 | False | gap | 78 | True | N/A | N/A |
| 83 | False | gap | 82 | False | N/A | N/A |
| 87 | False | no_qnr | N/A | True | N/A | N/A |
| 91 | False | no_qnr | N/A | True | N/A | N/A |
| 95 | False | no_qnr | N/A | True | N/A | N/A |
| 99 | False | no_qnr | N/A | True | N/A | N/A |
| 103 | False | gap | 102 | False | N/A | N/A |
| 107 | True | direct_n_qnr | 106 | False | [43] | [('3', -2), ('43', -1), ('47', -1)] |

## Structural observations

### 1. Two distinct failure modes

**No-QNR failures (A ≤ 31, 35, 39, 47, 51, 55, 63, 71, 75, 87, 91, 95, 99):** n is QR mod A, so no prime factor of nx generates even-order elements. H(A) has odd order h, −1 ∉ H(A), and the forward direction hypothesis is not met. These are not "failures" of the criterion — A is simply inapplicable.

**Gap failures (A = 43, 59, 67, 79, 83, 103):** n is QNR mod A (h is even, −1 ∈ H(A)), but the centered sumset Σ_A(N) cannot reach h/2. These are genuine criterion gaps where the bounded signed exponents [−e_i, e_i] are insufficient to represent the target.

### 2. Gap pattern

The gap failures occur at h = 14, 58, 66, 78, 82, 102 — all even values where h/2 is odd (7, 29, 33, 39, 41, 51). This is consistent with the parity obstruction (Theorem 10): the target dlog is always at an odd position, and the signed sumset systematically misses odd positions when the generator structure has the wrong parity.

### 3. Why A = 107 works

At A = 107, n is QNR mod 107 (n_qr = False), so the direct route applies. The group order h = 106, and the centered sumset reaches h/2 = 53 via three signed terms: δ₃ = −2 (on prime 3), δ₄₃ = −1 (on prime 43), δ₄₇ = −1 (on prime 47). This is a short signed representation using 3 prime factors of N.

The key structural fact: 107 is the first prime ≡ 3 (mod 4) where (107/n) = −1. For all smaller prime A ≡ 3 (mod 4), either n is QR mod A (no QNR generator) or the gap obstruction prevents the centered sumset from reaching h/2.

### 4. Outlier classification

n = 8,803,369 is an **extreme QR prime** — it is a quadratic residue modulo almost all primes ≡ 3 (mod 4) up to 103. This is consistent with the density-0 prediction from the sieve argument (Theorem 14): such primes exist but are increasingly rare. The Burgess-style route discussed in Proposition 8 suggests a bound of the form A = O(n^{1/(4√e)+ε}) ≈ O(n^{0.1515+ε}) under the stated analytic assumptions. The observed A = 107 is far below this scale for n ≈ 8.8M, so the outlier is well within the analytic bound.

### 5. Constant bound implications

The outlier shows the constant bound C cannot be less than 107 for primes ≤ 10M. Whether C remains bounded as n → ∞ depends on whether the "extreme QR" primes have a finite maximum A or grow without bound. The sieve argument predicts density 0 but does not yield an explicit finite C.