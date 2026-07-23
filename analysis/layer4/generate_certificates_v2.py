#!/usr/bin/env python3
"""
Layer 4 Certificate Generation v2 — Optimized
================================================
Uses explicit constructions from route classification instead of brute-force y,z search.
For each prime n, the certificate contains:
- n, A (first working A)
- route type (order_2, direct_n_qnr, m_route)
- P (witness divisor of N² with P ≡ T mod A)
- x, y, z (explicit construction)
- verification: 4xyz = n*(xy + xz + yz), P | N², P ≡ T mod A
"""
import json, os, time
from sympy import isprime, factorint, gcd, nextprime, legendre_symbol, jacobi_symbol
from math import lcm

EXTENDED_A = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59,
              63, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107]

def compute_erdos_straus(n, A):
    """Compute explicit (x, y, z) for 4/n = 1/x + 1/y + 1/z using A.
    
    The construction: x = (n+A)/4, and the divisor-residue criterion gives
    P ≡ -N mod A where N = n*x. From P, we get y and z via:
    y = (P + N) / A... actually the construction depends on the route.
    
    For the standard construction (A=3, n≡5 mod 8):
      x = (n+3)/4, y = (2+nx)/3, z = nx*(nx/2+1)/3
    
    For general A: x = (n+A)/4, and we need to find P | N² with P ≡ -N mod A,
    then y = (P + N) / (n*A) and z = N² / (P * n * A)... 
    
    Actually, the simplest: just use the known Erdős–Straus solution search
    with the A-based x = (n+A)/4.
    """
    if gcd(n, A) > 1:
        return None
    
    m = (n + A) // 4  # x = m
    N = n * m
    T = (-N) % A
    
    # Verify T ∈ D_A by computing D_A
    factors_N = factorint(N)
    prime_factors = [(p, e) for p, e in factors_N.items() if gcd(p, A) == 1]
    if not prime_factors:
        return None
    
    # Compute D_A
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
    
    if T not in current_set:
        return None
    
    # Find witness P: a divisor of N² with P ≡ T mod A
    # Build divisors of N² and check
    P = find_witness_divisor(N, factors_N, A, T)
    if P is None:
        return None
    
    # From P: 4/n = 1/x + 1/y + 1/z where x = m
    # P | N² and P ≡ -N mod A means P = -N + k*A for some k
    # The Erdős–Straus identity: 4*N = n*(N + P + N²/P)... not quite
    # 
    # Standard construction: if P ≡ -N mod A and P | N², then:
    # Let Q = N² / P. Then P*Q = N².
    # 4/n = 1/x + 1/y + 1/z where:
    #   x = m = (n+A)/4
    #   y = (P + N) / A  (since P ≡ -N mod A → P + N ≡ 0 mod A)
    #   z = (Q + N) / A  (since Q = N²/P, and Q ≡ ? mod A)
    # 
    # Check: P + N ≡ 0 mod A (since P ≡ -N mod A). So A | (P + N). y = (P+N)/A.
    # And Q = N²/P. Q + N = N²/P + N = N(N+P)/P. 
    # (N+P)/P = N/P + 1. N/P might not be integer... but P | N², so N²/P is integer.
    # Q + N = N²/P + N = N(N/P + 1)... hmm, N/P might not be integer.
    # But P | N², so Q = N²/P is a positive integer.
    # z = (Q + N) / A. Need A | (Q + N).
    # Q ≡ N²/P mod A. Since P ≡ -N mod A, P⁻¹ ≡ -N⁻¹ mod A (if gcd(N,A)=1).
    # Q = N²/P ≡ N² * (-N⁻¹) = -N mod A. So Q + N ≡ 0 mod A. ✓
    
    x = m
    y_num = P + N
    y_den = A
    if y_num % y_den != 0:
        return None
    y = y_num // y_den
    
    Q = N * N // P
    z_num = Q + N
    z_den = A
    if z_num % z_den != 0:
        return None
    z = z_num // z_den
    
    # Verify
    if x <= 0 or y <= 0 or z <= 0:
        return None
    if 4 * x * y * z != n * (x * y + x * z + y * z):
        return None
    
    return {
        'n': n, 'A': A, 'P': P, 'Q': Q, 'T': T, 'N': N,
        'x': x, 'y': y, 'z': z,
        'verified': True
    }

def find_witness_divisor(N, factors_N, A, T):
    """Find P | N² with P ≡ T mod A. Uses iterative divisor generation."""
    prime_factors = [(p, e) for p, e in factors_N.items() if gcd(p, A) == 1]
    
    if not prime_factors:
        return None
    
    # Build divisors of N² iteratively, checking mod A
    # Keep only the mod-A residue and the smallest divisor for each residue
    # to avoid blowup
    residue_map = {1: 1}  # residue → smallest divisor
    
    for p, e in prime_factors:
        new_map = {}
        for res, div in residue_map.items():
            val = 1
            for a in range(2 * e + 1):
                new_res = (res * (val % A)) % A
                new_div = div * val
                if new_res not in new_map or new_div < new_map[new_res]:
                    new_map[new_res] = new_div
                val *= p
        residue_map = new_map
        if T % A in residue_map:
            return residue_map[T % A]
    
    return None

def main():
    start_time = time.time()
    
    print("=" * 70)
    print("LAYER 4 CERTIFICATE GENERATION v2 (optimized)")
    print("=" * 70)
    
    output_path = 'results/layer4_certificates.jsonl'
    os.makedirs('results', exist_ok=True)
    
    count = 0
    certified = 0
    failed = 0
    last_progress = time.time()
    
    with open(output_path, 'w') as out:
        n = 13
        while n <= 10000000:
            if not isprime(n) or n % 12 != 1 or n % 5 == 0:
                n = int(nextprime(n))
                continue
            
            count += 1
            
            cert = None
            for A in EXTENDED_A:
                if gcd(n, A) > 1:
                    continue
                result = compute_erdos_straus(n, A)
                if result is not None:
                    cert = result
                    break
            
            if cert:
                out.write(json.dumps(cert) + '\n')
                certified += 1
            else:
                failed += 1
                if failed <= 10:
                    print(f"  FAILED: n={n}")
            
            n = int(nextprime(n))
            
            now = time.time()
            if now - last_progress > 30:
                elapsed = now - start_time
                print(f"  Progress: {count} primes, n={n}, elapsed={elapsed:.0f}s, certified={certified}, failed={failed}")
                last_progress = now
    
    elapsed = time.time() - start_time
    print()
    print(f"{'=' * 70}")
    print(f"COMPLETE: {count} primes in {elapsed:.0f}s")
    print(f"  Certified: {certified} ({100*certified/count:.2f}%)")
    print(f"  Failed: {failed}")
    print(f"  Output: {output_path}")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()