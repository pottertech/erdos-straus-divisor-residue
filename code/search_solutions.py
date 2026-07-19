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
    wit = find_witness(n, A)
    if wit is None:
        return None
    return (wit['x'], wit['y'], wit['z'])


def find_witness(n, A):
    """Find Erdős–Straus solution and return full witness details.
    
    Returns a witness dict with all intermediate values:
        x, y, z: the decomposition 4/n = 1/x + 1/y + 1/z
        A: the A-parameter used
        P, Q: the divisor pair of (nx)² with P ≡ T (mod A)
        T: target residue -n²·4⁻¹ mod A
        nx = n*m, m = (n+A)/4
    Or None if no solution found for this A.
    """
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
                    return {
                        'x': x, 'y': y, 'z': z,
                        'A': A, 'P': P, 'Q': Q,
                        'T': T, 'nx': nx, 'm': m,
                    }
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
            wit = find_witness(n, A)
            if wit is not None:
                best_A = A
                best_sol = wit
                break

        if best_sol is not None:
            solutions[str(n)] = {
                'x': best_sol['x'], 'y': best_sol['y'], 'z': best_sol['z'],
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


def print_witness(n, max_A=200):
    """Print full witness details for a specific n."""
    A_values = [a for a in range(3, max_A + 1, 4)]
    print(f"Witness search for n={n}:")
    print(f"  n mod 12 = {n % 12}, n mod 5 = {n % 5}")
    for A in A_values:
        if gcd(n, A) > 1:
            continue
        wit = find_witness(n, A)
        if wit is not None:
            print(f"\n  Found with A={A}:")
            print(f"    x = {wit['x']}, y = {wit['y']}, z = {wit['z']}")
            print(f"    P = {wit['P']}, Q = {wit['Q']}")
            print(f"    T = {wit['T']} (target residue mod A)")
            print(f"    nx = {wit['nx']}, m = {wit['m']}")
            from fractions import Fraction
            lhs = Fraction(4, n)
            rhs = Fraction(1, wit['x']) + Fraction(1, wit['y']) + Fraction(1, wit['z'])
            print(f"    Verify: 4/{n} = 1/{wit['x']} + 1/{wit['y']} + 1/{wit['z']} = {rhs}  {'✅' if lhs == rhs else '❌'}")
            return wit
    print(f"\n  No solution found with A ≤ {max_A}")
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--witness':
        n = int(sys.argv[2])
        max_A = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        print_witness(n, max_A)
    else:
        main()
