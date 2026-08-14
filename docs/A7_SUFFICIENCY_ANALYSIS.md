# A=7 Sufficiency Analysis — Erdős-Straus Conjecture

**Date:** August 14, 2026
**Authors:** Brodie Foxworth, Skip Potter
**Status:** Structural obstruction identified; A=7 not sufficient. Unified framework found.

---

## 1. Summary

We attempted to prove that A=7 suffices for all "hard cases" of the Erdős-Straus conjecture (n ≡ 1 mod 12, n ≢ 0 mod 5, all prime factors of B₃ = n(n+3)/4 ≡ 1 mod 3). 

**Result:** A=7 is NOT sufficient. It solves 156/200 (78%) of hard cases up to n=10,000. The obstruction has two types, both rooted in the interaction between the mod 4 and mod 7 conditions.

**Key structural finding:** The A=7 condition `28 | (D/m)(m+1)` for some divisor m of D = n(n+7) fails for two distinct reasons, both involving the impossibility of simultaneously satisfying the mod 4 and mod 7 sub-conditions.

---

## 2. The A=7 Condition Decomposed

For A=7, x = (n+7)/4, and we need m | D = n(n+7) such that:

**28 | (D/m)(m+1)**

This decomposes as:
- **Mod 4:** 4 | (D/m)(m+1)
- **Mod 7:** 7 | (D/m)(m+1)

### Mod 7 condition

Since n ≡ 1 (mod 12) implies n is odd, and n+7 is even. For the hard cases, gcd(n, 7) = 1 (verified: all 200 hard cases have 7 ∤ n). So 7 ∤ D = n(n+7).

Since 7 ∤ D, for any divisor m of D, 7 ∤ (D/m). So the mod 7 condition reduces to:

**7 | (m+1), i.e., m ≡ 6 (mod 7)**

Since 6 is a **quadratic non-residue** (QNR) mod 7 (QRs are {1, 2, 4}), a divisor m ≡ 6 mod 7 exists only if D has at least one prime factor that is QNR mod 7 (i.e., p ≡ 3, 5, or 6 mod 7).

### Mod 4 condition

D = n(n+7) where n is odd and n+7 is even. Let v₂ = v₂(n+7) = v₂(D).

For a divisor m of D:
- If m is **even**: m+1 is odd, so v₂((D/m)(m+1)) = v₂(D/m) = v₂(D) - v₂(m). Need v₂(D) - v₂(m) ≥ 2.
- If m is **odd**: m+1 is even, so v₂((D/m)(m+1)) = v₂(D) + v₂(m+1). Need v₂(D) + v₂(m+1) ≥ 2. Since v₂(D) ≥ 1 (as n+7 is even), this requires v₂(m+1) ≥ 1 when v₂(D) = 1, or is automatic when v₂(D) ≥ 2.

---

## 3. Two Types of Obstruction

### Type 1: All primes of D are QR mod 7 (30/44 failures, 68%)

When every prime factor of D = n(n+7) is a quadratic residue mod 7 (p ≡ 1, 2, or 4 mod 7), ALL divisors of D are QR mod 7. No divisor m ≡ 6 mod 7 can exist. The mod 7 condition is unsatisfiable.

**Examples:** n = 109, 1129, 1201, 1369, 1549, 1789, 1849, 2221, 2521, 2689, ...

**Characteristic:** D mod 7 ∈ {1, 2, 4} (all QR), and every prime factor p of D has p mod 7 ∈ {1, 2, 4}.

### Type 2: QNR mod 7 factors exist but only in even divisors (14/44 failures, 32%)

D has QNR mod 7 prime factors, so divisors m ≡ 6 mod 7 DO exist — but ALL of them are **even**. Since the QNR factors come from n (odd) and n+7 ≡ n mod 7, the only way to get m ≡ 6 mod 7 is to include enough QNR factors from n. But n is odd, so divisors of n are odd. The even part of D comes from n+7.

The key: to get m ≡ 6 mod 7 with m **odd**, we need d₁ × d₂ ≡ 6 mod 7 where d₁ | n (odd) and d₂ | odd_part(n+7) (odd). But for these 14 cases, **6 is not achievable as a product of odd divisors** — the QNR residues (3, 5) combine with available QR residues but never produce 6 among odd divisors.

Since all m ≡ 6 mod 7 are even, they all consume 2-adic valuation from D. With v₂(D) = 2 or 3, the remaining v₂(D/m) = 1, which is insufficient for the mod 4 condition (needs ≥ 2 when m+1 is odd).

**Examples:** n = 61, 1069, 1213, 1741, 2161, 2833, 3169, 4429, 4513, 5521, 7309, 7789, 7933, 9133

**Characteristic:** D has QNR mod 7 factors, but 6 ∉ {d₁ × d₂ mod 7 : d₁ | n, d₂ | odd_part(n+7)}.

---

## 4. Complete Failure Classification (n ≤ 10,000)

| Type | Count | Mechanism | A=7 condition |
|------|-------|-----------|---------------|
| Success | 156 | D has QNR mod 7 factor AND odd m ≡ 6 mod 7 exists with mod 4 satisfiable | ✅ |
| Type 1 | 30 | All primes of D are QR mod 7 → no m ≡ 6 mod 7 | ❌ mod 7 |
| Type 2 | 14 | QNR factors exist but only in even divisors → mod 4 fails | ❌ mod 4 |

---

## 5. Higher A Values Rescue

For the 44 A=7 failures, higher A values solve all but one:

| A | New cases solved | Cumulative | Mechanism |
|---|-----------------|------------|----------|
| 7 | 156 | 156 (78.0%) | z=my parametrization |
| 11 | 32 | 188 (94.0%) | Different prime (11), different QR/QNR structure |
| 15 | 3 | 191 (95.5%) | Composite A = 3×5, mixed conditions |
| 19 | 5 | 196 (98.0%) | Prime 19 ≡ 3 mod 4, new QR structure |
| 23 | 3 | 199 (99.5%) | Prime 23 ≡ 3 mod 4 |
| 31+ | 0 | 199 | n=2521 remains unsolved by z=my |

**n=2521** (prime) is the sole exception: requires A=23 with a non-parametric solution (z/y not integer).

### Why higher A works

For A=p (prime, p ≡ 3 mod 4), the condition is m ≡ -1 (mod p). Since p ≡ 3 mod 4, -1 is a QNR mod p. So we need D_p = n(n+p) to have a QNR mod p factor.

The key: **different primes p probe different quadratic residue structures**. A case where all primes of n(n+7) are QR mod 7 may have QNR factors mod 11, mod 19, mod 23, etc. The Chinese Remainder Theorem ensures that for any finite set of primes, there exist n where all factors are QR mod all of them — but these become increasingly rare.

---

## 6. Updated A-Boundedness Status

| n range | Max A needed | Method |
|---------|-------------|--------|
| n ≤ 1,000 | 23 | z=my + brute force |
| n ≤ 10,000 | 23 | z=my + brute force (n=2521 exception) |
| n ≤ 100,000 | 31 | Full algorithm search (earlier work) |

### Theoretical status

- **A=3:** Proven iff condition (B₃ has prime factor ≡ 2 mod 3). Covers ~79%.
- **A=7:** NOT sufficient. Two obstructions identified (Type 1: QR mod 7, Type 2: even-only QNR divisors).
- **A ≤ 31:** Empirically sufficient up to n=100,000. No proof.
- **A-boundedness:** Still OPEN.

---

## 7. Proof Strategy: The QR Sieve

The analysis suggests a proof approach:

1. **For each prime p ≡ 3 (mod 4)** (7, 11, 19, 23, 31, 43, 47, ...), A=p works iff D_p = n(n+p) has a QNR mod p factor AND the mod 4 condition is satisfiable.

2. **The obstruction for each A=p** is that all prime factors of n(n+p) are QR mod p. This is a condition on n mod p and the factorization of n.

3. **Sieving across primes:** For n to fail ALL A ≤ B, we need n(n+A) to have all-QR factorizations for every A in {3, 7, 11, 15, 19, 23, 31, ...}. As B grows, this becomes increasingly restrictive — but proving it's impossible for all n requires showing the sieve terminates.

4. **Density argument:** The density of n where all prime factors of n(n+p) are QR mod p is roughly (1/2)^(ω(D_p)) where ω is the number of distinct prime factors. For large n, ω grows, so the density shrinks. But density arguments don't prove universality.

5. **The mod 4 wild card:** Even when the mod 7 (or mod p) condition is satisfiable, the mod 4 condition adds an extra constraint. The interaction between 2-adic and p-adic structure is the core difficulty.

---

## 8. Next Research Directions

1. **Prove the QR obstruction is the only obstruction for A=p prime:** Show that when D_p has a QNR mod p factor, an odd divisor m ≡ -1 mod p always exists (or characterize when it doesn't).

2. **Quantify the mod 4 + mod p interaction:** For Type 2 failures, characterize exactly when the 2-adic valuation is insufficient.

3. **Chinese Remainder sieve:** Show that for any n, there exists a bounded A such that n(n+A) has a QNR mod A factor with sufficient 2-adic structure. This would prove A-boundedness.

4. **Handle n=2521:** Understand why this prime resists all z=my parametrizations and whether it's truly exceptional or the first of infinitely many.

5. **Extend verification to n=1,000,000:** Confirm A ≤ 31 (or find the true bound) with the corrected algorithm.

---

## 9. Files

- `141_HARD_CASES_ANALYSIS.md` — Complete analysis of all hard cases up to 10,000
- `CORRECTED_FINITE_CASE_ANALYSIS.md` — Documents the mod 36 bug and corrected condition
- `A7_SUFFICIENCY_ANALYSIS.md` — This file

---

*Tools: Python 3.13, SymPy 1.14.0. All computations verified with exact arithmetic.*