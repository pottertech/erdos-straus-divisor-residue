#!/usr/bin/env python3
"""
Verification of the Bounded Divisor-Residue Lemma.

Tests the implication -1 ∈ H(A) ⟹ -1 ∈ D_A for prime A,
categorizing cases into:
  - Case 1: h = 2 (proven general)
  - Case 2a: order-2 QNR exists (proven general)
  - Case 2b: Kneser condition (proven general under hypotheses)
  - Case 2c: Computational verification (remaining cases)
"""

from sympy import factorint, isprime, gcd, primitive_root
from math import lcm
from functools import reduce
import json
import sys


def compute_orders(n, A, nx_factors):
    """Compute multiplicative orders of prime factors of nx mod A."""
    orders = {}
    for p, e in nx_factors.items():
        if gcd(p, A) > 1:
            continue
        d = 1
        v = p % A
        c = v
        while c != 1 and d < A:
            c = (c * v) % A
            d += 1
        orders[p] = (d, e)
    return orders


def compute_D_A(n, A):
    """Compute bounded divisor-residue set D_A((nx)²)."""
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    
    res = {1}
    for p, e in nx_factors.items():
        if gcd(p, A) > 1:
            continue
        new = set()
        for f in range(2 * e + 1):
            pf = pow(p, f, A)
            for r in res:
                new.add((r * pf) % A)
        res = new
    return res


def compute_H_A(n, A):
    """Compute subgroup H(A)."""
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


def verify_lemma(max_n=100000, A_values=None):
    """Verify Bounded Divisor-Residue Lemma."""
    if A_values is None:
        A_values = [3, 7, 11, 15, 19, 23, 27, 31]
    
    cat1 = 0      # h = 2 (proven general)
    cat2a = 0     # order-2 QNR (proven general)
    cat2b_kneser = 0  # Kneser condition (proven general)
    cat2b_comp = 0   # Computational verification
    failures = 0
    
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
            orders = compute_orders(n, A, nx_factors)
            
            h = reduce(lcm, [d for d, _ in orders.values()]) if orders else 1
            if h % 2 != 0:
                continue  # -1 not in H(A)
            
            D = compute_D_A(n, A)
            H = compute_H_A(n, A)
            neg1 = A - 1
            
            if neg1 not in H:
                continue  # -1 not in H(A), skip
            
            if neg1 not in D:
                failures += 1
                print(f"  FAILURE: n={n} A={A} h={h}")
                continue
            
            # Categorize
            if h == 2:
                cat1 += 1
            elif any(d == 2 for d, _ in orders.values()):
                cat2a += 1
            else:
                m_val = h // 2
                k = len(orders)
                sum_range = sum(2 * e + 1 for _, e in orders.values())
                if sum_range >= m_val + k - 1:
                    cat2b_kneser += 1
                else:
                    cat2b_comp += 1
    
    total = cat1 + cat2a + cat2b_kneser + cat2b_comp
    
    print(f"\n{'='*60}")
    print(f"Bounded Divisor-Residue Lemma Verification")
    print(f"{'='*60}")
    print(f"  n range: 13 to {max_n}")
    print(f"  A values: {A_values}")
    print(f"  Prime-A cases: {total}")
    print(f"  Failures: {failures}")
    print()
    print(f"  Case 1 (h=2, PROVEN): {cat1}")
    print(f"  Case 2a (order-2 QNR, PROVEN): {cat2a}")
    print(f"  Case 2b-Kneser (PROVEN): {cat2b_kneser}")
    print(f"  Case 2b-Computational: {cat2b_comp}")
    print(f"  Proven generally: {cat1 + cat2a + cat2b_kneser} ({100*(cat1+cat2a+cat2b_kneser)/total:.1f}%)" if total > 0 else "")
    print(f"  Computational only: {cat2b_comp} ({100*cat2b_comp/total:.1f}%)" if total > 0 else "")
    
    return failures


if __name__ == "__main__":
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    failures = verify_lemma(max_n)
    if failures > 0:
        print(f"\n❌ {failures} failures detected!")
        sys.exit(1)
    else:
        print(f"\n✅ All cases verified — zero failures!")