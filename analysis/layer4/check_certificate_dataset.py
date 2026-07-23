#!/usr/bin/env python3
"""
Certificate Dataset Integrity Checker
======================================
Independently verifies the Layer 4 certificate dataset:

1. Zero JSON parse errors
2. Exact record count (166,011)
3. Zero duplicate n values
4. Maximum A = 107
5. Exact domain coverage: observed n values == expected admissible primes

The expected domain is: all primes p with 13 ≤ p ≤ 10,000,000,
p ≡ 1 (mod 12), p ≢ 0 (mod 5).

Usage:
  python3 analysis/layer4/check_certificate_dataset.py
  python3 analysis/layer4/check_certificate_dataset.py --verbose

Exit code: 0 if all checks pass, 1 if any fail.
"""
import json
import sys
import os
from math import gcd

DEFAULT_PATH = "results/layer4_certificates.jsonl"
EXPECTED_COUNT = 166011
EXPECTED_MAX_A = 107
MAX_N = 10_000_000


def generate_expected_primes():
    """Generate all admissible primes: 13 ≤ p ≤ MAX_N, p ≡ 1 (mod 12), p ≢ 0 (mod 5)."""
    # Use a sieve for efficiency
    sieve = bytearray(b'\x01') * (MAX_N + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(MAX_N**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, MAX_N + 1, i):
                sieve[j] = 0
    
    expected = set()
    for p in range(13, MAX_N + 1):
        if sieve[p] and p % 12 == 1 and p % 5 != 0:
            expected.add(p)
    return expected


def check_dataset(filepath, verbose=False):
    records = []
    parse_errors = 0
    seen_n = set()
    duplicates = 0

    with open(filepath, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                cert = json.loads(line)
                n = cert.get("n", 0)
                if n in seen_n:
                    duplicates += 1
                seen_n.add(n)
                records.append(cert)
            except json.JSONDecodeError:
                parse_errors += 1

    count = len(records)
    max_a = max((r.get("A", 0) for r in records), default=0)
    unique_n = len(seen_n)

    errors = []

    if parse_errors > 0:
        errors.append(f"Parse errors: {parse_errors} (expected: 0)")
    if count != EXPECTED_COUNT:
        errors.append(f"Record count: {count} (expected: {EXPECTED_COUNT})")
    if max_a != EXPECTED_MAX_A:
        errors.append(f"Max A: {max_a} (expected: {EXPECTED_MAX_A})")
    if duplicates > 0:
        errors.append(f"Duplicate n values: {duplicates} (expected: 0)")
    if unique_n != count:
        errors.append(f"Unique n values: {unique_n} != record count: {count}")

    # Exact domain coverage
    expected_n = generate_expected_primes()
    missing = expected_n - seen_n
    unexpected = seen_n - expected_n
    if missing:
        errors.append(f"Missing expected primes: {len(missing)}")
        if verbose and len(missing) <= 20:
            for n in sorted(missing)[:20]:
                errors.append(f"  missing: n={n}")
    if unexpected:
        errors.append(f"Unexpected n values (not admissible primes): {len(unexpected)}")
        if verbose and len(unexpected) <= 20:
            for n in sorted(unexpected)[:20]:
                errors.append(f"  unexpected: n={n}")
    if seen_n != expected_n:
        errors.append("Certificate domain does not exactly match expected admissible primes")

    print(f"Records: {count} (expected: {EXPECTED_COUNT})")
    print(f"Parse errors: {parse_errors} (expected: 0)")
    print(f"Unique n values: {unique_n}")
    print(f"Duplicates: {duplicates} (expected: 0)")
    print(f"Max A: {max_a} (expected: {EXPECTED_MAX_A})")
    print(f"Expected admissible primes: {len(expected_n)}")
    print(f"Missing: {len(missing)}")
    print(f"Unexpected: {len(unexpected)}")

    if errors:
        print()
        print("DATASET INTEGRITY: FAIL ❌")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print()
        print("DATASET INTEGRITY: PASS ✅")
        sys.exit(0)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Certificate dataset integrity checker")
    parser.add_argument("--file", default=DEFAULT_PATH, help="Path to JSONL certificate file")
    parser.add_argument("--verbose", action="store_true", help="Print details for missing/unexpected")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)

    check_dataset(args.file, verbose=args.verbose)