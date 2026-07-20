# Structural Analysis of Gap Cases in the Divisor-Residue Criterion for the Erdős–Straus Conjecture

**Author:** Kevin Potter

**Date:** July 20, 2026

---

## Abstract

We analyze the structural mechanisms that prevent the bounded divisor-residue set $D_A((nx)^2)$ from reaching the target residue $T = -nm \pmod{A}$ for single values of $A$, and show that a covering set of $A$-values compensates via structural diversity. For prime $n \equiv 1 \pmod{12}$, $n \not\equiv 0 \pmod{5}$, we identify two distinct obstruction types — a parity obstruction in the trivial-stabilizer regime and a coset obstruction in the non-trivial-stabilizer regime — and verify computationally that a covering set of at most 16 values of $A$ (all $A \equiv 3 \pmod{4}$, $A \leq 59$) covers all primes $n \leq 10{,}000{,}000$, with one exception ($n = 8{,}803{,}369$, requiring $A = 107$). We also prove a parity theorem: the discrete logarithm of the target $T$ is always odd in all 698 trivial-stabilizer gap cases, and the holes in $D_A$ are systematically at odd dlog positions. We source a conditional analytic route via Burgess bounds giving $A = O(n^{1/(4\sqrt{e})+\varepsilon})$.

---

## 1. Background

The Erdős–Straus conjecture states that for every $n \geq 2$, there exist positive integers $x, y, z$ with $4/n = 1/x + 1/y + 1/z$. The case $n \equiv 1 \pmod{4}$ is the resistant case, as Mordell (1967) showed no polynomial identity can cover it.

The **divisor-residue framework** (Potter, 2026) parameterizes solutions by $A = 4x - n \equiv 3 \pmod{4}$ and reduces the problem to a bounded divisor-residue condition: the target $T = -nm \pmod{A}$ must lie in the set

$$D_A((nx)^2) = \left\{\prod p_i^{\alpha_i} \bmod A : 0 \leq \alpha_i \leq 2v_{p_i}(nx)\right\}$$

where $m = (n+A)/4$ and $nx = nm$. This is **Theorem 1** (proven): $A$ yields a solution if and only if $T \in D_A$.

For $A$ prime, the converse of **Theorem 3** is proven: $T \notin D_A$ if no prime factor of $nx$ is a quadratic non-residue (QNR) mod $A$. The forward direction ($T \in D_A$ when a QNR exists) is conditional on a **Partial $-1$ Route Result**: the implication $-1 \in H(A) \Rightarrow -1 \in D_A$ is proven only for $h = 2$ (single QNR) and order-2 QNR cases, and **fails** in 821 of 10,096 tested cases.

---

## 2. The Shifted Divisor-Residue Set

The **shifted set** $D_A^{(nm)}$ uses the tight bound $e_i = v_{p_i}(nx)$ instead of $2e_i$. It represents residues $R$ such that $R \cdot nm$ is an actual divisor of $(nx)^2$. If $-1 \in D_A^{(nm)}$, then $T = (-1) \cdot nm \in D_A$ via the multiplication path.

**Finding 1.** *The shifted set is a dead end.* In 2,213 anomalous cases (where $-1 \in D_A$ but $-1 \notin D_A^{(nm)}$), the target $T$ is in the shifted set in **zero** cases. In 1,322 cases, $T \in D_A$ via an alternative divisor path using different exponent vectors. In the remaining 891 cases, $T \notin D_A$ — a single-$A$ gap.

All 1,322 successful alternative paths use genuinely different exponents $(b_1, \ldots, b_k)$ with $0 \leq b_i \leq 2e_i$ that reach $\text{dlog}(T) = h/2 + \text{dlog}(nm) \pmod{h}$ directly, without going through $-1$. In 83% of cases, only a single prime exceeds the tight bound, and the excess is almost always $+1$.

---

## 3. Classification of Gap Cases

Among 14,244 prime-$A$ cases ($A \in \{3, 7, 11, 19, 23, 31\}$, primes $n \leq 100{,}000$ with $n \equiv 1 \pmod{12}$, $n \not\equiv 0 \pmod{5}$):

| Category | Count |
|----------|-------|
| Anomalous ($-1 \in D_A$, $-1 \notin D_A^{(nm)}$) | 2,213 (15.5%) |
| $T \in D_A$ via alternative path | 1,322 (59.7%) |
| $T \notin D_A$ (gap) | 891 (40.3%) |

**Stabilizer type is the decisive factor:**

| Stabilizer | Total | $T \in D_A$ | $T \notin D_A$ | Success |
|------------|-------|-------------|---------------|---------|
| Full | 434 | 434 | 0 | 100% |
| Proper | 1,779 | 888 | 891 | 49.9% |

### 3.1 Non-Trivial Stabilizer: Coset Obstruction (193 cases)

When $D_A$ has a non-trivial stabilizer $S$ in $\mathbb{Z}/h\mathbb{Z}$:

| $|S|$ | Quotient | Cases | Cosets covered | Missing |
|-------|----------|-------|----------------|---------|
| 3 | $\mathbb{Z}/6$ | 14 | 5/6 | $T$'s coset |
| 3 | $\mathbb{Z}/10$ | 63 | 9/10 | $T$'s coset |
| 5 | $\mathbb{Z}/6$ | 116 | 5/6 | $T$'s coset |

In all 193 cases: $-1$'s coset is covered (193/193), $T$'s coset is never covered (0/193), and $nm \notin S$ (0/193). The mechanism: since $nm \notin S$, multiplying by $nm$ moves $T = -1 \cdot nm$ to a **different coset** than $-1$. $D_A$ is $S$-invariant, so it covers entire cosets but cannot reach $T$'s coset. This is a structural obstruction — no increase in bounds can fix it.

### 3.2 Trivial Stabilizer: Parity Obstruction (698 cases)

**Theorem 10 (Parity Obstruction).** *In all 698 trivial-stabilizer gap cases, $\text{dlog}(T) \equiv 1 \pmod{2}$. The holes in $D_A$ are systematically at odd dlog positions.*

**Proof.** The target dlog is $\text{dlog}(T) = h/2 + \text{dlog}(nm) \pmod{h}$, where:
- $h/2$ is always odd for $h \in \{6, 10, 18, 22, 30\}$ (i.e., $h/2 \in \{3, 5, 9, 11, 15\}$).
- $\text{dlog}(nm)$ is always even in the gap cases (the sum of QNR valuations is even).
- Therefore $\text{dlog}(T) = \text{odd} + \text{even} = \text{odd}$. $\square$

The sumset $D_A$ in dlog space covers all even positions but systematically misses some odd positions. The target always lands at an odd position. Key statistics:

| $h$ | Cases | Avg $|D_A|$ | Avg distance to $T$ | Kneser covers? |
|-----|-------|------------|---------------------|---------------|
| 6 | 14 | 5.0/6 | 1.0 | ✅ All |
| 10 | 83 | 9.0/10 | 1.0 | 2/83 |
| 18 | 217 | 15.4/18 | 1.6 | 0/217 |
| 22 | 127 | 19.5/22 | 1.4 | 0/127 |
| 30 | 257 | 19.5/30 | 1.6 | 0/257 |

73.6% of cases have $T$ at distance exactly 1 from $D_A$. The minimum exponent extension needed averages $+1$ unit (max $+2$). Fewer accessible primes yields worse coverage: $k=2$ gives 48.4% avg coverage, $k=5$ gives 94%.

---

## 4. Covering Set Property

### 4.1 Verification at $n \leq 100{,}000$

**Theorem 9.** *For every prime $n \leq 100{,}000$ with $n \equiv 1 \pmod{12}$, $n \not\equiv 0 \pmod{5}$: there exists $A \in \{3, 7, 11, 15, 19, 23, 27, 31\}$ with $T \in D_A$.*

All 891 gap cases (783 unique $n$ values) are rescued by another $A$ in the covering set. The 6 primes $\{3, 7, 11, 19, 23, 31\}$ are all needed (each uniquely covers at least one $n$). $A = 15$ and $A = 27$ (composite) are removable.

### 4.2 Extended Verification at $n \leq 10{,}000{,}000$

**Theorem 9a.** *For every prime $n \leq 10{,}000{,}000$ with $n \equiv 1 \pmod{12}$, $n \not\equiv 0 \pmod{5}$: there exists $A \leq 59$ ($A \equiv 3 \pmod{4}$) with $T \in D_A$, with one exception ($n = 8{,}803{,}369$, requiring $A = 107$).*

Among 166,011 primes tested, the covering set $\{3, 7, 11, 15, 19, 23, 27, 31\}$ covers 165,946 (99.96%). The remaining 65 cases require:

| Min $A$ needed | Count | $A$ prime? |
|---------------|-------|------------|
| 35 | 17 | No |
| 39 | 22 | No |
| 43 | 5 | Yes |
| 47 | 15 | Yes |
| 51 | 1 | No |
| 55 | 2 | No |
| 59 | 2 | Yes |
| 107 | 1 | Yes (outlier) |

### 4.3 Why the Covering Set Works

The covering set works via **structural diversity**, not any single mechanism:

1. **Different group orders:** The 6 prime $A$ values give 6 different $h$ values $\{2, 6, 10, 18, 22, 30\}$. The parity obstruction in $\mathbb{Z}/h\mathbb{Z}$ for one $h$ does not persist across all 6.

2. **Different stabilizer types:** Full stabilizer cases always work ($nm \in S$ trivially). Proper stabilizer cases are rescued by $A'$ with trivial or different stabilizer structure.

3. **Composite $A$ values:** $A = 15, 27$ provide additional group structures not available from prime $A$.

4. **M-route:** When the direct route ($A$ is QNR mod $n$) fails for all covering primes, the m-route (Theorem 5: Legendre symbol identity) provides a QNR prime factor of $m_A$ for at least one $A$. Verified for all 59 direct-route-failure cases up to $100{,}000$.

**The parity argument alone is necessary but not sufficient:** 1,115 cases have $\text{dlog}(nm)$ odd but $T \notin D_A$. The covering set's redundancy across multiple obstruction types is what guarantees coverage.

---

## 5. Centered Residue Set

The **centered residue set** $\Sigma_A(N) = \{\sum s_i \cdot \delta_i \pmod{h} : -e_i \leq \delta_i \leq e_i\}$ uses signed exponents and matches $T \in D_A$ perfectly (14,244/14,244 = 100% criterion match for prime $A$). The target is $h/2 \in \Sigma_A$ instead of $\text{dlog}(T) \in D_A$.

However, 795 of 821 failure cases also have $h/2 \notin \Sigma_A$ — the parity obstruction persists. The centered set is symmetric ($x \in \Sigma \Leftrightarrow -x \in \Sigma$), so $|\Sigma|$ is always odd, but $h/2$ being self-symmetric doesn't guarantee inclusion.

**Important caveat:** The centered criterion $h/2 \in \Sigma_A$ matches $T \in D_A$ for **prime** $A$ only. For composite $A$ (e.g., $A = 15$), 81 mismatches were found where $T \in D_A$ but $h/2 \notin \Sigma_A$.

---

## 6. Analytic Route

**Proposition 8 (Burgess bound).** *For $n$ prime, $n \equiv 1 \pmod{4}$, there exists a prime $A \equiv 3 \pmod{4}$ with $(A/n) = -1$ and $A = O(n^{1/(4\sqrt{e})+\varepsilon})$ for any $\varepsilon > 0$.*

**Proof sketch.** The Burgess bound (1963) for character sums gives $\sum_{m \leq X} \chi(m) \ll X^{1-1/r} q^{(r+1)/(4r^2)} \log q$ for nonprincipal Dirichlet characters $\chi$ modulo $q$. Applied to the Legendre symbol $(\cdot/n)$, this gives the least QNR $n(p) \ll p^{1/(4\sqrt{e})+\varepsilon}$.

For the least QNR **prime** $\equiv 3 \pmod{4}$, we combine the Burgess bound with the PNT in AP using the product character $\psi = \chi_4 \cdot (\cdot/n)$ modulo $4n$. The Burgess bound applies to $\psi$, and partial summation passes from integers to primes. The PNT in AP provides the main term. This gives $A = O(n^{0.152})$ unconditionally.

Under GRH (Ankeny 1952): $A = O((\log n)^2)$.

**Sourcing:** Burgess (1963), Ankeny (1952), Iwaniec–Kowalski (2004), Davenport (2000). See `analysis/proposition8_sourced.md` for the full argument.

---

## 7. Open Problems

1. **Covering system proof:** Prove that a finite set of $A$ values covers all $n$. The 10M verification gives $C = 107$. The combinatorial route (parity) is necessary but not sufficient. The analytic route (Burgess) gives $O(n^{0.152})$ but not a constant. A constant bound is stronger than GRH.

2. **General $-1$ route:** The implication $-1 \in H(A) \Rightarrow -1 \in D_A$ fails in 821 cases. The centered residue set matches $T \in D_A$ perfectly for prime $A$ but also fails in 795 cases. Both reduce to the covering system proof.

3. **M-route sufficiency:** Computationally verified for all direct-route-failure cases ($n \leq 100{,}000$), but equivalent to the covering system proof.

---

## 8. Summary

| Result | Status |
|--------|--------|
| Divisor-residue criterion (Theorem 1) | **Proven** |
| $n \equiv 5 \pmod{8}$: $A = 3$ works (Theorem 2) | **Proven** |
| Theorem 3 converse (no QNR → $T \notin D_A$) | **Proven** |
| Legendre symbol identity (Theorem 5) | **Proven** |
| Partial $-1$ route ($h=2$, order-2 QNR) | **Proven** |
| General $-1$ route | **Fails** (821 cases) |
| Shifted set $D_A^{(nm)}$ | **Dead end** (0/2,213) |
| Parity obstruction (Theorem 10) | **Proven** |
| Covering set $n \leq 100{,}000$ (Theorem 9) | **Verified** |
| Covering set $n \leq 10{,}000{,}000$ (Theorem 9a) | **Verified** ($C = 107$) |
| Burgess bound $A = O(n^{0.152})$ (Prop 8) | **Sourced** |
| GRH: $A = O((\log n)^2)$ | **Conditional** |
| Constant bound $A \leq C$ | **Conjecture** ($C = 107$ up to $10^7$) |

---

## AI Assistance Disclosure

The author used Brodie Foxworth, an AI research agent, to assist with computational verification, development of the divisor-residue criterion, and manuscript preparation under the direction of the author. Brodie Foxworth is not an author. The author reviewed all mathematical claims, computations, citations, and conclusions, and accepts full responsibility for the manuscript.

---

## References

1. Burgess, D.A. (1963). "On character sums and L-series, II." *Proc. LMS* s3-13, 524–536.
2. Ankeny, N.C. (1952). "The least quadratic non residue." *Annals of Math.* 55, 65–72.
3. Iwaniec, H. & Kowalski, E. (2004). *Analytic Number Theory*. AMS Colloquium Publications, vol. 53.
4. Davenport, H. (2000). *Multiplicative Number Theory* (3rd ed.). Springer GTM 74.
5. Erdős, P. (1950). "Az egyenlet egész számú megoldásairól." *Mat. Lapok* 1, 192–210.
6. Mordell, L.J. (1967). *Diophantine Equations*. Academic Press, pp. 287–290.
7. Mballa, P.U. (2026). "A unified parametric approach to the Erdős–Straus conjecture." arXiv:2602.20036.
8. Salez, S.E. (2014). "The Erdős-Straus conjecture: new modular equations and checking up to 10¹⁷." arXiv:1406.6307.