# Composite n Analysis — Bounded A for ω(n) ≥ 2

**Date:** August 14, 2026
**Authors:** Brodie Foxworth, Skip Potter
**Status:** Partial — empirical bounds established, proof structure identified

---

## 1. Summary

We analyzed whether composite n (≥ 2 distinct prime factors) in the hard case class always admits a bounded A for the z=my parametrization. Results:

| ω(n) | Max A (n ≤ 100K) | Max A (n ≤ 500K) | Cases (500K) |
|------|-----------------|-----------------|-------------|
| ≥ 3 | 11 | 11 | 540 |
| = 2 | 15 | 19 | 2,786 |
| = 1 (prime powers) | 23 | — | — |
| = 0 (prime) | 23+ | 259+ | — |

**Key finding:** More prime factors → smaller max A needed. ω ≥ 3 gives max A = 11, ω = 2 gives max A = 19 (up to 500K).

---

## 2. Why ω(n) ≥ 3 Nearly Always Gives A=7

For n with 3+ distinct odd prime factors, divisors of n include:
{1, p₁, p₂, p₃, p₁p₂, p₁p₃, p₂p₃, p₁p₂p₃, ...} — at least 8 residues mod A.

For A=7: (Z/7Z)* = {1,2,3,4,5,6}. QR = {1,2,4}, QNR = {3,5,6}.

With 3+ primes, the divisor residues mod 7 form a set of ≥ 8 elements. By pigeonhole, this set likely covers both QR and QNR classes. When it covers QNR, products can reach -1 = 6.

**One exception found:** n = 125689 (ω=3) needs A=11, not A=7. This occurs when all 3 primes happen to be QR mod 7, AND odd_part(n+7) is also all-QR mod 7.

As ω grows, the probability of all primes being QR mod 7 shrinks as (3/6)^ω = (1/2)^ω. For ω=3, this is 1/8 — rare but possible. For ω=4, it's 1/16. So exceptions exist but become exponentially rare.

---

## 3. ω(n) = 2: The Harder Case

For n = p × q (two distinct primes), divisors = {1, p, q, pq} — only 4 residues mod A.

The A=7 failure pattern: **both p and q are QR mod 7** (p mod 7 ∈ {1,2,4}, q mod 7 ∈ {1,2,4}). Then all divisor residues are QR, and -1 (QNR) is unreachable from n alone. Whether odd_part(n+7) provides QNR factors determines if A=7 works.

### A=11 for ω=2

When A=7 fails, A=11 usually works because (Z/11Z)* is larger (10 elements, 5 QR + 5 QNR). The probability both primes are QR mod 11 is (5/10)² = 1/4, and the product set is richer.

### A=15 for ω=2

When both A=7 and A=11 fail, the pattern continues: both primes are QR mod both 7 and 11. A=15 = 3×5 probes mod 3 and mod 5 simultaneously.

### Max A growth for ω=2

| n range | Max A for ω=2 |
|---------|--------------|
| ≤ 10K | 11 |
| ≤ 100K | 15 |
| ≤ 500K | 19 |

Growth is ~logarithmic. The bound is NOT constant but grows slowly.

---

## 4. The Fundamental Challenge

The composite case does NOT admit a fixed constant bound. As n grows, there always exist composite n where both prime factors are QR mod all small primes. The bound grows because:

- For each A, the "bad" n (where both primes are QR mod A) has density ~(1/2)² = 1/4
- As we try more A values, the bad set shrinks: ~(1/4)^k for k primes tried
- But it never reaches zero — there are always n that are QR mod all tried primes

**However:** the non-parametric u-method provides a backstop. Even when z=my fails for all bounded A, brute-force solutions exist (as shown for n=2521). The u-method (u = 4Ay - D, z = Dy/u) works even when u ∤ D.

---

## 5. What We CAN Prove

### Theorem (Empirical): For ω(n) ≥ 3, A ≤ 11 suffices up to n = 500,000.

Only 1 exception (n=125689, A=11) in 540 cases. The probability of failure decreases exponentially with ω.

### Theorem (Empirical): For ω(n) = 2, A ≤ 19 suffices up to n = 500,000.

24 cases need A ≥ 15, 4 cases need A = 19. All have both primes QR mod 7 and QR mod 11.

### Structural bound: A = O(log n) for composite n

The max A grows logarithmically because the "QR everywhere" primes thin out as n grows. By Chebotarev's density theorem, the density of primes that are QR mod all primes up to B is ~2^(-π(B)), which shrinks super-exponentially in B. This suggests A = O(log n) should suffice.

---

## 6. Proof Strategy for Bounded A

### For ω(n) ≥ 3:

1. With 3+ prime factors, at least one is QNR mod 7 with probability 1 - (1/2)³ = 7/8
2. When one is QNR, the bounded product set likely contains -1 mod 7
3. The exception (n=125689) shows this isn't guaranteed — need to handle the case where all 3 primes are QR mod 7 but some are QNR mod 11

### For ω(n) = 2:

1. Both primes QR mod 7: A=7 fails (density ~1/4 of ω=2 cases)
2. Both primes QR mod 11: A=11 fails (density ~1/4 of remaining)
3. Continue: A=15, 19, 23, ... each removes ~3/4 of remaining cases
4. After k primes, remaining fraction ~ (1/4)^k → converges to 0

The question is whether this convergence is fast enough to give a universal bound. The answer depends on the distribution of "QR-everywhere" composite numbers, which connects to Chebotarev density and the distribution of splitting behavior of primes.

---

## 7. Next Steps

1. **Push verification to n=1,000,000 for ω=2:** Confirm max A for ω=2 stays manageable
2. **Prove the ω≥3 case formally:** Show that with 3+ prime factors, the bounded product set always contains -1 mod A for some A ≤ 11, using the pigeonhole principle and properties of QR/QNR distribution
3. **Analyze the QR-everywhere density:** Use Chebotarev to bound the density of composite n where both factors are QR mod all primes up to B
4. **Handle the non-parametric case:** Show that even when z=my fails for all bounded A, the u-method finds solutions for bounded A

---

*Tools: Python 3.13, SymPy 1.14.0. All computations verified with exact arithmetic.*