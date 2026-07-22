#!/usr/bin/env python3
"""
Composite A Exact Recheck v2
=============================
Reproduce the exact first-working-A logic from layer4_sieve_expansion.py,
then for every composite-A first-working case, verify by exact T ∈ D_A.

This version uses the SAME detection logic as the original sieve
(order_2, direct_n_qnr, m_route, gap classification via centered sumset)
to ensure we correctly identify which cases had composite A as first working.
"""

import json
import time
from sympy import isprime, factorint, gcd, legendre_symbol, nextprime, jacobi_symbol
from collections import Counter, defaultdict
from math import lcm
from itertools import product as iterproduct

EXTENDED_A = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59,
              63, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107]
COMPOSITE_A_SET = {15, 27, 35, 39, 51, 55}

def find_primitive_root(p):
    if p == 2: return 1
    phi = p - 1
    factors = factorint(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    return None

def multiplicative_order(a, n):
    if gcd(a, n) > 1: return None
    val = a % n
    for i in range(1, n):
        if val == 1: return i
        val = (val * a) % n
    return None

def discrete_log_mod(g, target, p):
    val = 1
    for i in range(p - 1):
        if val == target % p: return i
        val = (val * g) % p
    return None

def classify_route_full(n, A):
    """Same logic as layer4_sieve_expansion.py classify_route."""
    if gcd(n, A) > 1:
        return None
    
    m = (n + A) // 4
    N = n * m
    factors_N = factorint(N)
    prime_factors = [(p, e) for p, e in factors_N.items() if gcd(p, A) == 1]
    
    if not prime_factors:
        return {'works': False, 'route': 'no_qnr', 'A': A, 'm': m}
    
    if not isprime(A):
        if A % 2 == 0:
            return None
        has_qnr = False
        qnr_p = None
        for p, e in prime_factors:
            j = int(jacobi_symbol(p, A))
            if j == -1:
                has_qnr = True
                qnr_p = p
                break
        n_qr = (int(jacobi_symbol(n, A)) == 1)
        direct = not n_qr
        if direct or has_qnr:
            return {'works': True, 'route': 'direct_n_qnr' if direct else 'm_route',
                    'A': A, 'm': m, 'n_qr': n_qr, 'qnr_factor': n if direct else qnr_p}
        return {'works': False, 'route': 'no_qnr', 'A': A, 'm': m, 'n_qr': n_qr}
    
    # Prime A
    g = find_primitive_root(A)
    if g is None:
        return None
    
    orders = [multiplicative_order(p, A) for p, _ in prime_factors]
    h = 1
    for o in orders:
        h = lcm(h, o)
    
    n_qr = (legendre_symbol(n, A) == 1)
    direct = not n_qr
    order_2 = [p for p, _ in prime_factors if multiplicative_order(p, A) == 2]
    factors_m = factorint(m)
    m_qnr = [p for p in factors_m if gcd(p, A) == 1 and legendre_symbol(p, A) == -1]
    
    if h <= 1:
        return {'works': False, 'route': 'no_qnr', 'A': A, 'm': m, 'n_qr': n_qr}
    if h % 2 != 0:
        return {'works': False, 'route': 'no_qnr', 'A': A, 'm': m, 'n_qr': n_qr}
    
    target = h // 2
    s_values = {}
    for p, e in prime_factors:
        dlg = discrete_log_mod(g, p, A)
        if dlg is None:
            return None
        s_values[p] = dlg % h
    
    s_list = [s_values[p] for p, _ in prime_factors]
    
    target_reachable = False
    shortest_len = float('inf')
    shortest_repr = None
    
    # Single-term
    for i, (p, e) in enumerate(prime_factors):
        for d in range(-e, e + 1):
            if (d * s_list[i]) % h == target:
                target_reachable = True
                if 1 < shortest_len:
                    shortest_len = 1
                    shortest_repr = [(p, d)]
    
    # Two-term
    if shortest_len > 2:
        for i in range(min(len(prime_factors), 8)):
            p1, e1 = prime_factors[i]
            for d1 in range(-e1, e1 + 1):
                for j in range(i + 1, min(len(prime_factors), 10)):
                    p2, e2 = prime_factors[j]
                    for d2 in range(-e2, e2 + 1):
                        if (d1 * s_list[i] + d2 * s_list[j]) % h == target:
                            target_reachable = True
                            if 2 < shortest_len:
                                shortest_len = 2
                                shortest_repr = [(p1, d1), (p2, d2)]
    
    # Three-term
    if shortest_len > 3 and len(prime_factors) <= 6:
        for i in range(min(len(prime_factors), 4)):
            p1, e1 = prime_factors[i]
            for d1 in range(-e1, e1 + 1):
                for j in range(i + 1, min(len(prime_factors), 5)):
                    p2, e2 = prime_factors[j]
                    for d2 in range(-e2, e2 + 1):
                        partial = (d1 * s_list[i] + d2 * s_list[j]) % h
                        remaining = (target - partial) % h
                        for k in range(j + 1, min(len(prime_factors), 6)):
                            p3, e3 = prime_factors[k]
                            s3 = s_list[k]
                            for d3 in range(-e3, e3 + 1):
                                if (d3 * s3) % h == remaining:
                                    target_reachable = True
                                    if 3 < shortest_len:
                                        shortest_len = 3
                                        shortest_repr = [(p1, d1), (p2, d2), (p3, d3)]
    
    if not target_reachable:
        return {'works': False, 'route': 'gap', 'A': A, 'm': m, 'h': h, 'n_qr': n_qr}
    
    if order_2:
        route = 'order_2'
    elif direct:
        route = 'direct_n_qnr'
    elif m_qnr:
        route = 'm_route'
    elif shortest_len == 2:
        route = 'two_term_centered'
    elif shortest_len and shortest_len <= 5:
        route = 'short_signed'
    else:
        route = 'long_signed'
    
    return {
        'works': True, 'route': route, 'A': A, 'm': m, 'h': h,
        'n_qr': n_qr, 'shortest_repr': shortest_repr,
        'shortest_len': shortest_len if shortest_repr else None,
    }

def compute_exact_D_A(n, A):
    """Compute exact T ∈ D_A((nx)^2) by enumerating all divisor residues mod A."""
    if gcd(n, A) > 1:
        return None
    
    m = (n + A) // 4
    N = n * m
    factors_N = factorint(N)
    prime_factors = [(p, e) for p, e in factors_N.items() if gcd(p, A) == 1]
    
    if not prime_factors:
        return {'works': False, 'D_size': 0}
    
    T = (-N) % A
    
    # Compute D_A by iterative multiplication
    current_set = {1}
    for p, e in prime_factors:
        powers = set()
        val = 1
        for a in range(2 * e + 1):
            powers.add(val % A)
            val = (val * p) % A
        new_set = set()
        for c in current_set:
            for pw in powers:
                new_set.add((c * pw) % A)
        current_set = new_set
    
    return {
        'works': T in current_set,
        'D_size': len(current_set),
        'T': T,
    }

def main():
    start_time = time.time()
    print("=" * 70)
    print("COMPOSITE A EXACT RECHECK v2")
    print("=" * 70)
    
    composite_cases = []
    counts = Counter()
    by_A = defaultdict(list)
    
    n = 13
    total_primes = 0
    last_progress = time.time()
    
    while n <= 10000000:
        if not isprime(n) or n % 12 != 1 or n % 5 == 0:
            n = int(nextprime(n))
            continue
        
        total_primes += 1
        
        # Find first working A using same logic as original sieve
        first_working = None
        for A in EXTENDED_A:
            if gcd(n, A) > 1:
                continue
            result = classify_route_full(n, A)
            if result is None:
                continue
            if result.get('works'):
                first_working = (A, result)
                break
        
        if first_working and first_working[0] in COMPOSITE_A_SET:
            A, res = first_working
            # Now do exact D_A check
            exact = compute_exact_D_A(n, A)
            
            composite_cases.append({
                'n': n,
                'A': A,
                'route': res.get('route'),
                'exact_works': exact['works'] if exact else None,
                'exact_D_size': exact['D_size'] if exact else None,
                'exact_T': exact['T'] if exact else None,
            })
            
            by_A[A].append(composite_cases[-1])
            counts['total'] += 1
            if exact and exact['works']:
                counts['exact_works'] += 1
            else:
                counts['exact_fails'] += 1
        
        n = int(nextprime(n))
        
        now = time.time()
        if now - last_progress > 60:
            elapsed = now - start_time
            print(f"  Progress: {total_primes} primes, n={n}, elapsed={elapsed:.0f}s, "
                  f"composite cases={counts['total']}, works={counts['exact_works']}, fails={counts['exact_fails']}")
            last_progress = now
    
    elapsed = time.time() - start_time
    print()
    print(f"{'=' * 70}")
    print(f"COMPLETE: {counts['total']} composite-A cases in {elapsed:.0f}s")
    print(f"{'=' * 70}")
    print(f"Total: {counts['total']}")
    print(f"Exact T ∈ D_A works: {counts['exact_works']}")
    print(f"Exact T ∈ D_A fails: {counts['exact_fails']}")
    print()
    print("By A:")
    for A in sorted(by_A.keys()):
        cases = by_A[A]
        works = sum(1 for c in cases if c['exact_works'])
        fails = sum(1 for c in cases if not c['exact_works'])
        print(f"  A={A}: {len(cases)} cases, {works} exact-works, {fails} exact-fails")
    
    # Write outputs
    with open('analysis/layer4/composite_A_exact_results.json', 'w') as f:
        json.dump({
            'total_checked': counts['total'],
            'exact_works': counts['exact_works'],
            'exact_fails': counts['exact_fails'],
            'by_A': {str(A): {
                'total': len(by_A[A]),
                'works': sum(1 for c in by_A[A] if c['exact_works']),
                'fails': sum(1 for c in by_A[A] if not c['exact_works']),
            } for A in by_A},
            'failures': [
                {'n': c['n'], 'A': c['A'], 'route': c['route'],
                 'D_size': c['exact_D_size'], 'T': c['exact_T']}
                for c in composite_cases if not c['exact_works']
            ],
        }, f, indent=2)
    print("Written: composite_A_exact_results.json")
    
    with open('analysis/layer4/composite_A_recheck_report.md', 'w') as f:
        f.write("# Composite A Exact Recheck Report\n\n")
        f.write(f"**Goal:** Verify all composite-A first-working cases by exact T ∈ D_A((nx)²) membership.\n\n")
        f.write(f"**Composite A values:** {sorted(COMPOSITE_A_SET)}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"| Metric | Count |\n|--------|-------|\n")
        f.write(f"| Total composite-A first-working cases | {counts['total']} |\n")
        f.write(f"| Exact T ∈ D_A confirms works | {counts['exact_works']} |\n")
        f.write(f"| Exact T ∈ D_A shows failure | {counts['exact_fails']} |\n\n")
        f.write(f"## By A breakdown\n\n")
        f.write("| A | Total | Exact Works | Exact Fails |\n|---|-------|-------------|-------------|\n")
        for A in sorted(by_A.keys()):
            cases = by_A[A]
            works = sum(1 for c in cases if c['exact_works'])
            fails = sum(1 for c in cases if not c['exact_works'])
            f.write(f"| {A} | {len(cases)} | {works} | {fails} |\n")
        f.write("\n")
        
        if counts['exact_fails'] == 0:
            f.write("## Result\n\n")
            f.write(f"**All {counts['total']} composite-A first-working cases confirmed by exact T ∈ D_A membership.**\n\n")
            f.write("Layer 4 coverage can now be upgraded from 99.33% exact + 0.67% heuristic to **100% exact computational coverage** up to 10M.\n")
        else:
            f.write(f"## Failures\n\n")
            f.write("| n | A | Route | D_size | T |\n|---|---|-------|---------|---|\n")
            for c in composite_cases:
                if not c['exact_works']:
                    f.write(f"| {c['n']} | {c['A']} | {c['route']} | {c['exact_D_size']} | {c['exact_T']} |\n")
    print("Written: composite_A_recheck_report.md")
    
    if counts['exact_fails'] == 0:
        print(f"\n*** ALL {counts['total']} COMPOSITE-A CASES CONFIRMED ***")
        print("*** Layer 4 upgraded to 100% exact computational coverage ***")

if __name__ == "__main__":
    main()