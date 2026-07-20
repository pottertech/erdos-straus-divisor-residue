#!/usr/bin/env python3
"""
Extend covering set verification to n ≤ 10,000,000.

Check that {3, 7, 11, 19, 23, 31} (prime A values only) covers all
prime n ≤ 10M with n ≡ 1 (mod 12), n ≢ 0 (mod 5).

For each n, check if T ∈ D_A for at least one prime A in the set.
If not, check composite A (15, 27) and extended A values.

This is a computationally intensive script — uses the C search tool
where possible and falls back to Python for the D_A check.
"""

import json
from math import gcd
from sympy import factorint, isprime
import time

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
        return None
    m = (n + A) // 4
    T = (-n * m) % A
    D = compute_D_A(n, A, tight=False)
    return T in D

def main():
    print("=" * 70)
    print("Covering Set Verification: n ≤ 10,000,000")
    print("=" * 70)
    
    A_primes = [3, 7, 11, 19, 23, 31]
    A_composites = [15, 27]
    A_all = A_primes + A_composites
    
    max_n = 10000000
    
    start_time = time.time()
    
    total_primes = 0
    covered_by_prime = 0
    covered_by_composite_only = 0
    not_covered = 0
    
    gap_cases_prime = []  # n values where all prime A fail
    not_covered_cases = []  # n values where ALL A fail
    
    # Statistics per A
    a_success_count = {A: 0 for A in A_all}
    a_gap_count = {A: 0 for A in A_all}
    
    # Distribution of how many prime A succeed
    from collections import Counter
    success_dist = Counter()
    
    for n in range(13, max_n + 1):
        if n % 12 != 1 or n % 5 == 0:
            continue
        if not isprime(n):
            continue
        
        total_primes += 1
        
        # Check each prime A
        n_prime_success = 0
        prime_results = {}
        for A in A_primes:
            result = check_T_in_DA(n, A)
            if result is True:
                n_prime_success += 1
                a_success_count[A] += 1
                prime_results[A] = 'success'
            elif result is False:
                a_gap_count[A] += 1
                prime_results[A] = 'gap'
            else:
                prime_results[A] = 'skip'
        
        success_dist[n_prime_success] += 1
        
        if n_prime_success > 0:
            covered_by_prime += 1
        else:
            gap_cases_prime.append(n)
            # Check composite A
            comp_success = False
            for A in A_composites:
                result = check_T_in_DA(n, A)
                if result is True:
                    comp_success = True
                    a_success_count[A] += 1
                    break
                elif result is False:
                    a_gap_count[A] += 1
            
            if comp_success:
                covered_by_composite_only += 1
            else:
                not_covered += 1
                not_covered_cases.append(n)
        
        # Progress report
        if total_primes % 10000 == 0:
            elapsed = time.time() - start_time
            print(f"  Progress: {total_primes} primes checked, "
                  f"{elapsed:.0f}s elapsed, "
                  f"covered={covered_by_prime + covered_by_composite_only}, "
                  f"uncovered={not_covered}")
    
    elapsed = time.time() - start_time
    
    # ===== RESULTS =====
    print(f"\n{'='*70}")
    print("RESULTS")
    print(f"{'='*70}")
    print(f"\nTotal primes n ≤ {max_n} with n ≡ 1 mod 12, n ≢ 0 mod 5: {total_primes}")
    print(f"Time: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"\nCovered by prime A alone: {covered_by_prime} ({100*covered_by_prime/total_primes:.2f}%)")
    print(f"Covered by composite A only: {covered_by_composite_only} ({100*covered_by_composite_only/total_primes:.2f}%)")
    print(f"NOT covered by any A: {not_covered} ({100*not_covered/total_primes:.2f}%)")
    print(f"Total covered: {covered_by_prime + covered_by_composite_only} ({100*(covered_by_prime + covered_by_composite_only)/total_primes:.2f}%)")
    
    print(f"\nDistribution of # of successful prime A per n:")
    for k in sorted(success_dist.keys()):
        print(f"  {k} successes: {success_dist[k]} n values ({100*success_dist[k]/total_primes:.2f}%)")
    
    print(f"\nPer-A success/gap counts:")
    for A in A_all:
        s = a_success_count[A]
        g = a_gap_count[A]
        total = s + g
        print(f"  A={A:3d}: {s:6d} successes, {g:6d} gaps ({100*s/max(1,total):.1f}% success)")
    
    if gap_cases_prime:
        print(f"\nCases needing composite A (all prime A gap): {len(gap_cases_prime)}")
        if len(gap_cases_prime) <= 50:
            for n in gap_cases_prime:
                print(f"  n={n}")
        else:
            print(f"  First 20: {gap_cases_prime[:20]}")
    
    if not_covered_cases:
        print(f"\n⚠️  UNCOVERED cases (all A fail): {len(not_covered_cases)}")
        for n in not_covered_cases:
            print(f"  n={n}")
            # Try extended A values
            for A in range(35, 200, 4):
                if gcd(n, A) > 1:
                    continue
                result = check_T_in_DA(n, A)
                if result is True:
                    print(f"    Rescued by A={A}")
                    break
            else:
                print(f"    No A up to 200 works!")
    else:
        print(f"\n✅ ALL {total_primes} primes n ≤ {max_n} covered by {{3, 7, 11, 15, 19, 23, 27, 31}}")
    
    # ===== SAVE =====
    output = {
        'max_n': max_n,
        'total_primes': total_primes,
        'covered_by_prime': covered_by_prime,
        'covered_by_composite_only': covered_by_composite_only,
        'not_covered': not_covered,
        'elapsed_seconds': elapsed,
        'success_distribution': {str(k): v for k, v in sorted(success_dist.items())},
        'per_A': {str(A): {'success': a_success_count[A], 'gap': a_gap_count[A]} for A in A_all},
        'gap_cases_prime': gap_cases_prime[:100],
        'not_covered_cases': not_covered_cases,
    }
    
    outfile = 'results/covering_set_10m.json'
    with open(outfile, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {outfile}")


if __name__ == '__main__':
    main()