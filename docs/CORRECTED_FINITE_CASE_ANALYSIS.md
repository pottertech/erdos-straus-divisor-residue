# Corrected Finite Case Analysis — Erdős-Straus Conjecture

**Date:** August 14, 2026
**Authors:** Brodie Foxworth, Skip Potter
**Status:** Partial — mod 36 condition clarified, 141 cases require deeper analysis

---

## 1. Summary

We attempted a finite case analysis to prove A-boundedness for the Erdős-Straus conjecture on the open residue class n ≡ 1 (mod 12), n ≢ 0 (mod 5). A critical bug was found and corrected in our earlier analysis, revealing that the problem is deeper than initially expected.

**Key finding:** The correct local congruence condition is `36d | (d+B)²` (equivalently `d + 2B + B²/d ≡ 0 (mod 36)`), NOT `36 | (d+B)²` as we previously checked. These are different conditions when d does not divide (d+B)² cleanly.

---

## 2. The Bug

### What we checked (WRONG)

We verified that `(d + B)² ≡ 0 (mod 36)` for universal divisors d(A) where:
- d(3) = 4, d(7) = 2, d(11) = 6, d(15) = 4

This condition is equivalent to `d ≡ -B (mod 6)`, which we proved holds for all (n mod 36, A) pairs using simple modular arithmetic.

### What we should have checked (CORRECT)

The actual condition for a divisor d of B² to yield an integer solution is:

**d | B² AND (d + 2B + B²/d) ≡ 0 (mod 36)**

This is equivalent to **36d | (d+B)²**, which is strictly stronger than 36 | (d+B)².

### Why they differ

`(d+B)² = d² + 2Bd + B²`. Dividing by d: `(d+B)²/d = d + 2B + B²/d`.

- `36 | (d+B)²` means 36 divides the squared expression
- `36d | (d+B)²` means 36d divides it — requiring the quotient `(d+B)²/d` to also be divisible by 36

When d=4, B=2: `(d+B)² = 36`, so `36 | 36` ✅, but `36·4 = 144 ∤ 36` ❌.

### Impact

The "universal constant divisor" approach fails. No single constant d works for all n in a given residue class. The divisor must depend on the factorization of B = n(n+A)/2.

---

## 3. Corrected Mod 36 Analysis

### Residue classes

For n ≡ 1 (mod 12), the relevant residue classes are n mod 72 ∈ {1, 13, 25, 37, 49, 61} (since B mod 36 depends on n mod 72 due to the division by 2).

### B mod 36 for each (n mod 72, A)

| n mod 72 | A=3 | A=7 | A=11 | A=15 |
|----------|-----|-----|------|------|
| 1        | 2   | 4   | 6    | 8    |
| 13       | 32  | 22  | 12   | 2    |
| 25       | 26  | 4   | 18   | 32   |
| 37       | 20  | 22  | 24   | 26   |
| 49       | 14  | 4   | 30   | 20   |
| 61       | 8   | 22  | 0    | 14   |

### Working d mod 36 classes (from computation)

For each (n mod 72, A) pair, we computationally identified which d mod 36 values can satisfy the correct condition. Key observations:

- **A=3:** Working d mod 36 ∈ {4, 10, 16, 22, 28, 34} — all ≡ 4 (mod 6). But NOT all of these work for every n in the residue class (depends on factorization of B).
- **A=7:** Working d mod 36 ∈ {2, 8, 14, 20, 26, 32} — all ≡ 2 (mod 6).
- **A=11:** Working d mod 36 ∈ {0, 6, 12, 18, 24, 30, 36} — all ≡ 0 (mod 6).
- **A=15:** Working d mod 36 ∈ {4, 10, 16, 22, 28, 34} — all ≡ 4 (mod 6).

### Small constant divisors that work for SOME residue classes

| n mod 72 | A | Working small d |
|----------|---|-----------------|
| 1        | 7 | 8               |
| 1        | 15| 4               |
| 13       | 3 | 4               |
| 13       | 7 | 2               |
| 25       | 11| 18, B           |
| 25       | 15| 4               |
| 37       | 3 | 4               |
| 37       | 7 | 2               |
| 37       | 11| 12              |
| 49       | 11| 6               |
| 49       | 15| 4               |
| 61       | 3 | 4               |
| 61       | 7 | 2               |
| 61       | 11| 36, B           |

**No single A works for all 6 residue classes with a constant divisor.**

---

## 4. Computational Results (Corrected)

### Verification with correct condition (n ≤ 10,000)

- **Total cases:** 666 (n ≡ 1 mod 12, n ≢ 0 mod 5, 13 ≤ n ≤ 10,000)
- **Solved (A ≤ 99):** 525 (78.8%) — all solved with A=3
- **Unsolved (A ≤ 99):** 141 (21.2%)

### The 141 unsolved cases

All 141 unsolved cases share these properties:
1. **n ≡ 1 (mod 8)** — the parity obstruction
2. **B/2 = n(n+3)/4 has all prime factors ≡ 1 (mod 3)** — no prime ≡ 2 mod 3

This confirms the earlier finding: A=3 works iff B₃ = n(n+3)/4 has a prime factor ≡ 2 (mod 3). When ALL prime factors of B₃ are ≡ 1 (mod 3), the A=3 divisor search finds no valid d.

### First 20 unsolved cases

n = 49, 73, 169, 193, 241, 313, 361, 409, 433, 553, 601, 673, 721, 769, 793, 889, 961, 1033, 1129, 1201

### Factorization pattern

For unsolved cases, B = n(n+3)/2 = 2 × B' where B' is odd with all prime factors ≡ 1 (mod 3):

- n=49: B=1274=2×7²×13 (7≡1, 13≡1 mod 3)
- n=73: B=2774=2×19×73 (19≡1, 73≡1 mod 3)
- n=169: B=14534=2×13²×43 (13≡1, 43≡1 mod 3)
- n=193: B=18914=2×7²×193 (7≡1, 193≡1 mod 3)
- n=241: B=29402=2×61×241 (61≡1, 241≡1 mod 3)

---

## 5. What This Means

### The Hasse principle approach needs refinement

The Hasse principle for conics guarantees that local solvability (at all primes) implies global rational solvability. Our mod 36 condition checks local solvability at p=2 and p=3 (the only primes where obstructions can occur for this factored form).

However, **local solvability is necessary but not sufficient for integer solutions**. The gap between rational and integer solutions is the "integral Hasse principle" — and Bright-Loughran (2020) showed there is no Brauer-Manin obstruction, but this doesn't mean integral solutions always exist.

### The real obstruction

The 141 unsolved cases are not cases where local solvability fails — they're cases where the specific divisor-based construction fails to produce integers. The Pell-like equation may still have solutions; we just can't find them via the simple divisor approach with A ≤ 99.

### The original algorithm DID find solutions

Our earlier work (PROOF_ATTEMPT_A3.md) found that the full search algorithm (trying all A values and all t values near the F=0 threshold) found solutions for ALL 6,666 cases up to n=100,000 with A ≤ 31. This means solutions exist — the divisor-based approach just can't construct them efficiently for the 141 hard cases.

---

## 6. Next Steps

1. **Analyze the 141 unsolved cases** — determine what A and divisor work for each
2. **Find the structural pattern** — why do these cases resist the constant-divisor approach?
3. **Develop factorization-dependent divisors** — d should be chosen based on the prime factorization of B, not as a universal constant
4. **Prove the A=3 condition** — B₃ has prime factor ≡ 2 mod 3 iff A=3 works (empirically verified, needs proof)
5. **Handle the "all primes ≡ 1 mod 3" case** — this is the core difficulty

---

## 7. Comparison: Old vs New Understanding

| Aspect | Old (buggy) | New (corrected) |
|--------|-------------|----------------|
| Mod 36 condition | 36 \| (d+B)² | 36d \| (d+B)² |
| Universal divisors | d(3)=4, d(7)=2, d(11)=6, d(15)=4 | No universal constant works |
| Finite case analysis | 12 cases, all pass | 24 cases, many fail |
| Path to proof | Finite check → Hasse → done | Need factorization-dependent approach |
| A-boundedness | "Proven" with C=15 | Open — 141 cases need non-trivial divisors |

---

## 8. Lessons

1. **Check conditions carefully** — `36 | X` and `36d | X` are different when d ∤ X/36
2. **Computational verification catches bugs** — the 141 failures immediately revealed the error
3. **The problem is genuinely hard** — the n ≡ 1 (mod 8) subcase with all primes ≡ 1 mod 3 is the real obstruction

---

*Tools: Python 3.13, SymPy 1.14.0. All computations verified with exact arithmetic.*