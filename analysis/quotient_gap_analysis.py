#!/usr/bin/env python3
"""
Item 2 Step 3: Quotient Group Argument for Gap Cases with Non-Trivial Stabilizer.

For gap cases where the stabilizer H_0 has size d > 1, we work in the
quotient group G/H_0 ≅ Z/(h/d)Z. The question becomes:

  Does the quotient sumset (D_A mod H_0) contain the target coset
  (dlog(T) mod H_0) in Z/(h/d)Z?

If yes for ALL such cases, the quotient argument closes those gaps.

Stabilizer sizes in gap cases:
  - stab_size=3: 77 cases (h=18: 14, h=30: 63) → quotient Z/6, Z/10
  - stab_size=5: 116 cases (all h=30) → quotient Z/6
  Total: 193 cases with non-trivial stabilizer (not 276 — recheck)

Wait, earlier we said 276. Let me recompute:
  - h=18, stab=3: 14 cases
  - h=30, stab=3: 63 cases
  - h=30, stab=5: 116 cases
  Total: 14 + 63 + 116 = 193 cases

But some gap cases might have stab sizes we missed. Let's recheck from the data.
Actually the kneser analysis showed:
  stab_size=1: 698, stab_size=3: 77, stab_size=5: 116 → total 891
  So 77 + 116 = 193 non-trivial-stab gap cases.

The quotient group argument applies to these 193 cases.
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

def compute_stabilizer_of_sumset_dlog(n, A, H, dlog_table):
    """Compute stabilizer of D_A in dlog space (additive Z/hZ)."""
    h = len(H)
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    
    gens = [p % A for p in nx_factors if gcd(p, A) == 1]
    gen_dlogs = []
    exps = []
    for p in nx_factors:
        if gcd(p, A) == 0:
            continue
        if p % A in dlog_table:
            gen_dlogs.append(dlog_table[p % A])
            exps.append(nx_factors[p])
    
    if not gen_dlogs:
        return h, {0}, set(), [], []
    
    # Compute D_A in dlog space
    dlog_set = {0}
    for s, e in zip(gen_dlogs, exps):
        new = set()
        for f in range(2 * e + 1):
            for d in dlog_set:
                new.add((d + f * s) % h)
        dlog_set = new
    
    # Find stabilizer: largest subgroup S of Z/hZ such that dlog_set + S = dlog_set
    # Subgroups of Z/hZ: for each divisor d of h, subgroup = {0, d, 2d, ..., (h/d-1)*d}
    stab = {0}
    for d in sorted(divisors(h)):
        if d == 0:
            continue
        sub_size = h // d
        if sub_size <= len(stab):
            continue
        sub = set(range(0, h, d))
        # Check if sub stabilizes dlog_set
        is_stab = True
        for g in sub:
            if g == 0:
                continue
            shifted = {(val + g) % h for val in dlog_set}
            if shifted != dlog_set:
                is_stab = False
                break
        if is_stab:
            stab = sub
            break
    
    return h, stab, dlog_set, gen_dlogs, exps

def quotient_analysis(h, stab, dlog_set, gen_dlogs, exps, dlog_T):
    """
    Work in quotient group Z/hZ / stab.
    The quotient is Z/(h/|stab|)Z.
    
    Map: x mod h → x mod |stab_coset_rep| in quotient.
    Actually: quotient = Z/hZ / S where S = stab.
    Quotient size = h / |stab| = h / len(stab).
    Elements of quotient are cosets x + S.
    Representative: x mod d where d = len(stab) ... no.
    
    For Z/hZ with subgroup S = {0, d, 2d, ...} where |S| = h/d:
    Wait, S = {0, d, 2d, ..., (h/d - 1)*d} has size h/d.
    Quotient Z/hZ / S has size d = h / (h/d) = d.
    No wait: |S| = h/d, quotient size = h / |S| = h / (h/d) = d.
    
    Let me be precise:
    Subgroup S = d*Z/hZ where d | h, so S = {0, d, 2d, ..., (h-d)} has |S| = h/d.
    Quotient Z/hZ / S ≅ Z/dZ where d is the "step" of the subgroup.
    
    Actually no. S = {0, d, 2d, ...} mod h. The quotient Z/hZ / S ≅ Z/dZ
    where the quotient map sends x → x mod d.
    
    So the quotient group has order d, and the map is x mod h → x mod d.
    """
    stab_size = len(stab)
    if stab_size <= 1:
        return None  # trivial stabilizer, quotient = original group
    
    # Find the subgroup step d: S = {0, d, 2d, ...} mod h
    # S has |S| = h/d elements, so d = h / |S|
    d = h // stab_size
    
    # Quotient map: x mod h → x mod d
    # Quotient group: Z/dZ
    quotient_size = d
    
    # Map D_A to quotient
    quotient_DA = {x % d for x in dlog_set}
    
    # Map target to quotient
    quotient_T = dlog_T % d
    
    # Map generators to quotient
    quotient_gens = [s % d for s in gen_dlogs]
    
    # Kneser bound in quotient:
    # |quotient_DA| >= min(d, sum(2e_i + 1) - k + 1) with trivial stab in Z/dZ
    k = len(exps)
    kn_quotient = min(d, sum(2*e + 1 for e in exps) - k + 1)
    
    # Check if target coset is covered
    target_covered = quotient_T in quotient_DA
    
    # Check: is the full quotient covered?
    full_covered = len(quotient_DA) == d
    
    # Also check: -1 in quotient DA?
    neg1_quotient = (h // 2) % d
    neg1_in_quotient_DA = neg1_quotient in quotient_DA
    
    return {
        'quotient_size': quotient_size,
        'quotient_DA_size': len(quotient_DA),
        'quotient_DA': sorted(quotient_DA),
        'quotient_T': quotient_T,
        'target_covered': target_covered,
        'full_covered': full_covered,
        'neg1_quotient': neg1_quotient,
        'neg1_in_quotient_DA': neg1_in_quotient_DA,
        'kn_quotient_bound': kn_quotient,
        'kn_covers_quotient': kn_quotient >= d,
        'quotient_gens': quotient_gens,
        'stab_size': stab_size,
        'stab_step_d': d,
    }

def main():
    print("=" * 70)
    print("Item 2 Step 3: Quotient Group Argument for Non-Trivial Stabilizer Cases")
    print("=" * 70)

    A_values = [3, 7, 11, 19, 23, 31]
    max_n = 100000
    dlog_tables = {}
    for A in A_values:
        if isprime(A):
            g = primitive_root(A)
            dlog_tables[A] = build_dlog_table(A, g)

    gap_cases_nontriv = []
    gap_cases_triv = []
    all_scanned = 0

    for n in range(13, max_n + 1):
        if n % 12 != 1 or n % 5 == 0:
            continue
        if not isprime(n):
            continue
        for A in A_values:
            if not isprime(A) or gcd(n, A) > 1:
                continue
            all_scanned += 1
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
                # Anomalous case
                T_in_full = T in D_full
                if not T_in_full:
                    # GAP case — analyze stabilizer
                    H = compute_H_A(n, A)
                    h = len(H)
                    dlog_table = dlog_tables.get(A, {})
                    
                    h_val, stab, dlog_set, gen_dlogs, exps = \
                        compute_stabilizer_of_sumset_dlog(n, A, H, dlog_table)
                    stab_size = len(stab)
                    
                    # Compute dlog of T
                    dlog_nm = sum(e * s for e, s in zip(exps, gen_dlogs)) % h
                    dlog_T = (h // 2 + dlog_nm) % h
                    
                    # Verify T is NOT in dlog_set (it's a gap case)
                    assert dlog_T not in dlog_set, f"T should not be in D_A for gap case n={n}, A={A}"
                    
                    case_data = {
                        'n': n, 'A': A, 'h': h, 'stab_size': stab_size,
                        'exps': exps, 'gen_dlogs': gen_dlogs,
                        'dlog_T': dlog_T, 'dlog_neg1': h // 2,
                        'dlog_DA_size': len(dlog_set),
                        'dlog_DA': sorted(dlog_set),
                    }
                    
                    if stab_size > 1:
                        # Run quotient analysis
                        qa = quotient_analysis(h, stab, dlog_set, gen_dlogs, exps, dlog_T)
                        case_data['quotient'] = qa
                        gap_cases_nontriv.append(case_data)
                    else:
                        gap_cases_triv.append(case_data)

    print(f"\nTotal gap cases: {len(gap_cases_nontriv) + len(gap_cases_triv)}")
    print(f"  Non-trivial stabilizer: {len(gap_cases_nontriv)}")
    print(f"  Trivial stabilizer: {len(gap_cases_triv)}")

    # ===== QUOTIENT ANALYSIS =====
    print(f"\n{'='*70}")
    print("Quotient Group Analysis (non-trivial stabilizer cases)")
    print(f"{'='*70}")

    # By stab_size
    print(f"\nBy stabilizer size:")
    for ss in sorted(set(c['stab_size'] for c in gap_cases_nontriv)):
        cases = [c for c in gap_cases_nontriv if c['stab_size'] == ss]
        covered = sum(1 for c in cases if c['quotient']['target_covered'])
        full = sum(1 for c in cases if c['quotient']['full_covered'])
        print(f"  stab_size={ss}: {len(cases)} cases, target_covered={covered}, full_covered={full}")

    # By quotient size
    print(f"\nBy quotient group size:")
    for qs in sorted(set(c['quotient']['quotient_size'] for c in gap_cases_nontriv)):
        cases = [c for c in gap_cases_nontriv if c['quotient']['quotient_size'] == qs]
        covered = sum(1 for c in cases if c['quotient']['target_covered'])
        full = sum(1 for c in cases if c['quotient']['full_covered'])
        print(f"  |quotient|={qs}: {len(cases)} cases, target_covered={covered}/{len(cases)}, full_covered={full}/{len(cases)}")

    # Detailed: is target coset covered?
    print(f"\n{'='*70}")
    print("Target Coset Coverage in Quotient")
    print(f"{'='*70}")
    
    target_covered_count = sum(1 for c in gap_cases_nontriv if c['quotient']['target_covered'])
    target_not_covered = sum(1 for c in gap_cases_nontriv if not c['quotient']['target_covered'])
    print(f"  Target coset covered: {target_covered_count} / {len(gap_cases_nontriv)}")
    print(f"  Target coset NOT covered: {target_not_covered} / {len(gap_cases_nontriv)}")

    # Full coverage
    full_cov = sum(1 for c in gap_cases_nontriv if c['quotient']['full_covered'])
    print(f"  Quotient DA = full quotient: {full_cov} / {len(gap_cases_nontriv)}")

    # Kneser in quotient
    kn_quot = sum(1 for c in gap_cases_nontriv if c['quotient']['kn_covers_quotient'])
    print(f"  Kneser covers quotient: {kn_quot} / {len(gap_cases_nontriv)}")

    # ===== Cross-tab: stab_size × quotient_size =====
    print(f"\n{'='*70}")
    print("Cross-tab: stab_size × quotient_size × target_covered")
    print(f"{'='*70}")
    crosstab = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # [covered, not_covered]
    for c in gap_cases_nontriv:
        ss = c['stab_size']
        qs = c['quotient']['quotient_size']
        if c['quotient']['target_covered']:
            crosstab[ss][qs][0] += 1
        else:
            crosstab[ss][qs][1] += 1
    
    print(f"{'stab':>6} | {'|Q|':>6} | {'covered':>8} | {'not_cov':>8} | {'total':>6}")
    print("-" * 45)
    for ss in sorted(crosstab.keys()):
        for qs in sorted(crosstab[ss].keys()):
            cov, not_cov = crosstab[ss][qs]
            print(f"{ss:6d} | {qs:6d} | {cov:8d} | {not_cov:8d} | {cov+not_cov:6d}")

    # ===== Detailed analysis of uncovered cases =====
    print(f"\n{'='*70}")
    print("Analysis of Uncovered Cases (target NOT in quotient DA)")
    print(f"{'='*70}")
    
    uncovered = [c for c in gap_cases_nontriv if not c['quotient']['target_covered']]
    print(f"\n  Total uncovered: {len(uncovered)}")
    
    if uncovered:
        print(f"\n  By h:")
        by_h = Counter(c['h'] for c in uncovered)
        print(f"  {dict(sorted(by_h.items()))}")
        
        print(f"\n  By A:")
        by_A = Counter(c['A'] for c in uncovered)
        print(f"  {dict(sorted(by_A.items()))}")
        
        print(f"\n  By quotient size:")
        by_qs = Counter(c['quotient']['quotient_size'] for c in uncovered)
        print(f"  {dict(sorted(by_qs.items()))}")
        
        # Show quotient DA and what's missing
        print(f"\n  Detailed view (first 20):")
        print(f"  {'n':>8} {'A':>4} {'h':>4} {'stab':>5} {'|Q|':>4} {'|QDA|':>5} {'QT':>4} {'QDA':>20} {'missing':>20}")
        for c in uncovered[:20]:
            qa = c['quotient']
            missing = set(range(qa['quotient_size'])) - set(qa['quotient_DA'])
            print(f"  {c['n']:8d} {c['A']:4d} {c['h']:4d} {c['stab_size']:5d} {qa['quotient_size']:4d} {qa['quotient_DA_size']:5d} {qa['quotient_T']:4d} {str(qa['quotient_DA']):>20} {str(sorted(missing)):>20}")

    # ===== COVERED cases: does the quotient argument WORK? =====
    print(f"\n{'='*70}")
    print("THE KEY QUESTION: Does quotient coverage imply T ∈ D_A?")
    print(f"{'='*70}")
    
    # If target coset is covered in quotient, does that mean T ∈ D_A in original?
    # NO! Quotient coverage means there EXISTS some element of D_A in the same
    # coset as T. It does NOT mean T itself is in D_A.
    # We need to check: does quotient DA covering target coset → T ∈ D_A?
    
    # Actually: T ∈ D_A iff dlog_T ∈ dlog_set.
    # Quotient covered means dlog_T % d ∈ {x % d : x ∈ dlog_set}.
    # This means there's some x ∈ dlog_set with x ≡ dlog_T (mod d).
    # But that x ≠ dlog_T necessarily.
    
    # So quotient coverage is NECESSARY but NOT SUFFICIENT for T ∈ D_A.
    # However, if quotient DA = full quotient, then the coset is covered,
    # but T might still not be in D_A.
    
    # Let's check: in the cases where quotient covers target coset,
    # is T actually in D_A? (It shouldn't be, since these are all gap cases)
    
    # Verify: all these cases have T ∉ D_A by construction
    print(f"\n  All gap cases have T ∉ D_A by construction.")
    print(f"  Quotient coverage means: some element of D_A is in T's coset.")
    print(f"  This is NECESSARY but NOT SUFFICIENT for T ∈ D_A.")
    print(f"\n  So the quotient argument alone cannot close the gap.")
    print(f"  But it tells us HOW CLOSE we are:")
    
    # For each covered case, how many elements of D_A are in T's coset?
    print(f"\n  For covered cases, elements of D_A in T's coset:")
    in_coset_counts = []
    for c in gap_cases_nontriv:
        qa = c['quotient']
        d = qa['stab_step_d']
        dlog_T = c['dlog_T']
        elements_in_coset = [x for x in c['dlog_DA'] if x % d == dlog_T % d]
        in_coset_counts.append(len(elements_in_coset))
    
    coset_dist = Counter(in_coset_counts)
    print(f"  Distribution of |D_A ∩ (T's coset)|:")
    for k in sorted(coset_dist.keys()):
        print(f"    {k} elements in coset: {coset_dist[k]} cases")

    # ===== LIFTING ARGUMENT =====
    print(f"\n{'='*70}")
    print("Lifting Argument: Can we lift quotient coverage to T ∈ D_A?")
    print(f"{'='*70}")
    
    # If dlog_T ≡ x (mod d) for some x ∈ dlog_DA, can we reach dlog_T exactly?
    # dlog_T = x + j*d for some j ∈ {0, 1, ..., stab_size - 1}
    # We need to find j such that x + j*d is reachable.
    
    # The coset has stab_size = h/d elements.
    # If ANY element of the coset is in D_A, the coset is covered.
    # But we need the SPECIFIC element dlog_T.
    
    # Check: for covered cases, what's the distance from the closest
    # D_A element to dlog_T within the coset?
    distances = []
    for c in gap_cases_nontriv:
        qa = c['quotient']
        d = qa['stab_step_d']
        dlog_T = c['dlog_T']
        coset_elements = [x for x in c['dlog_DA'] if x % d == dlog_T % d]
        if coset_elements:
            min_dist = min(abs(x - dlog_T) for x in coset_elements)
            # Also check modular distance
            min_mod_dist = min(min(abs(x - dlog_T), h - abs(x - dlog_T)) 
                              for x in coset_elements for h in [c['h']])
            distances.append(min_mod_dist)
    
    dist_dist = Counter(distances)
    print(f"  Distance from nearest D_A element to T (modular, within coset):")
    for k in sorted(dist_dist.keys()):
        print(f"    dist={k}: {dist_dist[k]} cases")

    # ===== STRATEGIC SUMMARY =====
    print(f"\n{'='*70}")
    print("STRATEGIC SUMMARY")
    print(f"{'='*70}")
    print(f"""
Quotient group analysis for {len(gap_cases_nontriv)} non-trivial-stab gap cases:

  Stab size 3 (quotient Z/6 or Z/10): {sum(1 for c in gap_cases_nontriv if c['stab_size']==3)} cases
  Stab size 5 (quotient Z/6):        {sum(1 for c in gap_cases_nontriv if c['stab_size']==5)} cases

Results:
  - Target coset covered in quotient: {target_covered_count}/{len(gap_cases_nontriv)}
  - Full quotient coverage: {full_cov}/{len(gap_cases_nontriv)}
  - Kneser covers quotient: {kn_quot}/{len(gap_cases_nontriv)}

Problem: Quotient coverage is NECESSARY but NOT SUFFICIENT.
  - Coverage means ∃ x ∈ D_A with x ≡ T (mod stab_step)
  - But T itself may not be in D_A
  - The coset has stab_size elements; D_A covers some but not all

  Distance from nearest D_A element to T within coset is typically small.

Next approach: COMBINE quotient argument with a lifting lemma.
  If the coset is covered AND the stabilizer acts transitively enough,
  we might lift coverage to T ∈ D_A via an additional argument:
  - Cauchy-Davenport within the coset (if coset size is prime)
  - Direct check for small cosets (size 3 or 5 — finite)
  - Kneser within the fiber of the quotient map

For stab_size=3: cosets have 3 elements → only 3 possibilities to check
For stab_size=5: cosets have 5 elements → only 5 possibilities to check
Both are small enough for exhaustive verification!
""")

    # ===== SAVE =====
    output = {
        'summary': {
            'non_triv_gap_cases': len(gap_cases_nontriv),
            'triv_gap_cases': len(gap_cases_triv),
            'target_covered': target_covered_count,
            'target_not_covered': target_not_covered,
            'full_covered': full_cov,
            'kneser_covers': kn_quot,
        },
        'coset_element_dist': {str(k): v for k, v in sorted(coset_dist.items())},
        'distance_dist': {str(k): v for k, v in sorted(dist_dist.items())},
        'cases': gap_cases_nontriv,
    }
    
    outfile = 'analysis/quotient_gap_analysis.json'
    with open(outfile, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")


if __name__ == '__main__':
    main()