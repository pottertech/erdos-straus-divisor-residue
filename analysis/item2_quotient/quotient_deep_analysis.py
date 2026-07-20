#!/usr/bin/env python3
"""
Item 2 Step 3b: Deep dive into WHY the target is systematically excluded
from the quotient D_A in all 193 non-trivial-stab gap cases.

Observation from Step 3:
  - stab_size=5, quotient Z/6: D_A covers 5/6, missing element 1 or 5
  - stab_size=3, quotient Z/10: D_A covers 9/10, missing element 1 or 9

Question: Is the missing element always -1 in the quotient group?
  Z/6: -1 = 5
  Z/10: -1 = 9

If so, this means:
  -1 ∉ D_A (quotient) → -1 ∉ D_A (original, mod stab)
  Which is EXACTLY the original problem restated in the quotient!

This would mean the stabilizer argument is circular: the quotient
inherits the same -1 obstruction.

But wait — in the original group, -1 ∈ D_A (that's the premise).
So the obstruction must arise from the quotient map itself.
"""

import json
from collections import Counter
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
    h = len(H)
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    
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
    
    dlog_set = {0}
    for s, e in zip(gen_dlogs, exps):
        new = set()
        for f in range(2 * e + 1):
            for d in dlog_set:
                new.add((d + f * s) % h)
        dlog_set = new
    
    stab = {0}
    for d in sorted(divisors(h)):
        if d == 0:
            continue
        sub_size = h // d
        if sub_size <= len(stab):
            continue
        sub = set(range(0, h, d))
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

def main():
    print("=" * 70)
    print("Step 3b: Why is the target systematically excluded from quotient D_A?")
    print("=" * 70)

    A_values = [3, 7, 11, 19, 23, 31]
    max_n = 100000
    dlog_tables = {}
    for A in A_values:
        if isprime(A):
            g = primitive_root(A)
            dlog_tables[A] = build_dlog_table(A, g)

    results = []

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
                T_in_full = T in D_full
                if not T_in_full:
                    # Gap case
                    H = compute_H_A(n, A)
                    h = len(H)
                    dlog_table = dlog_tables.get(A, {})
                    
                    h_val, stab, dlog_set, gen_dlogs, exps = \
                        compute_stabilizer_of_sumset_dlog(n, A, H, dlog_table)
                    stab_size = len(stab)
                    
                    if stab_size <= 1:
                        continue  # Skip trivial stab for this analysis
                    
                    d = h // stab_size  # quotient step
                    quotient_size = d
                    
                    # Quotient D_A
                    quotient_DA = {x % d for x in dlog_set}
                    
                    # Target in quotient
                    dlog_nm = sum(e * s for e, s in zip(exps, gen_dlogs)) % h
                    dlog_T = (h // 2 + dlog_nm) % h
                    quotient_T = dlog_T % d
                    
                    # -1 in quotient
                    neg1_quotient = (h // 2) % d
                    
                    # nm in quotient
                    quotient_nm = dlog_nm % d
                    
                    # Generators in quotient
                    quotient_gens = [s % d for s in gen_dlogs]
                    
                    # What's missing from quotient D_A?
                    missing = set(range(d)) - quotient_DA
                    
                    # Is the missing element always -1?
                    neg1_in_missing = neg1_quotient in missing
                    target_is_neg1 = (quotient_T == neg1_quotient)
                    
                    # Key question: is target == -1 in quotient?
                    # dlog(T) = h/2 + dlog(nm). In quotient Z/d: T% d = (h/2 % d) + (dlog_nm % d) = neg1_quot + dlog_nm_quot
                    # -1 in quotient = h/2 % d
                    # So target == -1 iff dlog_nm % d == 0, i.e., nm is in the stabilizer subgroup.
                    
                    # Check: is nm in the stabilizer?
                    # nm in stab means dlog_nm is a multiple of d (the stab step)
                    nm_in_stab = (dlog_nm % d == 0)
                    
                    results.append({
                        'n': n, 'A': A, 'h': h, 'stab_size': stab_size,
                        'quotient_size': d,
                        'dlog_nm': dlog_nm, 'dlog_T': dlog_T,
                        'quotient_T': quotient_T,
                        'neg1_quotient': neg1_quotient,
                        'quotient_nm': quotient_nm,
                        'missing': sorted(missing),
                        'quotient_DA': sorted(quotient_DA),
                        'quotient_gens': quotient_gens,
                        'exps': exps,
                        'target_is_neg1': target_is_neg1,
                        'nm_in_stab': nm_in_stab,
                        'neg1_in_missing': neg1_in_missing,
                    })

    print(f"\nNon-trivial-stab gap cases: {len(results)}")

    # ===== Is target always -1 in quotient? =====
    print(f"\n{'='*70}")
    print("Is the target always -1 in the quotient group?")
    print(f"{'='*70}")
    
    target_neg1 = sum(1 for r in results if r['target_is_neg1'])
    target_not_neg1 = sum(1 for r in results if not r['target_is_neg1'])
    print(f"  Target == -1 in quotient: {target_neg1} / {len(results)}")
    print(f"  Target != -1 in quotient: {target_not_neg1} / {len(results)}")
    
    if target_neg1 == len(results):
        print(f"\n  YES! Target is ALWAYS -1 in the quotient.")
        print(f"  This means the obstruction is: -1 ∉ D_A (quotient)")
        print(f"  The quotient INHERITS the same -1 problem.")

    # ===== Is nm always in the stabilizer? =====
    print(f"\n{'='*70}")
    print("Is nm always in the stabilizer subgroup?")
    print(f"{'='*70}")
    
    nm_in_stab_count = sum(1 for r in results if r['nm_in_stab'])
    print(f"  nm ∈ stab: {nm_in_stab_count} / {len(results)}")
    
    if nm_in_stab_count == len(results):
        print(f"\n  YES! nm is ALWAYS in the stabilizer.")
        print(f"  This is WHY target == -1 in quotient:")
        print(f"  dlog(T) = h/2 + dlog(nm), and dlog(nm) ≡ 0 (mod d)")
        print(f"  so T mod d = h/2 mod d = -1 in quotient.")

    # ===== What does -1 look like in the quotient? =====
    print(f"\n{'='*70}")
    print("Structure of -1 obstruction in quotient")
    print(f"{'='*70}")
    
    # The quotient D_A is a sumset in Z/dZ.
    # Generators are s_i mod d, with bounds 0..2e_i.
    # -1 = d-1 in Z/dZ (when d is even) or (d-1)/2 (when d is odd... no)
    # Actually -1 in Z/dZ is just d-1.
    
    # But wait: h/2 mod d. h = stab_size * d. So h/2 = stab_size * d / 2.
    # If stab_size is even: h/2 = (stab_size/2) * d, so h/2 mod d = 0. -1 in quotient = 0??
    # If stab_size is odd: h/2 = stab_size * d / 2, and d must be even (since h = stab*d and h is even).
    
    # h = stab_size * d. For our cases:
    #   stab=3, h=18: d=6. h/2=9. 9 mod 6 = 3. -1 in Z/6 = 5. NOT EQUAL!
    #   stab=3, h=30: d=10. h/2=15. 15 mod 10 = 5. -1 in Z/10 = 9. NOT EQUAL!
    #   stab=5, h=30: d=6. h/2=15. 15 mod 6 = 3. -1 in Z/6 = 5. NOT EQUAL!
    
    # Wait! The "neg1_quotient" we computed is h/2 mod d, which is the image of -1 from
    # the original group under the quotient map. But -1 in the quotient group Z/dZ
    # is d-1, which may be DIFFERENT from h/2 mod d.
    
    # So there are TWO notions of -1:
    # 1. Original -1 mapped to quotient: h/2 mod d
    # 2. -1 in quotient group itself: d-1
    
    # The target is dlog_T mod d = (h/2 + dlog_nm) mod d = h/2 mod d (since nm in stab)
    # So target = h/2 mod d (the image of original -1).
    
    # But -1 in the quotient GROUP (as a multiplicative concept) would be
    # the element of order 2 in Z/dZ, which is d/2 if d is even, or doesn't exist if d is odd.
    
    # Actually in additive Z/dZ, -1 is just d-1 (additive inverse of 1).
    # The element of order 2 is d/2 (when d is even).
    
    # The question is whether h/2 mod d equals d-1 (additive -1) or d/2 (element of order 2).
    
    print(f"\n  For each (stab_size, h, d):")
    print(f"  {'stab':>5} {'h':>4} {'d':>4} {'h/2':>4} {'h/2 mod d':>9} {'d-1':>4} {'d/2':>4} {'target_type':>12}")
    seen = set()
    for r in results:
        key = (r['stab_size'], r['h'], r['quotient_size'])
        if key in seen:
            continue
        seen.add(key)
        ss, h, d = key
        h2 = h // 2
        h2_mod_d = h2 % d
        neg1_add = d - 1
        order2 = d // 2 if d % 2 == 0 else None
        if h2_mod_d == neg1_add:
            ttype = "additive -1"
        elif order2 is not None and h2_mod_d == order2:
            ttype = "order-2 elem"
        else:
            ttype = f"other ({h2_mod_d})"
        print(f"  {ss:5d} {h:4d} {d:4d} {h2:4d} {h2_mod_d:9d} {neg1_add:4d} {str(order2):>4} {ttype:>12}")
    
    # ===== The REAL question: does -1 ∈ D_A in the original imply
    # -1_quotient ∈ D_A_quotient? =====
    print(f"\n{'='*70}")
    print("Does -1 ∈ D_A (original) imply -1_quotient ∈ quotient D_A?")
    print(f"{'='*70}")
    
    # -1 in original D_A means h/2 ∈ dlog_set.
    # -1_quotient = h/2 mod d.
    # quotient D_A = {x mod d : x ∈ dlog_set}.
    # So h/2 mod d IS in quotient D_A (since h/2 ∈ dlog_set).
    # BUT THE TARGET IS ALSO h/2 mod d (since nm ∈ stab)!
    
    # Wait — if -1 ∈ D_A (original) then h/2 ∈ dlog_set,
    # so h/2 mod d ∈ quotient D_A.
    # And target = h/2 mod d (since nm in stab).
    # So target IS in quotient D_A!
    
    # But our computation showed 0/193 covered. Contradiction!
    # Let me check...
    
    print(f"\n  Let me verify: is h/2 always in dlog_set for these gap cases?")
    h2_in_dlog = sum(1 for r in results if (r['h'] // 2) in set(range(r['h'])) and True)
    # Actually we need to recompute dlog_set for each case...
    # The key insight: these are ANOMALOUS cases where -1 ∈ D_A but -1 ∉ D_A^(nm).
    # By definition, -1 ∈ D_A (full), so h/2 IS in dlog_set.
    # So h/2 mod d IS in quotient D_A.
    # And target = h/2 + dlog_nm, with dlog_nm ≡ 0 mod d (nm in stab).
    # So target mod d = h/2 mod d.
    # So target IS in quotient D_A!
    
    # But the script said 0/193. There must be a bug.
    # Let me check the computation directly.
    
    print(f"\n  DEBUG: Checking a few cases directly...")
    for r in results[:5]:
        h2 = r['h'] // 2
        d = r['quotient_size']
        h2_mod_d = h2 % d
        target_mod_d = r['quotient_T']
        qDA = set(r['quotient_DA'])
        print(f"    n={r['n']}, A={r['A']}, h={r['h']}, d={d}")
        print(f"    h/2={h2}, h/2 mod d={h2_mod_d}, target mod d={target_mod_d}")
        print(f"    quotient D_A={r['quotient_DA']}")
        print(f"    h/2 mod d in quotient D_A? {h2_mod_d in qDA}")
        print(f"    target mod d in quotient D_A? {target_mod_d in qDA}")
        print(f"    nm_in_stab={r['nm_in_stab']}, dlog_nm={r['dlog_nm']}, dlog_nm mod d={r['dlog_nm'] % d}")
        print()

    # ===== THE RESOLUTION =====
    print(f"{'='*70}")
    print("RESOLUTION OF THE APPARENT CONTRADICTION")
    print(f"{'='*70}")
    
    # If -1 ∈ D_A (original), then h/2 ∈ dlog_set.
    # But our gap cases are defined by -1 ∈ D_A (multiplicative, not dlog).
    # -1 in D_A means (A-1) ∈ D_A as a MULTIPLICATIVE residue, i.e., there exist
    # exponents b_i with 0 <= b_i <= 2e_i such that product(p_i^b_i) ≡ -1 (mod A).
    # In dlog space: sum(b_i * s_i) ≡ (A-1's dlog) mod (A-1).
    # But h = |H(A)| which divides A-1. The dlog is mod h, not mod (A-1).
    
    # So -1 ∈ D_A (multiplicative) means A-1 ∈ D_A as a residue.
    # In dlog space (mod h): the dlog of A-1 is h/2 ONLY IF A-1 = g^{h/2} in H(A).
    # But A-1 might not be in H(A) at all! It's -1 mod A, which has order 2.
    # If h is even, -1 = g^{h/2} IS in H(A). If h is odd, -1 is NOT in H(A).
    
    # For our cases h = 6,10,18,22,30 — all even, so -1 = g^{h/2} IS in H(A).
    # So -1 ∈ D_A means h/2 ∈ dlog_set. This should hold.
    
    # But wait — dlog_set is computed from the generators and bounds.
    # -1 ∈ D_A (multiplicative) means -1 is reachable as a product of p_i^b_i.
    # In dlog: sum(b_i * s_i) ≡ h/2 (mod h). So h/2 IS in dlog_set.
    
    # Then h/2 mod d IS in quotient D_A. And target = h/2 + dlog_nm mod h,
    # with dlog_nm ≡ 0 mod d. So target mod d = h/2 mod d.
    # So target SHOULD be in quotient D_A.
    
    # The bug must be in the computation. Let me check if h/2 is actually
    # in dlog_set for these cases.
    
    print(f"\n  Checking if h/2 is actually in dlog_set for gap cases...")
    # We need to recompute dlog_set. But we already have it in the results
    # from the previous script. Let me just check the quotient_DA sets.
    
    h2_mod_d_in_qDA = 0
    for r in results:
        d = r['quotient_size']
        h2_mod_d = (r['h'] // 2) % d
        if h2_mod_d in set(r['quotient_DA']):
            h2_mod_d_in_qDA += 1
    
    print(f"  h/2 mod d in quotient D_A: {h2_mod_d_in_qDA} / {len(results)}")
    
    # If this is also 0, then -1 ∉ D_A in these cases, which contradicts
    # our premise. But the premise was -1 ∈ D_A (multiplicative).
    # The issue might be that the dlog computation uses a DIFFERENT primitive
    # root than the one defining -1 = g^{h/2}.
    
    # Actually the real issue: -1 ∈ D_A means A-1 is reachable as a PRODUCT
    # of p_i^{b_i}. The dlog of A-1 mod A with primitive root g is (A-1)/2
    # (since g is a primitive root mod A, g^{(A-1)/2} ≡ -1 mod A).
    # But we're working in H(A) which has order h | (A-1).
    # The dlog of -1 in H(A) is h/2 (since -1 has order 2 in H(A) when h is even).
    
    # So -1 ∈ D_A ↔ h/2 ∈ dlog_set. This should hold.
    
    # Unless... the dlog_table maps residues to dlogs mod (A-1), not mod h.
    # Let me check: dlog_table = {pow(g, i, A): i for i in range(A-1)}.
    # So dlog values are in range(A-1), not range(h).
    # But H(A) has order h, and the dlog mod h is dlog mod h.
    
    # AH — that's the issue! The dlog_table gives dlogs mod (A-1), but
    # the sumset structure is in Z/hZ, not Z/(A-1)Z. We need to reduce
    # the dlogs mod h before computing the sumset.
    
    # Let me check if the previous scripts handled this correctly...
    
    print(f"\n  POTENTIAL BUG: dlog_table gives dlogs mod (A-1), but sumset is in Z/hZ.")
    print(f"  Need to reduce dlogs mod h before computing sumset.")
    print(f"  Checking if this was done correctly in previous scripts...")
    
    # In the original scripts, gen_dlogs = [dlog_table[p % A] for p in ...]
    # These are mod (A-1). Then sum(b_i * s_i) % h — the % h reduces correctly.
    # And the sumset computation: (d + f * s) % h — also reduces correctly.
    # So the dlog_set IS computed in Z/hZ. Good.
    
    # But the dlog of -1: g^{(A-1)/2} ≡ -1 (mod A). The dlog of -1 in the
    # full group Z/(A-1)Z is (A-1)/2. In the subgroup H(A) of order h,
    # -1 = g^{(A-1)/2}. For -1 to be in H(A), we need (A-1)/2 to be a
    # multiple of (A-1)/h, i.e., h | (A-1)/2 * h/(A-1) ... no.
    # H(A) = <g^{(A-1)/h}>. So -1 ∈ H(A) iff (A-1)/2 ≡ 0 mod (A-1)/h,
    # i.e., h | (A-1)/2 * ... hmm, -1 = g^{(A-1)/2}. This is in <g^{(A-1)/h}>
    # iff (A-1)/2 is a multiple of (A-1)/h, i.e., h | (A-1)/2 * h/(A-1) ...
    # no: g^{(A-1)/2} ∈ <g^{(A-1)/h}> iff (A-1)/h | (A-1)/2, i.e., h | 2(A-1)/h...
    # i.e., (A-1)/h divides (A-1)/2, i.e., 2 divides h.
    
    # Since h is always even in our cases, -1 IS in H(A) and its dlog in H(A)
    # is (A-1)/2 mod (A-1)/h ... no. Let me think more carefully.
    
    # H(A) = {g^{j*(A-1)/h} : j = 0, ..., h-1}. 
    # -1 = g^{(A-1)/2}. For -1 to be in H(A): (A-1)/2 = j*(A-1)/h for some j,
    # i.e., j = h/2. So -1 = g^{(h/2)*(A-1)/h} = g^{(A-1)/2}. YES.
    # The dlog of -1 in H(A) (using generator g^{(A-1)/h}) is h/2.
    
    # BUT in our dlog_table (which uses primitive root g, not g^{(A-1)/h}),
    # the dlog of p % A is dlog_table[p % A] which is mod (A-1).
    # To convert to the H(A) dlog, we need to multiply by h/(A-1).
    # dlog_H = dlog_g * h / (A-1) = dlog_g / ((A-1)/h).
    
    # AH HA — THIS IS THE BUG! The scripts compute gen_dlogs using the
    # primitive root dlog (mod A-1), but the sumset structure is in Z/hZ.
    # The conversion factor is (A-1)/h, and the scripts DON'T apply it!
    
    # Actually wait — let me re-read the code. In classify_anomalous.py:
    # gen_dlogs[p] = dlog_table[p % A]  — this is mod (A-1)
    # dlog_nm = sum(e * s for e, s in ...) % h  — reducing mod h
    # dlog_T = (h//2 + dlog_nm) % h
    
    # The reduction % h is WRONG if the dlogs are mod (A-1).
    # We need: dlog_H = dlog_g * (h / (A-1)) mod h
    # Or equivalently: dlog_H = dlog_g / ((A-1)/h) mod h
    
    # Since (A-1)/h is the index, and h | (A-1), we need to DIVIDE by the index.
    # But division mod h requires the index to be coprime to h, which isn't guaranteed.
    
    # Actually, the correct approach: H(A) is generated by g' = g^{(A-1)/h}.
    # The dlog of x in H(A) (base g') is: j such that g'^j = x, i.e., g^{j*(A-1)/h} = x.
    # If x = g^k, then j*(A-1)/h ≡ k (mod A-1), so j ≡ k * h/(A-1) (mod h).
    # But k * h / (A-1) = k / ((A-1)/h). This is an integer only if (A-1)/h | k.
    
    # For generators p_i: p_i^{(A-1)} ≡ 1, and p_i generates a subgroup of H(A)
    # iff ord(p_i mod A) | h. The dlog of p_i in H(A) base g' is:
    # j such that g'^{j} ≡ p_i, i.e., g^{j*(A-1)/h} ≡ p_i (mod A).
    # If p_i = g^{k_i} in the full group, then j*(A-1)/h ≡ k_i (mod A-1),
    # so j ≡ k_i * h/(A-1) (mod h), but k_i * h / (A-1) = k_i / ((A-1)/h).
    
    # For this to have a solution, (A-1)/h must divide k_i, which means p_i ∈ H(A).
    # If p_i ∉ H(A), then p_i doesn't contribute to D_A (it's not a generator of H(A)).
    
    # THE REAL ISSUE: the dlog_table maps residues to exponents of the PRIMITIVE ROOT g.
    # But generators of D_A are the RESIDUES p_i mod A, and their dlogs in H(A)
    # require the conversion. The scripts that compute dlog_nm etc. are using
    # the FULL GROUP dlog (mod A-1) and reducing mod h, which is NOT the same
    # as the H(A) dlog (mod h) unless the conversion factor is applied.
    
    # HOWEVER: the sumset structure is independent of the dlog representation.
    # D_A = {product p_i^{b_i} mod A : 0 <= b_i <= 2e_i}. This is a set of residues.
    # The dlog representation is just for analysis. The actual D_A computation
    # (compute_D_A) correctly computes the multiplicative set.
    
    # The dlog analysis is only for understanding the STRUCTURE. If the dlog
    # conversion is wrong, the structural conclusions (like "target == -1 in quotient")
    # might be wrong, but the D_A computation itself is correct.
    
    # Let me verify: is -1 actually in D_A for these gap cases?
    # We can check directly: is (A-1) in compute_D_A(n, A)?
    
    print(f"\n  Direct verification: is -1 actually in D_A for gap cases?")
    verified = 0
    not_verified = 0
    for r in results[:50]:
        n, A = r['n'], r['A']
        D = compute_D_A(n, A, tight=False)
        if (A - 1) in D:
            verified += 1
        else:
            not_verified += 1
            print(f"    WARNING: -1 NOT in D_A for n={n}, A={A}!")
    print(f"  -1 ∈ D_A (verified): {verified}/50")
    print(f"  -1 ∉ D_A (error):    {not_verified}/50")

    # ===== CORRECT QUOTIENT ANALYSIS =====
    print(f"\n{'='*70}")
    print("CORRECTED Quotient Analysis (multiplicative, not dlog)")
    print(f"{'='*70}")
    
    # Instead of working in dlog space, work directly with multiplicative residues.
    # The stabilizer of D_A (multiplicative) is: S = {s ∈ H(A) : s * D_A = D_A}.
    # The quotient H(A)/S acts on the cosets.
    # Target: T = -nm mod A. We want to know if T is in the same S-coset as
    # some element of D_A.
    
    # Actually, let me recompute everything in multiplicative space.
    
    corrected_results = []
    for r in results:
        n, A = r['n'], r['A']
        h = r['h']
        
        D = compute_D_A(n, A, tight=False)
        H = compute_H_A(n, A)
        
        # Compute multiplicative stabilizer of D_A in H(A)
        # S = {s ∈ H : s * D = D} (multiplicative)
        # Since D ⊆ H (all elements of D_A are in H(A) by construction),
        # s * D = {s * d mod A : d ∈ D}. We need s * D = D.
        
        # Subgroups of H(A) (multiplicative): H(A) ≅ Z/hZ (additive).
        # Subgroups of order d correspond to index-d subgroups.
        # In multiplicative terms: S = {g^{j*h/d} : j=0,...,d-1} for each d | h.
        
        g = primitive_root(A)
        # H(A) generators
        m = (n + A) // 4
        nx = n * m
        nx_factors = factorint(nx)
        gens_res = {p % A for p in nx_factors if gcd(p, A) == 1}
        
        # Find multiplicative stabilizer of D
        # Check each subgroup of H(A)
        stab_mult = {1}  # trivial
        for d in sorted(divisors(h)):
            if d <= 1:
                continue
            sub_size = h // d  # subgroup order
            if sub_size <= len(stab_mult):
                continue
            # Subgroup of order sub_size: {g^{j * (A-1)/sub_size} : j=0,...,sub_size-1}
            # But need to check if these are in H(A). H(A) = {g^{j*(A-1)/h} : j=0,...,h-1}.
            # Subgroup of order sub_size in H(A): {g^{j * h/sub_size * (A-1)/h} : j=0,...,sub_size-1}
            # = {g^{j * (A-1)/sub_size} : j=0,...,sub_size-1}
            step = (A - 1) // sub_size
            sub_mult = {pow(g, j * step, A) for j in range(sub_size)}
            
            # Check if sub_mult stabilizes D (multiplicatively)
            is_stab = True
            for s in sub_mult:
                if s == 1:
                    continue
                shifted = {(s * d) % A for d in D}
                if shifted != D:
                    is_stab = False
                    break
            if is_stab:
                stab_mult = sub_mult
                break
        
        stab_size_mult = len(stab_mult)
        
        # Quotient: H(A) / stab_mult
        # Cosets: stab_mult * h for h ∈ H(A)
        # Map D_A to quotient: D_A → {coset representative}
        # Target T → which coset?
        
        # Find coset of T
        T = (-n * m) % A
        neg1 = A - 1
        
        # Coset representatives: for each h ∈ H, coset = stab * h
        # Find which coset each element is in
        # Use the step d = h // stab_size_mult
        # In additive dlog: coset = dlog(x) mod d
        # In multiplicative: coset representative = x * stab_mult^{-1} ... 
        # Easier: use additive dlog but correctly this time.
        
        # Actually, the multiplicative stabilizer corresponds to the additive
        # stabilizer in dlog space. The issue was the dlog conversion, not
        # the stabilizer computation.
        
        # Let me just directly check: which cosets does D_A cover, and
        # which coset is T in?
        
        # Coset of element x: the set stab_mult * x = {s*x mod A : s ∈ stab_mult}
        # Two elements are in the same coset iff their coset sets are equal.
        # Simpler: x and y are in the same coset iff x/y ∈ stab_mult
        # (where x/y = x * y^{-1} mod A, and y^{-1} = pow(y, A-2, A) since A is prime)
        
        def coset_id(x, stab_mult, A):
            """Return a canonical representative for the coset of x."""
            # x's coset = {s*x mod A : s ∈ stab_mult}
            # Canonical rep = min of coset
            coset = {(s * x) % A for s in stab_mult}
            return min(coset)
        
        def in_same_coset(x, y, stab_mult, A):
            """Check if x and y are in the same coset."""
            # x/y mod A should be in stab_mult
            y_inv = pow(y, A - 2, A)
            ratio = (x * y_inv) % A
            return ratio in stab_mult
        
        # D_A cosets
        D_cosets = set()
        for d in D:
            D_cosets.add(coset_id(d, stab_mult, A))
        
        # Target coset
        T_coset = coset_id(T, stab_mult, A)
        
        # -1 coset
        neg1_coset = coset_id(neg1, stab_mult, A)
        
        # Is T's coset covered by D_A?
        T_coset_covered = T_coset in D_cosets
        
        # Is -1's coset covered?
        neg1_coset_covered = neg1_coset in D_cosets
        
        # Number of cosets
        n_cosets = h // stab_size_mult
        
        # Is -1 in D_A?
        neg1_in_D = neg1 in D
        
        # Is nm in stab_mult?
        nm_mod = (n * m) % A
        nm_in_stab_mult = nm_mod in stab_mult
        
        corrected_results.append({
            'n': n, 'A': A, 'h': h,
            'stab_size_mult': stab_size_mult,
            'n_cosets': n_cosets,
            'D_cosets_covered': len(D_cosets),
            'T_coset': T_coset,
            'T_coset_covered': T_coset_covered,
            'neg1_coset': neg1_coset,
            'neg1_coset_covered': neg1_coset_covered,
            'neg1_in_D': neg1_in_D,
            'nm_in_stab': nm_in_stab_mult,
            'T_in_D': T in D,
        })
    
    # Summary
    print(f"\n  Corrected results for {len(corrected_results)} non-trivial-stab gap cases:")
    print(f"  (verifying -1 ∈ D_A and T ∉ D_A)")
    
    neg1_in_D_count = sum(1 for r in corrected_results if r['neg1_in_D'])
    T_not_in_D = sum(1 for r in corrected_results if not r['T_in_D'])
    print(f"  -1 ∈ D_A: {neg1_in_D_count}/{len(corrected_results)}")
    print(f"  T ∉ D_A: {T_not_in_D}/{len(corrected_results)}")
    
    print(f"\n  Multiplicative stabilizer sizes:")
    stab_dist = Counter(r['stab_size_mult'] for r in corrected_results)
    for s in sorted(stab_dist.keys()):
        print(f"    stab_size={s}: {stab_dist[s]} cases")
    
    print(f"\n  Coset coverage:")
    t_cov = sum(1 for r in corrected_results if r['T_coset_covered'])
    neg1_cov = sum(1 for r in corrected_results if r['neg1_coset_covered'])
    print(f"    T's coset covered: {t_cov}/{len(corrected_results)}")
    print(f"    -1's coset covered: {neg1_cov}/{len(corrected_results)}")
    
    print(f"\n  nm ∈ stabilizer (multiplicative):")
    nm_stab = sum(1 for r in corrected_results if r['nm_in_stab'])
    print(f"    {nm_stab}/{len(corrected_results)}")
    
    # Cross-tab: nm_in_stab × T_coset_covered
    print(f"\n  Cross-tab: nm∈stab × T_coset_covered:")
    for nm_s in [True, False]:
        for tc in [True, False]:
            cnt = sum(1 for r in corrected_results if r['nm_in_stab'] == nm_s and r['T_coset_covered'] == tc)
            if cnt:
                print(f"    nm∈stab={nm_s}, T_coset_cov={tc}: {cnt}")
    
    print(f"\n  D_A coset coverage details:")
    for r in corrected_results[:20]:
        print(f"    n={r['n']:6d} A={r['A']:2d} h={r['h']:2d} stab={r['stab_size_mult']} "
              f"cosets={r['D_cosets_covered']}/{r['n_cosets']} "
              f"T_cov={r['T_coset_covered']} neg1_cov={r['neg1_coset_covered']} "
              f"nm∈stab={r['nm_in_stab']}")


if __name__ == '__main__':
    main()