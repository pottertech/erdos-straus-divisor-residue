# Erdős-Straus Conjecture: z=my Parametrization Verification (n ≤ 10,000,000)

**Date:** 2026-08-14
**Runtime:** 213.7s (3.6 min)

## Parameters

- **N_max:** 10,000,000
- **Hard case criteria:** n ≡ 1 (mod 12), n ≢ 0 (mod 5), all odd prime factors of B₃ = n(n+3)/4 are ≡ 1 (mod 3)
- **A list:** 112 values, all ≡ 3 (mod 4), range [3, 499]
- **Success criterion:** A works iff D = n(n+A) has a divisor m with 4A | (D/m)(m+1)

## Summary Results

| Metric | Value |
|--------|-------|
| Total hard cases | 108980 |
| Solved by z=my | 108978 |
| Unsolved | 2 |
| Max A overall | 259 |
| Max A (ω=2) | 47 |
| Max A (ω≥3) | 15 |

## ω(n) Distribution

| ω(n) | Count |
|------|-------|
| 0 | 1 |
| 1 | 48937 |
| 2 | 46287 |
| 3 | 12818 |
| 4 | 933 |
| 5 | 4 |

## Minimum A Distribution

| A value | Count | Percentage |
|---------|-------|-----------|
| 3 | 28712 | 26.35% |
| 7 | 69289 | 63.58% |
| 11 | 7119 | 6.53% |
| 15 | 1624 | 1.49% |
| 19 | 921 | 0.85% |
| 23 | 740 | 0.68% |
| 31 | 315 | 0.29% |
| 43 | 32 | 0.03% |
| 47 | 101 | 0.09% |
| 55 | 32 | 0.03% |
| 59 | 24 | 0.02% |
| 67 | 6 | 0.01% |
| 71 | 22 | 0.02% |
| 79 | 13 | 0.01% |
| 83 | 2 | 0.00% |
| 91 | 2 | 0.00% |
| 95 | 8 | 0.01% |
| 99 | 2 | 0.00% |
| 103 | 1 | 0.00% |
| 107 | 4 | 0.00% |
| 111 | 2 | 0.00% |
| 115 | 2 | 0.00% |
| 135 | 1 | 0.00% |
| 143 | 1 | 0.00% |
| 147 | 1 | 0.00% |
| 179 | 1 | 0.00% |
| 259 | 1 | 0.00% |
| **Total** | **108978** | **100%** |

## Growth Comparison with Previous Results

| Bound | Max A overall | Max A (ω=2) | Max A (ω≥3) | Hard cases |
|-------|-------------|------------|------------|------------|
| n ≤ 50,000 | 59 | — | — | — |
| n ≤ 500,000 | — | 19 | 11 | — |
| n ≤ 10,000,000 | 259 | 47 | 15 | 108980 |

## Unsolved Cases

**2 unsolved case(s) found.**

| n | Is Prime | ω(n) | Factorization |
|---|----------|------|----------------|
| 1 | False | 0 |  |
| 2,521 | True | 1 | 2521 |
## Complete A Distribution (Detailed)

```
A=  3:  28712  ██████████████████████████████████████████████████
A=  7:  69289  ██████████████████████████████████████████████████
A= 11:   7119  ██████████████████████████████████████████████████
A= 15:   1624  ██████████████████████████████████████████████████
A= 19:    921  ██████████████████████████████████████████████████
A= 23:    740  ██████████████████████████████████████████████████
A= 31:    315  ██████████████████████████████████████████████████
A= 43:     32  ███████
A= 47:    101  █████████████████████
A= 55:     32  ███████
A= 59:     24  █████
A= 67:      6  ██
A= 71:     22  █████
A= 79:     13  ███
A= 83:      2  █
A= 91:      2  █
A= 95:      8  ██
A= 99:      2  █
A=103:      1  █
A=107:      4  █
A=111:      2  █
A=115:      2  █
A=135:      1  █
A=143:      1  █
A=147:      1  █
A=179:      1  █
A=259:      1  █
```

## Phase Timings

- Phase 1 (finding hard cases): 143.5s (2.4 min)
- Phase 2 (solving with z=my): 70.2s (1.2 min)
- Total runtime: 213.7s (3.6 min)

## Conclusion

The z=my parametrization with A values up to 499 fails to solve 2 hard case(s) up to n = 10,000,000.
Further investigation needed for these cases.
