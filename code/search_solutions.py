#!/usr/bin/env python3
"""
Exhaustive search for Erdős–Straus solutions in the residue class
n ≡ 1 (mod 12), n ≢ 0 (mod 5).

Generates search_results.json with solutions for all admissible n up to
a given bound, using the A-parameter framework.
"""

import json
from sympy import factorint, isprime, gcd
import itertools
import sys


def find_solution_for_A(n, A):
    """Find Erdős–Straus solution for given n, A. Returns (x, y, z) or None."""
    if (n + A) % 4 != 0:
        return None
    x = (n + A) // 4
    m = (n + A) // 4
    nx = n * m
    nx_factors = factorint(nx)
    T = (-n * m) % A

    primes = list(nx_factors.keys())
    max_exps = [2 * nx_factors[p] for p in primes]

    for combo in itertools.product(*[range(e + 1) for e in max_exps]):
        P = 1
        for p, a in zip(primes, combo):
            P *= p ** a
        if P == 0:
            continue
        if P % A == T % A:
            Q = nx * nx // P
            if Q == 0:
                continue
            y_num = P + nx
            z_num = Q + nx
            if y_num % A == 0 and z_num % A == 0:
                y = y_num // A
                z = z_num // A
                if y > 0 and z > 0:
                    return (x, y, z)
    return None


def search_range(max_n, A_values=None):
    """Search for solutions for all admissible n up to max_n."""
    if A_values is None:
        A_values = [a for a in range(3, 200, 4)]  # A ≡ 3 mod 4

    solutions = {}
    admissible = 0

    for n in range(13, max_n + 1):
        if n % 12 != 1 or n % 5 == 0:
            continue
        admissible += 1

        best_A = None
        best_sol = None

        for A in A_values:
            if gcd(n, A) > 1:
                continue
            sol = find_solution_for_A(n, A)
            if sol is not None:
                best_A = A
                best_sol = sol
                break

        if best_sol is not None:
            x, y, z = best_sol
            solutions[str(n)] = {
                'x': x, 'y': y, 'z': z,
                'A': best_A,
                'is_prime': bool(isprime(n))
            }

    return solutions, admissible


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    max_A = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    A_values = [a for a in range(3, max_A + 1, 4)]
    print(f"Searching n ≤ {max_n} with A ≤ {max_A}...")
    print(f"A values: {A_values}")

    solutions, admissible = search_range(max_n, A_values)

    output = {
        'max_n': max_n,
        'max_A': max_A,
        'admissible_count': admissible,
        'solution_count': len(solutions),
        'uncovered': admissible - len(solutions),
        'solutions': solutions,
    }

    outfile = sys.argv[3] if len(sys.argv) > 3 else 'search_results.json'
    with open(outfile, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults:")
    print(f"  Admissible: {admissible}")
    print(f"  Solutions found: {len(solutions)}")
    print(f"  Uncovered: {admissible - len(solutions)}")

    # Distribution of A
    from collections import Counter
    A_dist = Counter(s['A'] for s in solutions.values())
    print(f"\n  A distribution:")
    for A in sorted(A_dist.keys()):
        print(f"    A={A:3d}: {A_dist[A]:5d} ({100*A_dist[A]/len(solutions):.1f}%)")

    # Uncovered cases
    if admissible - len(solutions) > 0:
        uncovered = []
        for n in range(13, max_n + 1):
            if n % 12 != 1 or n % 5 == 0:
                continue
            if str(n) not in solutions:
                uncovered.append(n)
        print(f"\n  Uncovered values: {uncovered[:20]}{'...' if len(uncovered) > 20 else ''}")


if __name__ == "__main__":
    main()