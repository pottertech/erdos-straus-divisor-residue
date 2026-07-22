# Composite A Exact Recheck Report

**Goal:** Verify all composite-A first-working cases by exact T ∈ D_A((nx)²) membership.

**Composite A values:** [15, 27, 35, 39, 51, 55]

## Summary

| Metric | Count |
|--------|-------|
| Total composite-A first-working cases | 1115 |
| Exact T ∈ D_A confirms works | 1078 |
| Exact T ∈ D_A shows failure | 37 |

**All 37 failures are rescued by prime A values.** Zero unrescued cases.

## By A breakdown

| A | Total | Exact Works | Exact Fails |
|---|-------|-------------|-------------|
| 15 | 951 | 951 | 0 |
| 27 | 123 | 91 | 32 |
| 35 | 16 | 13 | 3 |
| 39 | 22 | 20 | 2 |
| 51 | 1 | 1 | 0 |
| 55 | 2 | 2 | 0 |

**A=15, A=51, A=55: 100% confirmed by exact D_A.**
**A=27: 32 Jacobi false positives** (Jacobi said m-route works, exact D_A says T ∉ D_A).
**A=35: 3 false positives.** **A=39: 2 false positives.**

## Rescue A for failures

All 37 cases where composite A failed exact recheck are rescued by a prime A value:

| Rescue A | Count |
|----------|-------|
| 31 | 21 |
| 47 | 9 |
| 43 | 3 |
| 59 | 3 |
| 71 | 1 |

No case requires A > 71 for rescue. The maximum prime A needed across all 166,011 primes remains 107 (the outlier n=8,803,369).

## Corrected coverage

After exact recheck, the true first-working-A distribution is:

| Category | Count | % |
|----------|-------|---|
| Prime-A first working (exact) | 164,933 | 99.35% |
| Composite-A first working, exact confirmed | 1,078 | 0.65% |
| Composite-A Jacobi false positive, rescued by prime A | 37 | 0.02% |
| Unresolved | 0 | 0% |

**All 166,011 primes covered. 100% exact computational coverage.**

The 37 composite-A false positives were reclassified to their prime-A rescue value. The corrected first-working-A counts shift 37 cases from composite A to prime A (mostly A=31 and A=47).

## Implications

1. **Jacobi symbol is unreliable for composite A** — it overcounts success by ~3.3% (37/1,115). This confirms Mark Kruelle's caveat that Jacobi -1 is necessary but not sufficient for QNR modulo composite A.

2. **A=15 is safe** — all 951 cases confirmed by exact D_A. This is because 15 = 3 × 5, and the Chinese Remainder Theorem decomposes D_{15} ≅ D_3 × D_5, making the Jacobi check reliable for this specific composite.

3. **A=27 is the worst offender** (32/123 = 26% false positive rate). This is because 27 = 3³, and the Jacobi symbol mod 27 doesn't capture the cubic residue structure needed for exact D_A membership.

4. **Prime A values are fully rigorous** — all prime-A first-working cases use exact Legendre symbol computation and centered criterion, not Jacobi.