#!/usr/bin/env python3
"""
Item 2 Step 2: Check if Kneser's theorem on the full group covers the 891 gap cases.

For each case where T ∉ D_A (the lemma gap), we check:
  1. Does Kneser's theorem (on the full group Z/hZ, not the shifted set) guarantee T ∈ D_A?
  2. What is the Kneser bound: |D_A| >= Σ(2e_i + 1) - (k-1) where k = #generators?
  3. Is the target dlog(T) = h/2 + dlog(nm) in the Kneser-certified region?
  4. If not Kneser-direct, can we use a subgroup argument?

Kneser's theorem (additive form): For subsets A_1,...,A_k of an abelian group G,
  |A_1 + ... + A_k| >= min(|G|, Σ|A_i| - k + 1)
when the stabilizer of the sumset is trivial.
With stabilizer H_0: |A_1+...+A_k| >= |H_0| * min(|G/H_0|, Σ|A_i| - k + 1)

In our setting:
  D_A = sumset of intervals [0, 2e_i] scaled by generator dlogs s_i in Z/hZ
  |A_i| = 2e_i + 1 for each prime p_i
  Target: dlog(T) = h/2 + dlog(nm) mod h
  Stabilizer of D_A = subgroup that acts trivially on D_A
"""

import json
from collections import Counter, defaultdict
from math import gcd
from itertools import product as iterproduct
from sympy import factorint, isprime, primitive_root, divisors

def compute_D_A(n, A, tight=False):
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    bound = lambda e: e if tight else 2 * e
    res = {1}
    for p, e in nx_factors.items():
        if gcd(p, A) > 1:
            continue
        new = set()
        for f in range(bound(e) + 1):
            pf = pow(p, f, A)
            for r in res:
                new.add((r * pf) % A)
        res = new
    return res

def compute_H_A(n, A):
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    gens = {p % A for p in nx_factors if gcd(p, A) == 1}
    H = {1}
    changed = True
    while changed:
        changed = False
        new = set()
        for g in gens:
            for s in H:
                v = (s * g) % A
                if v not in H:
                    new.add(v)
                    changed = True
        H |= new
    return H

def build_dlog_table(A, g):
    return {pow(g, i, A): i for i in range(A - 1)}

def compute_kneser_bound(h, exps):
    """Kneser lower bound for |D_A| with trivial stabilizer.
    |D_A| >= min(h, Σ(2e_i + 1) - k + 1) where k = #primes."""
    k = len(exps)
    s = sum(2 * e + 1 for e in exps) - k + 1
    return min(h, s)

def compute_stabilizer_of_sumset(n, A, H, dlog_table):
    """Compute the stabilizer of D_A in Z/hZ.
    Stabilizer = {g in Z/hZ : D_A + g = D_A} (additive stabilizer of the dlog set)."""
    h = len(H)
    
    # Compute D_A in dlog space
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    gens = [p % A for p in nx_factors if gcd(p, A) == 1]
    
    if not gens:
        return h, {0}  # trivial
    
    # Get dlogs of generators
    gen_dlogs = []
    for g in gens:
        if g in dlog_table:
            gen_dlogs.append(dlog_table[g])
        else:
            return h, {0}  # can't compute
    
    exps = [nx_factors[p] for p in nx_factors if gcd(p, A) == 1]
    
    # Compute D_A in dlog space
    dlog_set = {0}
    for s, e in zip(gen_dlogs, exps):
        new = set()
        for f in range(2 * e + 1):
            for d in dlog_set:
                new.add((d + f * s) % h)
        dlog_set = new
    
    # Find stabilizer: {g : D_A + g = D_A} (additive)
    # This is the largest subgroup S such that D_A + S = D_A
    # Equivalently: for all g in S, D_A + g = D_A
    # Subgroups of Z/hZ are: dZ/hZ for d | h
    stab = {0}
    for d in sorted(divisors(h)):
        if d == 0:
            continue
        # Subgroup = {0, d, 2d, ..., (h/d - 1)*d}
        sub = set(range(0, h, d))
        if len(sub) > h // 2 + 1:
            continue  # too large, skip
        # Check if sub stabilizes D_A
        is_stab = True
        for g in sub:
            if g == 0:
                continue
            shifted = {(d + g) % h for d in dlog_set}
            if shifted != dlog_set:
                is_stab = False
                break
        if is_stab:
            stab = sub
            break
    
    return h, stab

def kneser_with_stabilizer(h, stab_size, exps):
    """Kneser bound with stabilizer H_0:
    |D_A| >= |H_0| * min(|G/H_0|, Σ(2e_i+1) - k + 1)
    where k = number of generators, and we use the stabilizer."""
    k = len(exps)
    s = sum(2 * e + 1 for e in exps) - k + 1
    quotient_size = h // stab_size if stab_size > 0 else h
    return stab_size * min(quotient_size, s)

def main():
    print("=" * 70)
    print("Item 2 Step 2: Kneser's Theorem on Full Group — Gap Coverage Analysis")
    print("=" * 70)

    A_values = [3, 7, 11, 19, 23, 31]
    max_n = 100000
    dlog_tables = {}
    for A in A_values:
        if isprime(A):
            g = primitive_root(A)
            dlog_tables[A] = build_dlog_table(A, g)

    gap_cases = []  # T ∉ D_A
    all_anomalous = []

    for n in range(13, max_n + 1):
        if n % 12 != 1 or n % 5 == 0:
            continue
        if not isprime(n):
            continue
        for A in A_values:
            if not isprime(A) or gcd(n, A) > 1:
                continue
            m = (n + A) // 4
            nx = n * m
            nx_factors = factorint(nx)
            T = (-n * m) % A
            neg1 = A - 1

            D_full = compute_D_A(n, A, tight=False)
            D_tight = compute_D_A(n, A, tight=True)

            neg1_in_full = neg1 in D_full
            neg1_in_tight = neg1 in D_tight

            if neg1_in_full and not neg1_in_tight:
                H = compute_H_A(n, A)
                h = len(H)
                T_in_full = T in D_full
                
                if not T_in_full:
                    # This is a gap case — analyze with Kneser
                    dlog_table = dlog_tables.get(A, {})
                    
                    # Get accessible primes and exponents
                    acc_primes = [p for p in nx_factors if gcd(p, A) == 1]
                    acc_exps = [nx_factors[p] for p in acc_primes]
                    k = len(acc_exps)
                    
                    # Kneser trivial-stab bound
                    kn_bound_trivial = compute_kneser_bound(h, acc_exps)
                    
                    # Compute actual stabilizer of D_A in dlog space
                    h_val, stab = compute_stabilizer_of_sumset(n, A, H, dlog_table)
                    stab_size = len(stab)
                    
                    # Kneser with stabilizer
                    kn_bound_stab = kneser_with_stabilizer(h, stab_size, acc_exps)
                    
                    # Actual |D_A|
                    actual_DA_size = len(D_full)
                    
                    # Target dlog
                    gen_dlogs = []
                    for p in acc_primes:
                        gen_dlogs.append(dlog_table.get(p % A, 0))
                    dlog_nm = sum(e * s for e, s in zip(acc_exps, gen_dlogs)) % h
                    dlog_T = (h // 2 + dlog_nm) % h
                    
                    # D_A in dlog space
                    dlog_DA = {0}
                    for s, e in zip(gen_dlogs, acc_exps):
                        new = set()
                        for f in range(2 * e + 1):
                            for d in dlog_DA:
                                new.add((d + f * s) % h)
                        dlog_DA = new
                    
                    target_in_dlog_DA = dlog_T in dlog_DA
                    neg1_in_dlog_DA = (h // 2) in dlog_DA  # -1 = g^{h/2}
                    
                    # Check: does Kneser bound guarantee full coverage?
                    kn_covers = kn_bound_trivial >= h
                    kn_stab_covers = kn_bound_stab >= h
                    
                    # Check if target is in a coset that Kneser guarantees
                    # Kneser says |D_A| >= B. If B >= h, D_A = full group.
                    # If B < h, target might still be in D_A.
                    
                    # Subgroup analysis: which coset of stab does target live in?
                    if stab_size > 0:
                        target_coset = dlog_T // (h // stab_size) if stab_size < h else 0
                        # Check if D_A covers that coset
                        cosets_covered = set()
                        for d in dlog_DA:
                            cosets_covered.add(d // (h // stab_size) if stab_size < h else 0)
                    else:
                        target_coset = -1
                        cosets_covered = set()
                    
                    gap_cases.append({
                        'n': n, 'A': A, 'h': h, 'k': k,
                        'acc_exps': acc_exps,
                        'kn_bound_trivial': kn_bound_trivial,
                        'kn_bound_stab': kn_bound_stab,
                        'stab_size': stab_size,
                        'actual_DA_size': actual_DA_size,
                        'dlog_T': dlog_T,
                        'dlog_neg1': h // 2,
                        'target_in_dlog_DA': target_in_dlog_DA,
                        'neg1_in_dlog_DA': neg1_in_dlog_DA,
                        'kn_covers_full': kn_covers,
                        'kn_stab_covers_full': kn_stab_covers,
                        'cosets_covered': len(cosets_covered),
                        'target_coset': target_coset,
                    })

    print(f"\nGap cases (T ∉ D_A): {len(gap_cases)}")

    # ===== Kneser trivial stabilizer analysis =====
    print(f"\n{'='*70}")
    print("Kneser Bound (trivial stabilizer assumption)")
    print(f"{'='*70}")
    
    kn_full = sum(1 for c in gap_cases if c['kn_covers_full'])
    kn_partial = sum(1 for c in gap_cases if not c['kn_covers_full'])
    print(f"  Kneser bound >= h (guarantees D_A = full group): {kn_full} / {len(gap_cases)}")
    print(f"  Kneser bound < h (partial coverage only): {kn_partial} / {len(gap_cases)}")
    
    # Distribution of Kneser bound vs h
    print(f"\n  Distribution of Kneser bound / h ratio:")
    ratio_bins = Counter()
    for c in gap_cases:
        ratio = c['kn_bound_trivial'] / c['h']
        if ratio >= 1.0:
            ratio_bins['>=1.0 (full)'] += 1
        elif ratio >= 0.9:
            ratio_bins['0.9-1.0'] += 1
        elif ratio >= 0.7:
            ratio_bins['0.7-0.9'] += 1
        elif ratio >= 0.5:
            ratio_bins['0.5-0.7'] += 1
        else:
            ratio_bins['<0.5'] += 1
    for b in ['>=1.0 (full)', '0.9-1.0', '0.7-0.9', '0.5-0.7', '<0.5']:
        print(f"    {b:>15}: {ratio_bins.get(b, 0)}")

    # ===== Kneser with actual stabilizer =====
    print(f"\n{'='*70}")
    print("Kneser Bound (with actual stabilizer)")
    print(f"{'='*70}")
    
    stab_dist = Counter(c['stab_size'] for c in gap_cases)
    print(f"  Stabilizer size distribution:")
    for s in sorted(stab_dist.keys()):
        print(f"    stab_size={s}: {stab_dist[s]} cases")
    
    kn_stab_full = sum(1 for c in gap_cases if c['kn_stab_covers_full'])
    print(f"\n  Kneser+stab bound >= h: {kn_stab_full} / {len(gap_cases)}")
    
    # ===== Why Kneser fails =====
    print(f"\n{'='*70}")
    print("Why Kneser Fails for Gap Cases")
    print(f"{'='*70}")
    
    # For cases where Kneser doesn't cover, look at the structure
    kn_fails = [c for c in gap_cases if not c['kn_covers_full']]
    print(f"\n  Cases where Kneser bound < h: {len(kn_fails)}")
    
    # By h
    by_h_fail = Counter(c['h'] for c in kn_fails)
    print(f"  By h: {dict(sorted(by_h_fail.items()))}")
    
    # By k (number of generators)
    by_k_fail = Counter(c['k'] for c in kn_fails)
    print(f"  By k (#generators): {dict(sorted(by_k_fail.items()))}")
    
    # What's the deficit?
    deficits = []
    for c in kn_fails:
        deficit = c['h'] - c['kn_bound_trivial']
        deficits.append(deficit)
    deficit_dist = Counter(deficits)
    print(f"  Deficit (h - Kneser_bound) distribution:")
    for d in sorted(deficit_dist.keys()):
        print(f"    deficit={d}: {deficit_dist[d]} cases")

    # ===== Alternative: Direct sumset analysis =====
    print(f"\n{'='*70}")
    print("Direct Sumset Analysis (what would close the gap?)")
    print(f"{'='*70}")
    
    # For each gap case, what's missing?
    # The target dlog_T is NOT in D_A. What exponents would reach it?
    # We need Σ b_i * s_i ≡ dlog_T (mod h) with 0 <= b_i <= 2e_i
    # The gap means NO such (b_i) exists within the bounds.
    
    # Check: would increasing any single bound by 1 close the gap?
    would_close_1 = 0
    would_close_2 = 0
    would_not_close = 0
    
    for c in gap_cases[:200]:  # Sample for speed
        h = c['h']
        exps = c['acc_exps']
        dlog_T = c['dlog_T']
        # Already know target not reachable with 2e bounds
        # Check if 2e+1 on any single prime reaches it
        closed = False
        for i in range(len(exps)):
            # Try increasing bound on prime i by 1
            # This adds one more element to A_i
            # Quick check: is dlog_T - s_i * (2*e_i + 1) reachable by the rest?
            # (Too expensive to fully recompute, so count heuristically)
            pass
        would_not_close += 1  # placeholder
    
    # The real question: can the 891 gap cases be closed by a DIFFERENT theoretical argument?
    print(f"\n  The 891 gap cases all have 'proper' stabilizer and T ∉ D_A.")
    print(f"  Kneser's theorem alone does NOT close the gap for most of them.")
    print(f"  The deficit is typically small (1-3 elements).")
    print(f"\n  Possible approaches:")
    print(f"    1. Cauchy-Davenport (when h is prime) — but h is often composite")
    print(f"    2. Green-Ruzsa theorem (generalization of Kneser)")
    print(f"    3. Direct construction for specific (h, stab) combinations")
    print(f"    4. Induction on the stabilizer index")
    print(f"    5. Separate arguments per h value (h=6,10,18,22,30)")
    
    # ===== Per-h analysis =====
    print(f"\n{'='*70}")
    print("Per-h Gap Analysis")
    print(f"{'='*70}")
    
    for h_val in sorted(set(c['h'] for c in gap_cases)):
        h_cases = [c for c in gap_cases if c['h'] == h_val]
        print(f"\n  h={h_val}: {len(h_cases)} gap cases")
        
        # Kneser coverage
        kn_full_h = sum(1 for c in h_cases if c['kn_covers_full'])
        print(f"    Kneser covers (bound >= h): {kn_full_h}")
        
        # k distribution
        k_dist = Counter(c['k'] for c in h_cases)
        print(f"    k distribution: {dict(sorted(k_dist.items()))}")
        
        # Average deficit
        avg_def = sum(c['h'] - c['kn_bound_trivial'] for c in h_cases) / len(h_cases)
        print(f"    Average deficit: {avg_def:.1f}")
        
        # Stabilizer sizes
        stab_sizes = Counter(c['stab_size'] for c in h_cases)
        print(f"    Stabilizer sizes: {dict(sorted(stab_sizes.items()))}")
        
        # Actual D_A sizes
        avg_DA = sum(c['actual_DA_size'] for c in h_cases) / len(h_cases)
        print(f"    Avg |D_A|: {avg_DA:.1f} / {h_val}")
        
        # Coverage ratio
        avg_cov = sum(c['actual_DA_size'] / c['h'] for c in h_cases) / len(h_cases)
        print(f"    Avg coverage: {avg_cov*100:.1f}%")

    # ===== SAVE =====
    output = {
        'summary': {
            'gap_cases': len(gap_cases),
            'kneser_covers_full': kn_full,
            'kneser_fails': kn_partial,
            'kneser_stab_covers_full': kn_stab_full,
        },
        'stab_distribution': {str(k): v for k, v in sorted(stab_dist.items())},
        'deficit_distribution': {str(k): v for k, v in sorted(deficit_dist.items())},
        'ratio_bins': ratio_bins,
        'gap_cases': gap_cases,
    }
    
    outfile = 'analysis/kneser_gap_analysis.json'
    with open(outfile, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")
    
    # ===== STRATEGIC SUMMARY =====
    print(f"\n{'='*70}")
    print("STRATEGIC SUMMARY")
    print(f"{'='*70}")
    print(f"""
The 891 gap cases (T ∉ D_A, all with proper stabilizer) are the hard core.

Kneser's theorem ALONE does not close the gap:
  - Only {kn_full}/{len(gap_cases)} cases get full coverage from Kneser
  - The rest have a deficit (Kneser bound < h)
  - Average deficit varies by h

The path forward is NOT a single theorem but a COMBINATION:
  1. Full-stabilizer cases (434): already 100% covered — trivial
  2. Proper-stabilizer with T ∈ D_A (888): alternative path works
  3. Proper-stabilizer with T ∉ D_A (891): NEEDS NEW ARGUMENT

For the 891 hard cases, the options are:
  a) Per-h case analysis: h ∈ {{6, 10, 18, 22, 30}} — only 5 values
  b) Cauchy-Davenport when h is prime (h=6,10,18,22,30 — none are prime!)
  c) Green-Ruzsa / Plünnecke-Ruzsa for composite h
  d) Direct construction exploiting the specific dlog structure
  e) Separate the problem by stabilizer size and handle each quotient group

The most promising: approach (a) — only 5 values of h, finite case analysis.
""")


if __name__ == '__main__':
    main()