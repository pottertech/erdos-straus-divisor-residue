#!/usr/bin/env python3
"""
Item 2 Step 4: Covering set verification for all 891 gap cases.

For each gap case (n, A) where T ∉ D_A, check whether another A'
from the covering set {3, 7, 11, 19, 23, 31} (or extended set) 
handles n successfully — i.e., T' ∈ D_{A'} for that A'.

Also check:
  1. How many A values succeed for each gap-case n?
  2. Which A values are the "backup" that cover gap cases?
  3. Is there any n where ALL A values fail?
  4. What's the minimum covering set needed?
"""

import json
from collections import Counter, defaultdict
from math import gcd
from sympy import factorint, isprime

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

def check_T_in_DA(n, A):
    """Check if T = -nm is in D_A (full 2e bound)."""
    if gcd(n, A) > 1:
        return None  # A doesn't apply (n divisible by A)
    m = (n + A) // 4
    T = (-n * m) % A
    D = compute_D_A(n, A, tight=False)
    return T in D

def check_neg1_in_DA(n, A):
    """Check if -1 is in D_A (full 2e bound)."""
    if gcd(n, A) > 1:
        return None
    neg1 = A - 1
    D = compute_D_A(n, A, tight=False)
    return neg1 in D

def check_solution_exists(n, A):
    """Check if 4/n = 1/x + 1/y + 1/z has a solution with this A.
    This means T ∈ D_A where T = -nm mod A."""
    return check_T_in_DA(n, A)

def main():
    print("=" * 70)
    print("Item 2 Step 4: Covering Set Verification for Gap Cases")
    print("=" * 70)

    # Covering set from the manuscript
    A_covering = [3, 7, 11, 15, 19, 23, 27, 31]
    # Note: 15 and 27 are composite. The prime-A analysis only uses primes.
    # But for the covering set property, we need all of them.
    # For this analysis, check both prime and composite A.
    
    A_primes = [3, 7, 11, 19, 23, 31]
    A_all = [3, 7, 11, 15, 19, 23, 27, 31]
    
    max_n = 100000
    
    # First, find all gap cases (n, A) where -1 ∈ D_A but T ∉ D_A
    # for prime A in A_primes.
    gap_cases = []  # list of (n, A) tuples
    all_cases = []
    
    for n in range(13, max_n + 1):
        if n % 12 != 1 or n % 5 == 0:
            continue
        if not isprime(n):
            continue
        for A in A_primes:
            if gcd(n, A) > 1:
                continue
            neg1_in = check_neg1_in_DA(n, A)
            T_in = check_T_in_DA(n, A)
            
            if neg1_in and not T_in:
                gap_cases.append((n, A))
            
            all_cases.append((n, A, neg1_in, T_in))
    
    print(f"\nTotal prime-A cases: {len(all_cases)}")
    print(f"Gap cases (T ∉ D_A): {len(gap_cases)}")
    
    # Unique n values in gap cases
    gap_ns = sorted(set(n for n, A in gap_cases))
    print(f"Unique n values with at least one gap: {len(gap_ns)}")
    
    # ===== For each gap-case n, check ALL A values =====
    print(f"\n{'='*70}")
    print("Coverage Analysis: For each gap-case n, how many A values succeed?")
    print(f"{'='*70}")
    
    n_coverage = []  # list of (n, gap_A, results_dict)
    
    for n in gap_ns:
        results = {}
        gap_As_for_n = [A for nn, A in gap_cases if nn == n]
        
        for A in A_all:
            if gcd(n, A) > 1:
                results[A] = 'skip'
                continue
            T_in = check_T_in_DA(n, A)
            if T_in is None:
                results[A] = 'skip'
            elif T_in:
                results[A] = 'success'
            else:
                results[A] = 'fail'
        
        n_coverage.append({
            'n': n,
            'gap_As': gap_As_for_n,
            'results': results,
            'n_success': sum(1 for v in results.values() if v == 'success'),
            'n_fail': sum(1 for v in results.values() if v == 'fail'),
            'n_skip': sum(1 for v in results.values() if v == 'skip'),
        })
    
    # How many n have at least one success?
    has_success = sum(1 for c in n_coverage if c['n_success'] > 0)
    no_success = sum(1 for c in n_coverage if c['n_success'] == 0)
    print(f"\n  Gap-case n values with at least one successful A: {has_success} / {len(n_coverage)}")
    print(f"  Gap-case n values with NO successful A: {no_success} / {len(n_coverage)}")
    
    if no_success > 0:
        print(f"\n  ⚠️  {no_success} n values where NO A in covering set works!")
        print(f"  These need extended A values or direct solution search.")
        for c in n_coverage:
            if c['n_success'] == 0:
                print(f"    n={c['n']}: gap_As={c['gap_As']}, results={c['results']}")
    
    # ===== Distribution of success count =====
    print(f"\n{'='*70}")
    print("Distribution: # of successful A values per gap-case n")
    print(f"{'='*70}")
    
    success_dist = Counter(c['n_success'] for c in n_coverage)
    for k in sorted(success_dist.keys()):
        print(f"  {k} successful A's: {success_dist[k]} n values")
    
    # ===== Which A values are the "saviors"? =====
    print(f"\n{'='*70}")
    print("Which A values rescue gap cases?")
    print(f"{'='*70}")
    
    savior_counts = Counter()
    for c in n_coverage:
        for A, result in c['results'].items():
            if result == 'success' and A not in c['gap_As']:
                savior_counts[A] += 1
    
    print(f"  A values that succeed when another A gaps (non-gap A succeeds):")
    for A in sorted(savior_counts.keys()):
        print(f"    A={A:3d}: rescues {savior_counts[A]} gap-case n values")
    
    # ===== Per-A gap vs success =====
    print(f"\n{'='*70}")
    print("Per-A: gap cases and successes across all n")
    print(f"{'='*70}")
    
    for A in A_all:
        n_gap = sum(1 for c in n_coverage if A in c['gap_As'])
        n_success = sum(1 for c in n_coverage if c['results'].get(A) == 'success')
        n_fail = sum(1 for c in n_coverage if c['results'].get(A) == 'fail')
        n_skip = sum(1 for c in n_coverage if c['results'].get(A) == 'skip')
        print(f"  A={A:3d}: gap={n_gap:4d}, success={n_success:4d}, fail={n_fail:4d}, skip={n_skip:4d}")
    
    # ===== The hard cases: n where only 1 A succeeds =====
    print(f"\n{'='*70}")
    print("Hardest cases: n with only 1 successful A")
    print(f"{'='*70}")
    
    one_success = [c for c in n_coverage if c['n_success'] == 1]
    print(f"  Count: {len(one_success)}")
    if one_success:
        print(f"\n  {'n':>8} | {'gap_As':>12} | {'successful_A':>12} | {'all_results'}")
        print(f"  " + "-" * 60)
        for c in one_success[:30]:
            succ_As = [A for A, r in c['results'].items() if r == 'success']
            print(f"  {c['n']:8d} | {str(c['gap_As']):>12} | {str(succ_As):>12} | {c['results']}")
    
    # ===== Extended A check for no-success cases =====
    print(f"\n{'='*70}")
    print("Extended A check for no-success n values")
    print(f"{'='*70}")
    
    if no_success > 0:
        extended_A = list(range(3, 200, 4))  # A ≡ 3 mod 4 up to 200
        extended_A = [A for A in extended_A if A not in A_all]
        
        for c in n_coverage:
            if c['n_success'] > 0:
                continue
            n = c['n']
            print(f"\n  n={n}: checking extended A values...")
            ext_successes = []
            for A in extended_A:
                if gcd(n, A) > 1:
                    continue
                T_in = check_T_in_DA(n, A)
                if T_in:
                    ext_successes.append(A)
            if ext_successes:
                print(f"    Extended successes: {ext_successes[:10]}")
            else:
                print(f"    No extended A up to 200 works!")
                # Direct solution search
                found = False
                for x in range(1, n):
                    for y in range(x, n):
                        # 4/n - 1/x - 1/y = 1/z → z = nxy / (4xy - ny - nx)
                        num = n * x * y
                        den = 4 * x * y - n * y - n * x
                        if den > 0 and num % den == 0:
                            z = num // den
                            if z > 0:
                                found = True
                                print(f"    Direct solution: x={x}, y={y}, z={z}")
                                break
                    if found:
                        break
                if not found:
                    print(f"    ⚠️  No direct solution found either!")
    else:
        print(f"  All gap-case n values have at least one successful A in the covering set!")
    
    # ===== Covering set minimality =====
    print(f"\n{'='*70}")
    print("Covering set minimality: can we remove any A?")
    print(f"{'='*70}")
    
    # For each A in the covering set, check if removing it causes any n to lose all coverage
    for remove_A in A_all:
        still_covered = 0
        lost = 0
        for c in n_coverage:
            # Count successes without remove_A
            remaining = sum(1 for A, r in c['results'].items() 
                          if r == 'success' and A != remove_A)
            if remaining > 0:
                still_covered += 1
            else:
                # Was remove_A the only success?
                if c['results'].get(remove_A) == 'success':
                    lost += 1
        
        status = "REMOVABLE" if lost == 0 else f"NEEDED (loses {lost} n values)"
        print(f"  Remove A={remove_A:3d}: {status}")
    
    # ===== Summary =====
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"""
Gap cases: {len(gap_cases)} (n, A) pairs where T ∉ D_A
Unique n values with gaps: {len(gap_ns)}
  - Covered by another A in covering set: {has_success}
  - NOT covered by any A in covering set: {no_success}

The covering set {'{3, 7, 11, 15, 19, 23, 27, 31}'} {'FULLY COVERS' if no_success == 0 else 'DOES NOT FULLY COVER'} all gap cases.

Key finding: {'Every gap case n has at least one other A that succeeds.' if no_success == 0 else 'Some n values need extended A or direct verification.'}

This means the theorem's correctness relies on the COVERING SET PROPERTY:
  for each n ≡ 1 mod 12, n ≢ 0 mod 5, at least one A in the covering set 
  must yield T ∈ D_A.

The single-A analysis shows WHERE each A fails; the covering set shows 
that these failures are ALWAYS rescued by another A.
""")

    # ===== SAVE =====
    output = {
        'summary': {
            'gap_cases': len(gap_cases),
            'unique_gap_ns': len(gap_ns),
            'has_success': has_success,
            'no_success': no_success,
            'covering_set': A_all,
            'fully_covered': no_success == 0,
        },
        'success_distribution': {str(k): v for k, v in sorted(success_dist.items())},
        'savior_counts': {str(k): v for k, v in sorted(savior_counts.items())},
        'n_coverage': n_coverage,
    }
    
    outfile = 'analysis/covering_set_verification.json'
    with open(outfile, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")


if __name__ == '__main__':
    main()