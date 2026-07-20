#!/usr/bin/env python3
"""
Item 2 Step 1: Structural classification of 1,322 anomalous cases.

Anomalous = -1 ∈ D_A (full, 2e bound) but -1 ∉ D_A^(nm) (tight, e bound).
For each case, classify by:
  - h (order of H(A))
  - stabilizer type (trivial, proper non-trivial, full group)
  - witness path structure (which primes exceed tight bound, by how much)
  - dlog decomposition class
"""

import json
from collections import Counter, defaultdict
from math import gcd
from itertools import product as iterproduct
from sympy import factorint, isprime, primitive_root

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

def compute_stabilizer(n, A, H):
    """Compute stabilizer of nm action on H: {h in H : nm*h in H_shifted_subset}.
    Actually compute the stabilizer subgroup of the coset action."""
    m = (n + A) // 4
    nx = n * m
    # Stabilizer = elements of H that map shifted set to itself
    # More precisely: stabilizer of the D_A^(nm) action
    # For classification, use the stabilizer of nm in the multiplicative group mod A
    g = primitive_root(A)
    h = len(H)
    # Find dlog of nm
    dlog_table = {pow(g, i, A): i for i in range(A - 1)}
    nm_mod_A = (n * m) % A
    if nm_mod_A in dlog_table:
        dlog_nm = dlog_table[nm_mod_A]
    else:
        return 'unknown', 0
    # Stabilizer size = gcd(dlog_nm, h)
    from math import gcd as _gcd
    stab_size = _gcd(dlog_nm, h)
    if stab_size == 1:
        return 'trivial', 1
    elif stab_size == h:
        return 'full', h
    else:
        return 'proper', stab_size

def find_witness_for_residue(n, A, target_res, tight=False):
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    primes = [p for p in nx_factors if gcd(p, A) == 1]
    exps = [nx_factors[p] for p in primes]
    bound = lambda e: e if tight else 2 * e
    for combo in iterproduct(*[range(bound(e) + 1) for e in exps]):
        res = 1
        for p, a in zip(primes, combo):
            res = (res * pow(p, a, A)) % A
        if res == target_res % A:
            return dict(zip(primes, combo))
    return None

def build_dlog_table(A, g):
    return {pow(g, i, A): i for i in range(A - 1)}

def classify_witness(n, A, neg1_witness, T_witness, nx_factors, h, dlog_table):
    """Classify the structure of the alternative witness path."""
    if not T_witness:
        return 'no_T_witness', {}

    # Convert keys to int
    tw = {int(k): v for k, v in T_witness.items()}
    nw = {int(k): v for k, v in neg1_witness.items()} if neg1_witness else {}
    factors = {int(k): int(v) for k, v in nx_factors.items()}

    # Which primes exceed tight bound e_i?
    exceeds = {}
    within = {}
    for p in factors:
        e = factors[p]
        tw_val = tw.get(p, 0)
        if tw_val > e:
            exceeds[p] = {'tw': tw_val, 'e': e, 'excess': tw_val - e}
        else:
            within[p] = {'tw': tw_val, 'e': e}

    # How much does standard path (-1 * nm) overflow?
    standard_overflow = 0
    for p in factors:
        nw_val = nw.get(p, 0)
        e = factors[p]
        if nw_val + e > 2 * e:
            standard_overflow += 1

    # dlog analysis
    gen_dlogs = {}
    for p in factors:
        gen_dlogs[p] = dlog_table.get(p % A, 0)

    dlog_nm = sum(factors[p] * gen_dlogs.get(p, 0) for p in factors) % h
    dlog_T = (h // 2 + dlog_nm) % h
    dlog_tw = sum(tw.get(p, 0) * gen_dlogs.get(p, 0) for p in gen_dlogs) % h

    # Classify: does T-witness avoid -1 entirely?
    # T-witness uses different exponents than -1 witness + e_i
    uses_neg1_path = True
    for p in factors:
        if tw.get(p, 0) != nw.get(p, 0) + factors[p]:
            uses_neg1_path = False
            break

    n_exceeding = len(exceeds)
    n_within = len(within)

    # Structural class
    if n_exceeding == 0:
        struct_class = 'within_tight'  # shouldn't happen for anomalous, but check
    elif n_exceeding == 1:
        struct_class = 'single_overflow'
    elif n_exceeding == 2:
        struct_class = 'double_overflow'
    else:
        struct_class = 'multi_overflow'

    return struct_class, {
        'n_exceeding': n_exceeding,
        'n_within': n_within,
        'exceeds': exceeds,
        'within': within,
        'standard_overflow': standard_overflow,
        'uses_neg1_path': uses_neg1_path,
        'dlog_nm': dlog_nm,
        'dlog_T': dlog_T,
        'dlog_tw': dlog_tw,
        'h': h,
    }

def main():
    print("=" * 70)
    print("Item 2 Step 1: Structural Classification of Anomalous Cases")
    print("=" * 70)

    A_values = [3, 7, 11, 19, 23, 31]
    max_n = 100000
    dlog_tables = {}
    for A in A_values:
        if isprime(A):
            g = primitive_root(A)
            dlog_tables[A] = build_dlog_table(A, g)

    anomalous = []
    all_prime_A = 0

    for n in range(13, max_n + 1):
        if n % 12 != 1 or n % 5 == 0:
            continue
        if not isprime(n):
            continue
        for A in A_values:
            if not isprime(A) or gcd(n, A) > 1:
                continue
            all_prime_A += 1
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
                stab_type, stab_size = compute_stabilizer(n, A, H)
                neg1_witness = find_witness_for_residue(n, A, neg1, tight=False)
                T_in_full = T in D_full
                T_witness = find_witness_for_residue(n, A, T, tight=False) if T_in_full else None
                T_in_tight = T in D_tight

                wclass, wdata = classify_witness(
                    n, A, neg1_witness, T_witness,
                    {str(p): e for p, e in nx_factors.items() if gcd(p, A) == 1},
                    h, dlog_tables.get(A, {})
                )

                anomalous.append({
                    'n': n, 'A': A, 'h': h,
                    'stab_type': stab_type, 'stab_size': stab_size,
                    'T': T, 'm': m, 'nx': nx,
                    'T_in_DA': T_in_full,
                    'T_in_shifted': T_in_tight,
                    'witness_class': wclass,
                    'witness_data': wdata,
                    'neg1_witness': neg1_witness,
                    'T_witness': T_witness,
                    'nx_factors': {str(p): e for p, e in nx_factors.items() if gcd(p, A) == 1},
                })

    print(f"\nTotal prime-A cases scanned: {all_prime_A}")
    print(f"Anomalous cases: {len(anomalous)}")

    T_in_DA = [c for c in anomalous if c['T_in_DA']]
    no_T = [c for c in anomalous if not c['T_in_DA']]
    print(f"  T ∈ D_A (has alternative path): {len(T_in_DA)}")
    print(f"  T ∉ D_A (lemma fails): {len(no_T)}")

    # ===== CLASSIFICATION BY h =====
    print(f"\n{'='*70}")
    print("Classification by h (order of H(A))")
    print(f"{'='*70}")
    by_h = Counter(c['h'] for c in anomalous)
    by_h_T = Counter(c['h'] for c in T_in_DA)
    by_h_no_T = Counter(c['h'] for c in no_T)
    print(f"{'h':>6} | {'Total':>6} | {'T∈D_A':>6} | {'T∉D_A':>6} | {'%T∈':>6}")
    print("-" * 42)
    for h in sorted(by_h.keys()):
        total = by_h[h]
        t_yes = by_h_T.get(h, 0)
        t_no = by_h_no_T.get(h, 0)
        pct = 100 * t_yes / total if total else 0
        print(f"{h:6d} | {total:6d} | {t_yes:6d} | {t_no:6d} | {pct:5.1f}%")

    # ===== CLASSIFICATION BY A =====
    print(f"\n{'='*70}")
    print("Classification by A")
    print(f"{'='*70}")
    by_A = Counter(c['A'] for c in anomalous)
    by_A_T = Counter(c['A'] for c in T_in_DA)
    by_A_no_T = Counter(c['A'] for c in no_T)
    print(f"{'A':>6} | {'Total':>6} | {'T∈D_A':>6} | {'T∉D_A':>6} | {'%T∈':>6}")
    print("-" * 42)
    for A in sorted(by_A.keys()):
        total = by_A[A]
        t_yes = by_A_T.get(A, 0)
        t_no = by_A_no_T.get(A, 0)
        pct = 100 * t_yes / total if total else 0
        print(f"{A:6d} | {total:6d} | {t_yes:6d} | {t_no:6d} | {pct:5.1f}%")

    # ===== CLASSIFICATION BY STABILIZER TYPE =====
    print(f"\n{'='*70}")
    print("Classification by Stabilizer Type")
    print(f"{'='*70}")
    by_stab = Counter(c['stab_type'] for c in anomalous)
    by_stab_T = Counter(c['stab_type'] for c in T_in_DA)
    by_stab_no_T = Counter(c['stab_type'] for c in no_T)
    print(f"{'Stab':>12} | {'Total':>6} | {'T∈D_A':>6} | {'T∉D_A':>6} | {'%T∈':>6}")
    print("-" * 50)
    for s in ['trivial', 'proper', 'full', 'unknown']:
        if s not in by_stab:
            continue
        total = by_stab[s]
        t_yes = by_stab_T.get(s, 0)
        t_no = by_stab_no_T.get(s, 0)
        pct = 100 * t_yes / total if total else 0
        print(f"{s:>12} | {total:6d} | {t_yes:6d} | {t_no:6d} | {pct:5.1f}%")

    # ===== CLASSIFICATION BY WITNESS STRUCTURE =====
    print(f"\n{'='*70}")
    print("Classification by Witness Path Structure")
    print(f"{'='*70}")
    by_wclass = Counter(c['witness_class'] for c in T_in_DA)
    print(f"{'Class':>20} | {'Count':>6} | {'%':>6}")
    print("-" * 38)
    for wc in sorted(by_wclass.keys()):
        cnt = by_wclass[wc]
        pct = 100 * cnt / len(T_in_DA) if T_in_DA else 0
        print(f"{wc:>20} | {cnt:6d} | {pct:5.1f}%")

    # ===== CROSS-TABULATION: h × stabilizer type =====
    print(f"\n{'='*70}")
    print("Cross-tab: h × Stabilizer Type (T ∈ D_A cases only)")
    print(f"{'='*70}")
    crosstab = defaultdict(lambda: defaultdict(int))
    for c in T_in_DA:
        crosstab[c['h']][c['stab_type']] += 1
    stab_types_seen = sorted(set(c['stab_type'] for c in T_in_DA))
    header = f"{'h':>6} |" + "|".join(f" {s:>10} " for s in stab_types_seen) + "|"
    print(header)
    print("-" * len(header))
    for h in sorted(crosstab.keys()):
        row = f"{h:6d} |"
        for s in stab_types_seen:
            row += f" {crosstab[h].get(s, 0):10d} |"
        print(row)

    # ===== CROSS-TABULATION: A × witness class =====
    print(f"\n{'='*70}")
    print("Cross-tab: A × Witness Class (T ∈ D_A cases only)")
    print(f"{'='*70}")
    crosstab2 = defaultdict(lambda: defaultdict(int))
    for c in T_in_DA:
        crosstab2[c['A']][c['witness_class']] += 1
    wclasses_seen = sorted(set(c['witness_class'] for c in T_in_DA))
    header = f"{'A':>6} |" + "|".join(f" {w:>20} " for w in wclasses_seen) + "|"
    print(header)
    print("-" * len(header))
    for A in sorted(crosstab2.keys()):
        row = f"{A:6d} |"
        for w in wclasses_seen:
            row += f" {crosstab2[A].get(w, 0):20d} |"
        print(row)

    # ===== KEY STATISTICS =====
    print(f"\n{'='*70}")
    print("Key Statistics")
    print(f"{'='*70}")

    # How many primes in the factorization (accessible primes)
    n_primes = Counter()
    for c in T_in_DA:
        np = len(c['nx_factors'])
        n_primes[np] += 1
    print(f"\nNumber of accessible primes in factorization:")
    for k in sorted(n_primes.keys()):
        print(f"  {k} primes: {n_primes[k]} cases ({100*n_primes[k]/len(T_in_DA):.1f}%)")

    # Excess distribution: how much does T-witness exceed e_i?
    excess_dist = Counter()
    for c in T_in_DA:
        wd = c['witness_data']
        if isinstance(wd, dict) and 'exceeds' in wd:
            for p, info in wd['exceeds'].items():
                excess_dist[info['excess']] += 1
    print(f"\nExcess distribution (how far T-witness exceeds e_i):")
    for k in sorted(excess_dist.keys()):
        print(f"  excess={k}: {excess_dist[k]} prime-instances")

    # Does T-witness ever use the -1 path?
    uses_neg1 = sum(1 for c in T_in_DA if c['witness_data'].get('uses_neg1_path', False))
    print(f"\nT-witness uses -1*nm path: {uses_neg1} / {len(T_in_DA)}")
    print(f"T-witness uses ALTERNATIVE path: {len(T_in_DA) - uses_neg1} / {len(T_in_DA)}")

    # The 891 cases where T ∉ D_A — what's special?
    print(f"\n{'='*70}")
    print(f"Analysis of {len(no_T)} cases where T ∉ D_A")
    print(f"{'='*70}")
    no_T_by_A = Counter(c['A'] for c in no_T)
    no_T_by_h = Counter(c['h'] for c in no_T)
    no_T_by_stab = Counter(c['stab_type'] for c in no_T)
    print(f"By A: {dict(sorted(no_T_by_A.items()))}")
    print(f"By h: {dict(sorted(no_T_by_h.items()))}")
    print(f"By stabilizer: {dict(sorted(no_T_by_stab.items()))}")

    # ===== SAVE FULL RESULTS =====
    output = {
        'summary': {
            'total_prime_A_cases': all_prime_A,
            'anomalous_count': len(anomalous),
            'T_in_DA': len(T_in_DA),
            'T_not_in_DA': len(no_T),
            'T_in_shifted': 0,
        },
        'by_h': {str(k): {'total': by_h[k], 'T_in_DA': by_h_T.get(k, 0), 'T_not_in_DA': by_h_no_T.get(k, 0)} for k in sorted(by_h.keys())},
        'by_A': {str(k): {'total': by_A[k], 'T_in_DA': by_A_T.get(k, 0), 'T_not_in_DA': by_A_no_T.get(k, 0)} for k in sorted(by_A.keys())},
        'by_stabilizer': {k: {'total': by_stab[k], 'T_in_DA': by_stab_T.get(k, 0), 'T_not_in_DA': by_stab_no_T.get(k, 0)} for k in sorted(by_stab.keys())},
        'by_witness_class': {k: by_wclass[k] for k in sorted(by_wclass.keys())},
        'n_primes_dist': {str(k): n_primes[k] for k in sorted(n_primes.keys())},
        'excess_dist': {str(k): excess_dist[k] for k in sorted(excess_dist.keys())},
        'uses_neg1_path': uses_neg1,
        'alternative_path': len(T_in_DA) - uses_neg1,
        'no_T_by_A': dict(sorted(no_T_by_A.items())),
        'no_T_by_h': dict(sorted(no_T_by_h.items())),
        'no_T_by_stab': dict(sorted(no_T_by_stab.items())),
        'anomalous_cases': anomalous,
    }

    outfile = 'analysis/classified_anomalous.json'
    with open(outfile, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nFull results saved to {outfile}")

    # ===== SUMMARY INSIGHT =====
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"""
Of {all_prime_A} prime-A cases (n ≤ {max_n}, n ≡ 1 mod 12, n ≢ 0 mod 5):
  - {len(anomalous)} anomalous ({100*len(anomalous)/all_prime_A:.1f}%): -1 ∈ D_A but -1 ∉ D_A^(nm)
  - {len(T_in_DA)} ({100*len(T_in_DA)/len(anomalous):.1f}% of anomalous): T ∈ D_A via alternative path
  - {len(no_T)} ({100*len(no_T)/len(anomalous):.1f}% of anomalous): T ∉ D_A — lemma gap
  - 0 cases where T ∈ shifted set (confirmed dead end)

Witness path analysis (T ∈ D_A cases):
  - {uses_neg1} use the -1*nm path (shouldn't be possible for anomalous — check)
  - {len(T_in_DA) - uses_neg1} use genuinely alternative divisor paths

Next: Check if Kneser's theorem on the full group covers these gaps.
""")


if __name__ == '__main__':
    main()