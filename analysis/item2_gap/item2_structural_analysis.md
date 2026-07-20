# Item 2: D_A Closure / Shifted Divisor-Residue Set — Structural Analysis

## Problem Statement

For the bounded divisor-residue set $D_A$, we study the implication:

$$-1 \in D_A \implies T = -nm \in D_A$$

where $D_A$ is constructed with the full $2e_i$ bound on exponents.

The **shifted set** $D_A^{(nm)}$ uses the tight $e_i$ bound. The question: does $-1 \in D_A^{(nm)}$ suffice to guarantee $T \in D_A$?

## Summary of Findings

### Data

Scanned: 14,244 prime-A cases for primes $n \leq 100{,}000$ with $n \equiv 1 \pmod{12}$, $n \not\equiv 0 \pmod{5}$, across $A \in \{3, 7, 11, 19, 23, 31\}$.

| Category | Count | Description |
|----------|-------|-------------|
| Total prime-A cases | 14,244 | All scanned |
| Anomalous | 2,213 (15.5%) | $-1 \in D_A$ but $-1 \notin D_A^{(nm)}$ |
| T ∈ D_A (alternative path) | 1,322 (59.7%) | T reachable via full $2e_i$ bound |
| T ∉ D_A (lemma gap) | 891 (40.3%) | T NOT reachable — gap in the lemma |
| T ∈ shifted set | 0 (0%) | Confirmed: shifted set is a dead end |

### Key Structural Result

**Stabilizer type is the decisive factor:**

| Stabilizer | Total | T ∈ D_A | T ∉ D_A | Success rate |
|------------|-------|---------|---------|-------------|
| Full | 434 | 434 | 0 | 100% |
| Proper | 1,779 | 888 | 891 | 49.9% |

- **Full stabilizer:** T is ALWAYS in D_A. No gap.
- **Proper stabilizer:** Roughly 50/50 split. This is where the gap lives.

### Classification by h (order of H(A))

| h | A | Total anomalous | T ∈ D_A | T ∉ D_A | Success % |
|---|---|-----------------|---------|---------|-----------|
| 6 | 7 | 170 | 156 | 14 | 91.8% |
| 10 | 11 | 277 | 194 | 83 | 70.0% |
| 18 | 19 | 547 | 316 | 231 | 57.8% |
| 22 | 23 | 533 | 406 | 127 | 76.2% |
| 30 | 31 | 686 | 250 | 436 | 36.4% |

**h=30 (A=31) is the bottleneck:** 436 gap cases, only 36.4% success rate.

### Witness Path Structure (1,322 cases with T ∈ D_A)

| Structure | Count | % |
|-----------|-------|---|
| Single overflow (one prime exceeds $e_i$) | 1,097 | 83.0% |
| Double overflow (two primes exceed) | 213 | 16.1% |
| Multi overflow (3+ primes exceed) | 12 | 0.9% |

- **Excess magnitude:** 1,536 of 1,559 prime-instances exceed by exactly +1; 22 by +2; 1 by +3.
- **0/1,322 cases use the $(-1) \cdot nm$ path.** All use genuinely alternative divisor paths.
- The shifted set $D_A^{(nm)}$ is the wrong tool: it requires factoring $T = (-1) \cdot nm$, which overflows. The direct construction finds different exponent vectors $(b_1, \ldots, b_k)$ with $0 \leq b_i \leq 2e_i$ that reach $\text{dlog}(T) = h/2 + \text{dlog}(nm) \pmod{h}$ without going through $-1$.

### Accessible Prime Count Distribution

| # Primes | Count | % |
|----------|-------|---|
| 3 | 417 | 31.5% |
| 4 | 751 | 56.8% |
| 5 | 149 | 11.3% |
| 6 | 5 | 0.4% |

## Kneser's Theorem Analysis

### Trivial Stabilizer Bound

Kneser's theorem (trivial stabilizer): $|D_A| \geq \min(h, \sum(2e_i + 1) - k + 1)$.

| Coverage | Count | % |
|----------|-------|---|
| Bound ≥ h (full coverage) | 16 | 1.8% |
| Bound < h (partial) | 875 | 98.2% |

**Kneser alone fails for 875/891 gap cases.**

### With Actual Stabilizer

Stabilizer sizes in gap cases:

| Stabilizer size | Count |
|-----------------|-------|
| 1 (trivial) | 698 |
| 3 | 77 |
| 5 | 116 |

Kneser + stabilizer: 150/891 cases covered. Still far from sufficient.

### Per-h Gap Analysis

| h | Gap cases | Kneser covers | Avg deficit | Avg |D_A| | Coverage % |
|---|-----------|-------------|-------------|---------|------------|
| 6 | 14 | 14 | 0.0 | 5.0/6 | 83.3% |
| 10 | 83 | 2 | 2.8 | 9.0/10 | 90.0% |
| 18 | 231 | 0 | 10.0 | 15.4/18 | 85.4% |
| 22 | 127 | 0 | 13.8 | 19.5/22 | 88.6% |
| 30 | 436 | 0 | 21.8 | 22.0/30 | 73.4% |

**Key observations:**
- h=6: Kneser covers all 14 gap cases (but D_A still misses T due to stabilizer structure)
- h=10: Average |D_A| = 9/10, just 1 element short — very close
- h=18, 22: ~85-89% coverage, moderate deficit
- h=30: Only 73.4% coverage, large deficit (21.8 avg) — the hard core

### Deficit Distribution

| Deficit | Count |
|---------|-------|
| 1 | 26 |
| 3 | 34 |
| 5 | 26 |
| 7 | 18 |
| 9 | 72 |
| 11 | 149 |
| 13 | 62 |
| 15 | 68 |
| 17 | 18 |
| 19 | 30 |
| 21 | 112 |
| 23 | 210 |
| 25 | 50 |

The deficits are large and concentrated at h=30 (deficits 21-25).

## Why the Shifted Set Fails

The shifted set $D_A^{(nm)}$ constructs $T = (-1) \cdot nm$ by:
1. Finding $-1 \in D_A$ via witness $(a_1, \ldots, a_k)$ with $\sum a_i \cdot s_i \equiv h/2 \pmod{h}$
2. Multiplying by $nm$: new exponents $(a_1 + e_1, \ldots, a_k + e_k)$

This fails when $a_i + e_i > 2e_i$ for some prime $p_i$ (overflow). In all 1,322 anomalous cases where T ∈ D_A, the standard $(-1) \cdot nm$ path overflows, but a DIFFERENT exponent vector $(b_1, \ldots, b_k)$ reaches $\text{dlog}(T)$ directly.

The correct condition is:

> $T \in D_A$ whenever the bounded sumset $\{\sum b_i \cdot s_i : 0 \leq b_i \leq 2e_i\}$ contains $h/2 + \text{dlog}(nm) \pmod{h}$

This is WEAKER than requiring $-1 \in D_A^{(nm)}$, because it doesn't require factoring $T = (-1) \cdot nm$. The sumset with bound $2e$ can contain the target even when the sumset with bound $e$ doesn't contain $h/2$.

## The 891 Gap Cases

All 891 gap cases share:
- **Proper stabilizer** (never full)
- $T \notin D_A$ (target not reachable even with full $2e_i$ bounds)
- Kneser's theorem insufficient (deficit > 0 for 875 cases)

### Distribution

| A | h | Gap cases | % of all gaps |
|---|---|-----------|---------------|
| 7 | 6 | 14 | 1.6% |
| 11 | 10 | 60 | 6.7% |
| 19 | 18 | 231 | 25.9% |
| 23 | 22 | 127 | 14.3% |
| 31 | 30 | 459 | 51.6% |

A=31 (h=30) accounts for over half the gap cases.

## Conclusions

1. **Shifted set $D_A^{(nm)}$ is a dead end** — confirmed: 0 cases where T ∈ shifted set for anomalous cases.

2. **Full stabilizer → always works** — 434 cases, 100% success. When the stabilizer of $nm$ in $H(A)$ is the full group, T is always reachable.

3. **Proper stabilizer → 50/50 split** — the gap lives here. The 888 successful cases use alternative exponent vectors; the 891 failures cannot reach T within the $2e_i$ bounds.

4. **Kneser's theorem is insufficient** — only 16/891 gap cases covered by trivial-stab Kneser, 150/891 with actual stabilizer.

5. **The gap is concentrated at h=30 (A=31)** — 436 gap cases with average coverage 73.4%.

## Next Steps

The 891 gap cases require arguments beyond Kneser:

1. **Per-h finite case analysis** — only 5 values of h (6, 10, 18, 22, 30). Each can be studied as a finite combinatorial problem in $\mathbb{Z}/h\mathbb{Z}$.

2. **Green-Ruzsa theorem** — generalizes Kneser for composite-order groups; may give tighter bounds for the specific stabilizer structures observed (stab sizes 1, 3, 5).

3. **Quotient group argument** — for stabilizer $H_0$ of size $d$, work in $\mathbb{Z}/(h/d)\mathbb{Z}$. If the quotient sumset covers the target coset, then T ∈ D_A.

4. **Direct construction for h=30** — the bottleneck case. With stabilizer sizes 1, 3, 5, the quotient groups are $\mathbb{Z}/30$, $\mathbb{Z}/10$, $\mathbb{Z}/6$. Each is small enough for exhaustive analysis.

5. **Relax to almost-covering** — if T is not in D_A but D_A covers >70% of the group, can a different choice of A (from the covering set) handle the missing cases?

## Files

- `analysis/classify_anomalous.py` — Step 1 classification script
- `analysis/classified_anomalous.json` — Full classified results
- `analysis/kneser_gap_analysis.py` — Step 2 Kneser analysis script
- `analysis/kneser_gap_analysis.json` — Kneser gap results
- `analysis/shifted_set_analysis.py` — Original shifted-set analysis
- `analysis/shifted_set_analysis.json` — Original results
- `results/anomalous_cases_verified.json` — 61 verified cases (n ≤ 1000)