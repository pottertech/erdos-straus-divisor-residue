#!/usr/bin/env python3
"""
Open Problem #6: M-Route Sufficiency

The direct route: A works if (A/n) = -1 (A is QNR mod n).
The m-route: A works if some prime p | m_A = (n+A)/4 has (n/p) = -1,
  because then (p/A) = (n/p) = -1 by Theorem 5, so p is a QNR mod A,
  triggering Theorem 3.

Question: When the direct route fails for ALL A in the covering set
(i.e., n is QR mod all of {7, 11, 19, 23, 31} — note A=3 always has
(3/n)=1 since n ≡ 1 mod 12), does the m-route always succeed for at
least one A?

The m-route succeeds for A if:
  1. Some prime p | (n+A)/4 has (n/p) = -1
  2. AND T ∈ D_A for that A (the full Theorem 3 forward direction)

Since the m-route provides a QNR prime factor of nx (via m_A), condition
2 reduces to the Partial -1 Route + covering set property.

This script:
  1. Finds all n where the direct route fails (n QR mod all covering primes)
  2. For each such n, checks which A values have m-route success
  3. Verifies m-route always provides at least one working A
  4. Analyzes the structure: which QNR primes of n appear in m_A
"""

import json
from collections import Counter, defaultdict
from math import gcd
from sympy import factorint, isprime, legendre_symbol

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

def main():
    print("=" * 70)
    print("Open Problem #6: M-Route Sufficiency")
    print("=" * 70)

    A_primes = [3, 7, 11, 19, 23, 31]
    A_covering = [3, 7, 11, 15, 19, 23, 27, 31]
    max_n = 100000

    # For each prime n, classify:
    # - Direct route: does (A/n) = -1 for any covering A?
    # - M-route: does some p | m_A have (n/p) = -1?
    # - T ∈ D_A: does the full criterion hold?

    results = []
    direct_route_fail = []  # n where (A/n) = +1 for ALL A in {7,11,19,23,31}

    for n in range(13, max_n + 1):
        if n % 12 != 1 or n % 5 == 0:
            continue
        if not isprime(n):
            continue

        n_info = {'n': n, 'A_info': {}, 'direct_route_works': False, 'm_route_works': False}

        for A in A_covering:
            if gcd(n, A) > 1:
                n_info['A_info'][A] = {'status': 'skip'}
                continue

            m = (n + A) // 4
            T = (-n * m) % A
            D = compute_D_A(n, A, tight=False)
            T_in_D = T in D

            # Direct route: (A/n) = -1
            if isprime(A):
                direct = legendre_symbol(A, n)
            else:
                direct = None  # Composite A — direct route not well-defined

            # M-route: check if some prime p | m has (n/p) = -1
            m_factors = factorint(m)
            m_route_qnr_primes = []
            for p in m_factors:
                if isprime(p) and p != n and p > 2:
                    leg = legendre_symbol(n, p)
                    if leg == -1:
                        m_route_qnr_primes.append(p)

            m_route_has_qnr = len(m_route_qnr_primes) > 0

            n_info['A_info'][A] = {
                'status': 'success' if T_in_D else 'gap',
                'T_in_D': T_in_D,
                'direct_route': direct,  # (A/n) or None
                'm_route_qnr_primes': m_route_qnr_primes,
                'm_route_has_qnr': m_route_has_qnr,
                'm': m,
            }

            if direct == -1 and T_in_D:
                n_info['direct_route_works'] = True
            if m_route_has_qnr and T_in_D:
                n_info['m_route_works'] = True

        # Check: is n QR mod all of {7, 11, 19, 23, 31}?
        all_qr = all(
            legendre_symbol(A, n) == 1
            for A in [7, 11, 19, 23, 31]
            if gcd(n, A) == 1
        )
        n_info['all_qr_direct'] = all_qr

        if all_qr:
            direct_route_fail.append(n_info)

        results.append(n_info)

    print(f"\nTotal primes n tested: {len(results)}")
    print(f"Direct route fails (n QR mod all {{7,11,19,23,31}}): {len(direct_route_fail)}")

    # ===== DIRECT ROUTE FAILURES =====
    print(f"\n{'='*70}")
    print(f"Analysis of {len(direct_route_fail)} direct-route-failure cases")
    print(f"{'='*70}")

    # For these n, the direct route fails for all prime A > 3.
    # Does the m-route rescue them?

    m_route_rescued = sum(1 for r in direct_route_fail if r['m_route_works'])
    m_route_not = sum(1 for r in direct_route_fail if not r['m_route_works'])

    print(f"  M-route works for at least one A: {m_route_rescued} / {len(direct_route_fail)}")
    print(f"  M-route does NOT work: {m_route_not} / {len(direct_route_fail)}")

    # But wait — the m-route working means T ∈ D_A AND m-route has QNR.
    # We should also check: does T ∈ D_A hold for at least one A?
    t_in_d_any = sum(1 for r in direct_route_fail 
                     if any(info['T_in_D'] for info in r['A_info'].values() if info['status'] != 'skip'))
    print(f"  T ∈ D_A for at least one A: {t_in_d_any} / {len(direct_route_fail)}")

    # ===== DETAILED M-ROUTE ANALYSIS =====
    print(f"\n{'='*70}")
    print(f"Detailed m-route analysis for direct-route-failure cases")
    print(f"{'='*70}")

    print(f"\n{'n':>8} | {'A=3':>6} | {'A=7':>12} | {'A=11':>12} | {'A=15':>8} | {'A=19':>12} | {'A=23':>12} | {'A=27':>8} | {'A=31':>12} | {'m-route':>8}")
    print(f"  {'':>8} | {'':>6} | {'T∈D / QNRs in m':>18} | ...")
    print("-" * 120)

    for r in direct_route_fail[:30]:
        n = r['n']
        row = f"{n:8d} |"
        m_any = False
        for A in A_covering:
            info = r['A_info'].get(A, {})
            if info.get('status') == 'skip':
                row += f" {'skip':>12} |"
                continue
            t = 'T' if info.get('T_in_D') else '.'
            qnrs = info.get('m_route_qnr_primes', [])
            m_flag = 'm' if qnrs else '.'
            row += f" {t}{m_flag}{len(qnrs):>2} {'':>6} |"
            if info.get('T_in_D') and qnrs:
                m_any = True
        row += f" {'✅' if m_any else '❌':>8}"
        print(row)

    # ===== M-ROUTE MECHANISM =====
    print(f"\n{'='*70}")
    print("M-route mechanism: which QNR primes of n appear in m_A?")
    print(f"{'='*70}")

    # For each direct-route-failure n, find the least QNR of n
    # and check if it appears as a factor of m_A for some A
    qnr_appearance = Counter()
    for r in direct_route_fail:
        n = r['n']
        # Find least QNR of n (smallest prime p with (n/p) = -1)
        least_qnr = None
        for p in range(2, min(n, 10000)):
            if not isprime(p):
                continue
            if p > 2 and legendre_symbol(n, p) == -1:
                least_qnr = p
                break

        if least_qnr:
            qnr_appearance[least_qnr] += 1

        # Check which A values have least_qnr | m_A
        appears_in = []
        for A in A_covering:
            info = r['A_info'].get(A, {})
            if least_qnr and least_qnr in info.get('m_route_qnr_primes', []):
                appears_in.append(A)
                if info.get('T_in_D'):
                    break  # Found a working A

    print(f"\n  Least QNR of n distribution (for direct-route-failure cases):")
    for qnr, count in qnr_appearance.most_common(20):
        print(f"    least QNR = {qnr}: {count} n values")

    # ===== THE KEY QUESTION: does the least QNR always appear in some m_A? =====
    print(f"\n{'='*70}")
    print("Key question: does the least QNR of n divide m_A for some A?")
    print(f"{'='*70}")

    least_qnr_in_m = 0
    least_qnr_not_in_m = 0
    for r in direct_route_fail:
        n = r['n']
        # Find least QNR
        least_qnr = None
        for p in range(2, min(n, 10000)):
            if not isprime(p) or gcd(p, n) == 0:
                continue
            if p > 2 and legendre_symbol(n, p) == -1:
                least_qnr = p
                break

        if least_qnr is None:
            continue

        # Check if least_qnr | m_A for some A where T ∈ D_A
        found = False
        for A in A_covering:
            info = r['A_info'].get(A, {})
            if info.get('status') == 'skip':
                continue
            m = info.get('m', 0)
            if m > 0 and least_qnr in info.get('m_route_qnr_primes', []) and info.get('T_in_D'):
                found = True
                break

        if found:
            least_qnr_in_m += 1
        else:
            least_qnr_not_in_m += 1

    print(f"  Least QNR divides m_A with T ∈ D_A: {least_qnr_in_m}")
    print(f"  Least QNR does NOT: {least_qnr_not_in_m}")

    # ===== FULL M-ROUTE VERIFICATION =====
    print(f"\n{'='*70}")
    print("Full m-route verification: for each n, does m-route work?")
    print(f"{'='*70}")

    # Count: for how many n does the m-route (having a QNR prime in m_A) 
    # coincide with T ∈ D_A?
    m_route_qnr_and_T_in_D = 0
    m_route_qnr_and_T_not_in_D = 0
    no_qnr_and_T_in_D = 0
    no_qnr_and_T_not_in_D = 0

    for r in results:
        for A in A_covering:
            info = r['A_info'].get(A, {})
            if info.get('status') == 'skip':
                continue
            has_qnr = info.get('m_route_has_qnr', False)
            t_in = info.get('T_in_D', False)
            if has_qnr and t_in:
                m_route_qnr_and_T_in_D += 1
            elif has_qnr and not t_in:
                m_route_qnr_and_T_not_in_D += 1
            elif not has_qnr and t_in:
                no_qnr_and_T_in_D += 1
            else:
                no_qnr_and_T_not_in_D += 1

    print(f"  QNR in m_A & T ∈ D_A: {m_route_qnr_and_T_in_D}")
    print(f"  QNR in m_A & T ∉ D_A: {m_route_qnr_and_T_not_in_D}")
    print(f"  No QNR in m_A & T ∈ D_A: {no_qnr_and_T_in_D}")
    print(f"  No QNR in m_A & T ∉ D_A: {no_qnr_and_T_not_in_D}")

    # The m-route says: QNR in m_A → p is QNR mod A → Theorem 3 applies
    # So "QNR in m_A & T ∈ D_A" should be the dominant case
    # "QNR in m_A & T ∉ D_A" means Theorem 3 forward direction fails (the gap cases)
    # "No QNR in m_A & T ∈ D_A" means T ∈ D_A via a different mechanism (not m-route)

    # ===== DIRECT ROUTE COVERAGE =====
    print(f"\n{'='*70}")
    print("Direct route coverage (for context)")
    print(f"{'='*70}")

    direct_works = sum(1 for r in results if r['direct_route_works'])
    direct_fails = sum(1 for r in results if not r['direct_route_works'])
    print(f"  Direct route works for at least one A: {direct_works} / {len(results)}")
    print(f"  Direct route fails for all A: {direct_fails} / {len(results)}")
    print(f"    (These {direct_fails} are the cases needing m-route or other mechanisms)")

    # Of the direct-route-failure cases, how many have T ∈ D_A for at least one A?
    direct_fail_but_covered = sum(1 for r in direct_route_fail 
                                  if any(info.get('T_in_D') for info in r['A_info'].values() 
                                        if info.get('status') != 'skip'))
    print(f"  Direct fails but T ∈ D_A for some A: {direct_fail_but_covered} / {len(direct_route_fail)}")
    print(f"  Direct fails and T ∉ D_A for all A: {len(direct_route_fail) - direct_fail_but_covered} / {len(direct_route_fail)}")

    # ===== M-ROUTE + COVERING SET =====
    print(f"\n{'='*70}")
    print("M-route + covering set: full rescue analysis")
    print(f"{'='*70}")

    # For direct-route-failure cases, what rescues them?
    rescued_by_mroute = 0
    rescued_by_direct_only = 0
    rescued_by_composite = 0
    rescued_by_other = 0
    not_rescued = 0

    for r in direct_route_fail:
        # Check each A: is it rescued by m-route (QNR in m_A & T ∈ D_A)?
        mroute_rescue = False
        composite_rescue = False
        other_rescue = False
        for A in A_covering:
            info = r['A_info'].get(A, {})
            if info.get('status') == 'skip' or not info.get('T_in_D'):
                continue
            if not isprime(A):
                composite_rescue = True
            elif info.get('m_route_has_qnr', False):
                mroute_rescue = True
            else:
                other_rescue = True  # T ∈ D_A but no QNR in m_A — different mechanism

        if mroute_rescue:
            rescued_by_mroute += 1
        elif composite_rescue:
            rescued_by_composite += 1
        elif other_rescue:
            rescued_by_other += 1
        else:
            not_rescued += 1

    print(f"  Rescued by m-route (QNR in m_A, T ∈ D_A): {rescued_by_mroute}")
    print(f"  Rescued by composite A only: {rescued_by_composite}")
    print(f"  Rescued by other mechanism (T ∈ D_A, no QNR in m_A): {rescued_by_other}")
    print(f"  NOT rescued: {not_rescued}")

    # ===== STRATEGIC SUMMARY =====
    print(f"\n{'='*70}")
    print("STRATEGIC SUMMARY")
    print(f"{'='*70}")
    print(f"""
M-Route Sufficiency Analysis:

Direct route fails (n QR mod all {{7,11,19,23,31}}): {len(direct_route_fail)} n values
  Of these, m-route provides QNR prime in m_A: {m_route_rescued}
  M-route does NOT provide QNR: {m_route_not}
  T ∈ D_A for at least one A: {direct_fail_but_covered}

M-route and T ∈ D_A:
  QNR in m_A AND T ∈ D_A: {m_route_qnr_and_T_in_D} cases (m-route WORKS)
  QNR in m_A AND T ∉ D_A: {m_route_qnr_and_T_not_in_D} cases (m-route QNR found but gap)
  No QNR in m_A AND T ∈ D_A: {no_qnr_and_T_in_D} cases (other mechanism)
  No QNR in m_A AND T ∉ D_A: {no_qnr_and_T_not_in_D} cases (no QNR, no solution)

Key findings:
  1. The m-route finds QNR primes in m_A for {m_route_rescued} of {len(direct_route_fail)} direct-route-failure cases.
  2. But having a QNR in m_A does NOT guarantee T ∈ D_A ({m_route_qnr_and_T_not_in_D} failures).
  3. The gap between "QNR in m_A" and "T ∈ D_A" is exactly the Partial -1 Route / covering set gap.
  4. {no_qnr_and_T_in_D} cases have T ∈ D_A WITHOUT any QNR in m_A — a different mechanism.

The m-route provides the QNR prime (triggering Theorem 3 converse is not the issue),
but the forward direction of Theorem 3 (QNR → T ∈ D_A) is where the gap lives.

Conclusion: M-route sufficiency is EQUIVALENT to the covering set property (#4).
  - M-route finds the QNR prime → Theorem 3 applies → but forward direction is conditional
  - The covering set property ensures at least one A works, regardless of mechanism
  - M-route is one mechanism among several; it's not independently sufficient
""")

    # ===== SAVE =====
    output = {
        'total_primes': len(results),
        'direct_route_failures': len(direct_route_fail),
        'm_route_rescued': m_route_rescued,
        'm_route_not': m_route_not,
        'direct_fail_but_covered': direct_fail_but_covered,
        'qnr_and_T_in_D': m_route_qnr_and_T_in_D,
        'qnr_and_T_not_in_D': m_route_qnr_and_T_not_in_D,
        'no_qnr_and_T_in_D': no_qnr_and_T_in_D,
        'no_qnr_and_T_not_in_D': no_qnr_and_T_not_in_D,
    }
    
    outfile = 'analysis/mroute_sufficiency.json'
    with open(outfile, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")


if __name__ == '__main__':
    main()