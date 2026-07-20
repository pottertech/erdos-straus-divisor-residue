# Item 2 Step 3: Quotient Group Analysis — The Structural Obstruction

## Setup

For the 193 non-trivial-stabilizer gap cases (out of 891 total gap cases), we analyzed the quotient group H(A)/S where S is the multiplicative stabilizer of D_A.

## The Core Finding

**In all 193 cases, D_A covers every coset of S in H(A) except the one containing T.**

| Property | Count / 193 |
|----------|-------------|
| -1 ∈ D_A | 193 (100%) |
| T ∉ D_A | 193 (100%) |
| -1's coset covered | 193 (100%) |
| T's coset covered | 0 (0%) |
| nm ∈ stabilizer S | 0 (0%) |

## Why This Happens

The mechanism is:

1. **-1 ∈ D_A** (premise): -1 is reachable via bounded exponents. ✓
2. **nm ∉ S** (the stabilizer of D_A): nm lies outside the stabilizer in ALL 193 cases.
3. **T = -1 · nm**: Since nm shifts the coset, T lands in a DIFFERENT coset than -1.
4. **D_A covers -1's coset but not T's coset**: The sumset D_A is invariant under S (by definition of stabilizer), so it covers entire cosets. It covers -1's coset (since -1 ∈ D_A) but does NOT cover T's coset.

## The Stabilizer Structure

| Stab size | Quotient | Cases | D_A cosets covered | Missing coset |
|-----------|----------|-------|---------------------|---------------|
| 3 | Z/6 | 14 | 5/6 | T's coset |
| 3 | Z/10 | 63 | 9/10 | T's coset |
| 5 | Z/6 | 116 | 5/6 | T's coset |

In every case, D_A covers exactly |quotient| - 1 cosets, missing only T's coset.

## Interpretation

This is NOT a bound-size problem. D_A is large enough to cover the entire group (Kneser bound often ≥ h). The issue is that D_A is *structured*: it's invariant under the stabilizer S, so it covers entire S-cosets. The target T is always in the ONE uncovered coset.

The obstruction is: **nm is not in the stabilizer of D_A**, so multiplying -1 by nm moves to a coset that D_A doesn't cover. The shifted set D_A^(nm) fails precisely because it tries to multiply by nm, which leaves the covered region.

## Implications for the Proof

The quotient analysis shows:

1. **The shifted set approach is fundamentally flawed** — not just too weak, but structurally wrong. The multiplication by nm moves out of the covered cosets.

2. **The 193 non-trivial-stab cases need a DIFFERENT A** — since D_A for this particular A cannot reach T, the only way to cover these n values is via a different choice of A from the covering set {3, 7, 11, 19, 23, 31}.

3. **The 698 trivial-stab cases** are different — there, the stabilizer is trivial so the quotient argument doesn't apply, and the gap is about bound sizes (Kneser deficit).

4. **For a full proof**, we need to show that for every n where one A gives a gap, another A from the covering set succeeds. The covering set property is what closes the gap — not a single-A argument.

## Comparison: Full vs Proper Stabilizer

| Stabilizer type | Total anomalous | T ∈ D_A | T ∉ D_A | Mechanism |
|-----------------|----------------|---------|---------|-----------|
| Full | 434 | 434 (100%) | 0 | nm ∈ S, so T stays in -1's coset |
| Proper | 1,779 | 888 (49.9%) | 891 (50.1%) | nm ∉ S, T moves to uncovered coset |

**Full stabilizer → always works** because nm IS in the stabilizer, so T = -1·nm stays in the same coset as -1, which IS covered.

**Proper stabilizer → 50/50 split** because nm is NOT in the stabilizer. Whether T's coset is covered depends on whether D_A happens to reach that other coset — and for the 891 gap cases, it doesn't.

## Next Steps

1. **For the 193 non-trivial-stab cases**: verify that another A from the covering set handles each n. If so, the proof is: "the covering set property ensures at least one A works."

2. **For the 698 trivial-stab cases**: these have no stabilizer structure to exploit. Need per-h analysis (h ∈ {10, 18, 22, 30}) with direct combinatorial arguments.

3. **Unify**: show that the covering set {3, 7, 11, 19, 23, 31} (or an extended set) covers all primes n ≡ 1 mod 12, n ≢ 0 mod 5 up to the verification bound, with each n having at least one A where T ∈ D_A.

## Files

- `analysis/quotient_gap_analysis.py` — Initial quotient analysis
- `analysis/quotient_gap_analysis.json` — Results
- `analysis/quotient_deep_analysis.py` — Deep dive into structural obstruction
- `analysis/quotient_deep_analysis.py` output — Multiplicative verification