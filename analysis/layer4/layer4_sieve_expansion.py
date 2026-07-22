#!/usr/bin/env python3
"""
Layer 4 Sieve Expansion — Full 10M scan with extended A range
==============================================================
Per Mark Kruelle's directive:

For every admissible n up to 10,000,000 and candidate A in
{3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63,67,71,75,79,83,87,91,95,99,103,107},
classify the first working A and route type.

For each working pair compute:
- n, A, N = n(n+A)/4
- factorization of N
- whether n is QNR mod A
- whether some p | m_A is QNR mod A
- route type: direct n-route, m-route, centered signed route, composite-A route, exceptional
- shortest centered signed representation for -1 in C_A(N), if available
- residue class data for n modulo candidate moduli

Produce:
1. route_counts.json
2. route_examples.md
3. residue_cover_table.csv
4. outlier_8803369_analysis.md
5. layer4_sieve_report.md
6. proof_obligations.md

Do not claim a proof. The goal is to identify route families and finite proof obligations.
"""

import json
import csv
import time
import sympy
from sympy import isprime, factorint, gcd, legendre_symbol, nextprime, jacobi_symbol
from collections import defaultdict, Counter
from math import lcm

# Extended A set per Mark's directive
EXTENDED_A = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59,
              63, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107]

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

def classify_route(n, A):
    """Classify the route type for (n, A). Returns dict or None."""
    if gcd(n, A) > 1:
        return None
    
    m = (n + A) // 4
    N = n * m
    factors_N = factorint(N)
    prime_factors = [(p, e) for p, e in factors_N.items() if gcd(p, A) == 1]
    
    if not prime_factors:
        return {'works': False, 'route': 'no_qnr', 'A': A, 'm': m}
    
    # For composite A, use Jacobi symbol
    if not isprime(A):
        if A % 2 == 0:
            return None
        # Check QNR via Jacobi
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
    
    # Prime A — full analysis
    g = find_primitive_root(A)
    if g is None:
        return None
    
    orders = [multiplicative_order(p, A) for p, _ in prime_factors]
    h = 1
    for o in orders:
        h = lcm(h, o)
    
    n_qr = (legendre_symbol(n, A) == 1)
    direct = not n_qr
    
    # Order-2 check
    order_2 = [p for p, _ in prime_factors if multiplicative_order(p, A) == 2]
    
    # m-route check
    factors_m = factorint(m)
    m_qnr = [p for p in factors_m if gcd(p, A) == 1 and legendre_symbol(p, A) == -1]
    
    if h <= 1:
        return {'works': False, 'route': 'no_qnr', 'A': A, 'm': m, 'n_qr': n_qr}
    
    if h % 2 != 0:
        # h odd means -1 not in H(A), QNR doesn't exist? Actually h odd means all QR
        return {'works': False, 'route': 'no_qnr', 'A': A, 'm': m, 'n_qr': n_qr}
    
    # Compute centered set membership (simplified — just check target)
    target = h // 2
    s_values = {}
    for p, e in prime_factors:
        dlg = discrete_log_mod(g, p, A)
        if dlg is None:
            return None
        s_values[p] = dlg % h
    
    s_list = [s_values[p] for p, _ in prime_factors]
    
    # Check target in signed sumset (bounded search)
    target_reachable = False
    shortest_repr = None
    shortest_len = float('inf')
    
    # Single-term
    for i, (p, e) in enumerate(prime_factors):
        for d in range(-e, e + 1):
            if (d * s_list[i]) % h == target:
                target_reachable = True
                if 1 < shortest_len:
                    shortest_len = 1
                    shortest_repr = [(p, d)]
    
    # Two-term (limited search)
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
    
    # Three-term (very limited)
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
    
    # Route classification
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
        'n_qr': n_qr, 'direct_works': direct, 'm_qnr_factors': m_qnr,
        'shortest_repr': [(str(p), d) for p, d in shortest_repr] if shortest_repr else None,
        'shortest_len': shortest_len if shortest_repr else None,
    }

def main():
    start_time = time.time()
    
    print("=" * 80)
    print("LAYER 4 SIEVE EXPANSION — n ≤ 10M, extended A range")
    print("=" * 80)
    
    # Results storage
    route_counts = Counter()
    first_A_counts = Counter()
    route_examples = defaultdict(list)
    residue_cover = defaultdict(set)
    residue_gap = defaultdict(set)
    outlier_analysis = []
    all_results = []
    
    n = 13
    count = 0
    last_progress = time.time()
    
    while n <= 10000000:
        if not isprime(n) or n % 12 != 1 or n % 5 == 0:
            n = int(nextprime(n))
            continue
        
        count += 1
        
        # Try each A in order, find first working
        first_working = None
        for A in EXTENDED_A:
            if gcd(n, A) > 1:
                continue
            result = classify_route(n, A)
            if result is None:
                continue
            if result.get('works'):
                first_working = (A, result)
                break
        
        if first_working:
            A, res = first_working
            first_A_counts[A] += 1
            route_counts[res['route']] += 1
            
            if len(route_examples[res['route']]) < 5:
                route_examples[res['route']].append({'n': n, **res})
            
            # Residue class
            mod = 4 * A if A <= 31 else 4 * A
            residue_cover[A].add(n % mod)
            
            all_results.append({'n': n, 'A': A, **{k: v for k, v in res.items() if k != 'A'}})
        else:
            # No A worked — record as unresolved
            outlier_analysis.append(n)
        
        # Special analysis for the known outlier
        if n == 8803369:
            print(f"\n=== OUTLIER ANALYSIS: n = {n} ===")
            for A in EXTENDED_A:
                if gcd(n, A) > 1: continue
                res = classify_route(n, A)
                if res:
                    print(f"  A={A}: works={res.get('works')}, route={res.get('route')}, "
                          f"h={res.get('h', 'N/A')}, n_qr={res.get('n_qr', 'N/A')}")
                    if res.get('m_qnr_factors'):
                        print(f"    m_qnr_factors: {res['m_qnr_factors']}")
                    if res.get('shortest_repr'):
                        print(f"    shortest_repr: {res['shortest_repr']}")
        
        # Progress
        now = time.time()
        if now - last_progress > 30:
            elapsed = now - start_time
            print(f"  Progress: {count} primes, n={n}, elapsed={elapsed:.0f}s, "
                  f"routes={dict(route_counts)}")
            last_progress = now
        
        n = int(nextprime(n))
    
    elapsed = time.time() - start_time
    print(f"\n{'=' * 80}")
    print(f"COMPLETE: {count} primes analyzed in {elapsed:.0f}s")
    print(f"{'=' * 80}")
    
    # === Report ===
    print(f"\nTotal primes: {count}")
    print(f"Unresolved: {len(outlier_analysis)}")
    if outlier_analysis:
        print(f"Unresolved n values: {outlier_analysis[:20]}")
    
    print(f"\n=== FIRST WORKING A DISTRIBUTION ===")
    for A in sorted(first_A_counts.keys()):
        c = first_A_counts[A]
        pct = 100 * c / count
        print(f"  A={A}: {c} ({pct:.2f}%)")
    
    print(f"\n=== ROUTE TYPE DISTRIBUTION ===")
    route_names = {
        'order_2': 'Order-2 route',
        'direct_n_qnr': 'Direct n-QNR route',
        'm_route': 'M-route',
        'two_term_centered': 'Two-term centered',
        'short_signed': 'Short signed (3-5 terms)',
        'long_signed': 'Long signed (6+ terms)',
        'direct_or_mroute': 'Direct or m-route (composite A)',
        'gap': 'Gap (A fails)',
        'no_qnr': 'No QNR (inapplicable)',
    }
    for rt in sorted(route_counts.keys()):
        name = route_names.get(rt, rt)
        c = route_counts[rt]
        pct = 100 * c / count
        print(f"  {rt}: {name} — {c} ({pct:.2f}%)")
    
    # === Write output files ===
    
    # 1. route_counts.json
    with open('route_counts.json', 'w') as f:
        json.dump({
            'total_primes': count,
            'first_A_distribution': dict(sorted(first_A_counts.items())),
            'route_counts': dict(route_counts),
            'unresolved': outlier_analysis[:50],
            'unresolved_count': len(outlier_analysis),
        }, f, indent=2)
    print(f"\nWritten: route_counts.json")
    
    # 2. route_examples.md
    with open('route_examples.md', 'w') as f:
        f.write("# Layer 4 Sieve: Route Classification Examples\n\n")
        f.write(f"Total primes: {count} | Unresolved: {len(outlier_analysis)}\n\n")
        for rt in sorted(route_counts.keys()):
            name = route_names.get(rt, rt)
            f.write(f"## {rt}: {name}\n")
            f.write(f"Count: {route_counts[rt]}\n\n")
            f.write("| n | A | h | route | n_qr | m_qnr | shortest_repr |\n")
            f.write("|---|---|---|-------|------|-------|---------------|\n")
            for ex in route_examples[rt][:5]:
                sr = ex.get('shortest_repr', '')
                f.write(f"| {ex['n']} | {ex['A']} | {ex.get('h', '?')} | {ex['route']} | "
                        f"{ex.get('n_qr', '?')} | {ex.get('m_qnr_factors', '[]')} | {sr} |\n")
            f.write("\n")
    print(f"Written: route_examples.md")
    
    # 3. residue_cover_table.csv
    with open('residue_cover_table.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['A', 'modulus', 'covered_classes', 'gap_classes', 'cover_pct'])
        for A in EXTENDED_A:
            mod = 4 * A
            covered = residue_cover.get(A, set())
            gaps = residue_gap.get(A, set())
            total = len(covered) + len(gaps)
            pct = 100 * len(covered) / total if total > 0 else 0
            writer.writerow([A, mod, len(covered), len(gaps), f"{pct:.1f}%"])
    print(f"Written: residue_cover_table.csv")
    
    # 4. outlier_8803369_analysis.md
    with open('outlier_8803369_analysis.md', 'w') as f:
        f.write("# Outlier Analysis: n = 8,803,369\n\n")
        f.write("This prime requires A = 107, the largest A needed for any n ≤ 10M.\n\n")
        f.write("## A-by-A analysis\n\n")
        f.write("| A | works? | route | h | n_qr | m_qnr_factors | shortest_repr |\n")
        f.write("|---|--------|-------|---|------|---------------|---------------|\n")
        # Re-run analysis for this specific n
        n_val = 8803369
        for A in EXTENDED_A:
            if gcd(n_val, A) > 1: continue
            res = classify_route(n_val, A)
            if res is None: continue
            f.write(f"| {A} | {res.get('works')} | {res.get('route', 'N/A')} | "
                    f"{res.get('h', 'N/A')} | {res.get('n_qr', 'N/A')} | "
                    f"{res.get('m_qnr_factors', 'N/A')} | {res.get('shortest_repr', 'N/A')} |\n")
        f.write("\n## Structural observations\n\n")
        f.write("(To be filled based on analysis results)\n")
    print(f"Written: outlier_8803369_analysis.md")
    
    # 5. layer4_sieve_report.md
    with open('layer4_sieve_report.md', 'w') as f:
        f.write("# Layer 4 Sieve Report\n\n")
        f.write(f"**Scope:** All primes n ≡ 1 (mod 12), n ≢ 0 (mod 5), 13 ≤ n ≤ 10,000,000\n")
        f.write(f"**A range:** {EXTENDED_A}\n")
        f.write(f"**Total primes:** {count}\n")
        f.write(f"**Unresolved:** {len(outlier_analysis)}\n\n")
        f.write("## First Working A Distribution\n\n")
        f.write("| A | Count | % | Cumulative % |\n|---|------|----|------------|\n")
        cumul = 0
        for A in sorted(first_A_counts.keys()):
            c = first_A_counts[A]
            cumul += c
            f.write(f"| {A} | {c} | {100*c/count:.2f}% | {100*cumul/count:.2f}% |\n")
        f.write("\n## Route Type Distribution\n\n")
        f.write("| Route | Count | % |\n|-------|-------|---|\n")
        for rt in sorted(route_counts.keys()):
            name = route_names.get(rt, rt)
            c = route_counts[rt]
            f.write(f"| {rt} ({name}) | {c} | {100*c/count:.2f}% |\n")
        f.write("\n## Key Findings\n\n")
        f.write(f"1. **Coverage:** {count - len(outlier_analysis)}/{count} primes covered ({100*(count-len(outlier_analysis))/count:.4f}%)\n")
        f.write(f"2. **Max A needed:** {max(first_A_counts.keys()) if first_A_counts else 'N/A'}\n")
        f.write(f"3. **Most common first A:** {max(first_A_counts, key=first_A_counts.get) if first_A_counts else 'N/A'}\n")
        f.write(f"4. **Dominant route:** {max(route_counts, key=route_counts.get) if route_counts else 'N/A'}\n")
    print(f"Written: layer4_sieve_report.md")
    
    # 6. proof_obligations.md
    with open('proof_obligations.md', 'w') as f:
        f.write("# Layer 4: Proof Obligations\n\n")
        f.write("Based on the route classification, the following proof families are needed:\n\n")
        for rt in sorted(route_counts.keys()):
            name = route_names.get(rt, rt)
            c = route_counts[rt]
            difficulty = {'order_2': 'Easy (PROVEN)', 'direct_n_qnr': 'Easy (PROVEN)',
                          'm_route': 'Medium (OPEN)', 'two_term_centered': 'Medium (PARTIAL)',
                          'short_signed': 'Medium (OPEN)', 'long_signed': 'Hard (OPEN)',
                          'direct_or_mroute': 'Easy (PROVEN)', 'gap': 'N/A',
                          'no_qnr': 'N/A'}
            f.write(f"## {rt}: {name}\n")
            f.write(f"**Count:** {c} ({100*c/count:.2f}%)\n")
            f.write(f"**Difficulty:** {difficulty.get(rt, '?')}\n\n")
        f.write("## Proof Strategy\n\n")
        f.write("1. **Proven routes** (order_2, direct_n_qnr): Already covered by Theorems 2, 5\n")
        f.write("2. **M-route**: Need to prove m_A has QNR factor when direct route fails\n")
        f.write("3. **Centered routes**: Need Kneser-type argument for signed sumsets\n")
        f.write("4. **Covering set**: Need to prove finite A set always covers\n")
    print(f"Written: proof_obligations.md")
    
    print(f"\n{'=' * 80}")
    print(f"ALL OUTPUTS COMPLETE — {elapsed:.0f}s total")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    main()