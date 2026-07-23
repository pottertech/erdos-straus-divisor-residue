#!/usr/bin/env python3
"""
Layer 4 Certificate Verifier
=============================
Independently verifies every certificate in results/layer4_certificates.jsonl.

Each certificate must satisfy ALL of the following:
  1. P divides N^2
  2. Q = N^2 / P
  3. P ≡ T (mod A)
  4. Q ≡ T (mod A)
  5. x = (n + A) / 4
  6. y = (P + N) / A
  7. z = (Q + N) / A
  8. 4*x*y*z = n*(x*y + x*z + y*z)
  9. x > 0, y > 0, z > 0

Usage:
  python3 analysis/layer4/verify_certificates.py
  python3 analysis/layer4/verify_certificates.py --file results/layer4_certificates.jsonl
  python3 analysis/layer4/verify_certificates.py --verbose
"""
import json
import sys
import os
from math import gcd

DEFAULT_PATH = "results/layer4_certificates.jsonl"

def verify_certificate(cert):
    """
    Verify a single certificate.
    Returns (True, "") if valid, (False, reason) if invalid.
    """
    n = cert.get("n")
    A = cert.get("A")
    P = cert.get("P")
    Q = cert.get("Q")
    T = cert.get("T")
    N = cert.get("N")
    x = cert.get("x")
    y = cert.get("y")
    z = cert.get("z")
    verified_flag = cert.get("verified")

    # Check all required fields present
    required = ["n", "A", "P", "Q", "T", "N", "x", "y", "z", "verified"]
    for field in required:
        if field not in cert:
            return False, f"Missing field: {field}"

    # 1. P divides N^2
    if N * N % P != 0:
        return False, f"P={P} does not divide N^2={N*N}"

    # 2. Q = N^2 / P
    if Q != N * N // P:
        return False, f"Q={Q} != N^2/P={N*N//P}"

    # 3. P ≡ T (mod A)
    if P % A != T % A:
        return False, f"P={P} mod A={A} = {P%A} != T={T} mod A = {T%A}"

    # 4. Q ≡ T (mod A)
    if Q % A != T % A:
        return False, f"Q={Q} mod A={A} = {Q%A} != T={T} mod A = {T%A}"

    # 5. x = (n + A) / 4
    expected_x = (n + A) // 4
    if (n + A) % 4 != 0:
        return False, f"(n+A)={n+A} not divisible by 4"
    if x != expected_x:
        return False, f"x={x} != (n+A)/4={expected_x}"

    # 6. y = (P + N) / A
    if (P + N) % A != 0:
        return False, f"(P+N)={P+N} not divisible by A={A}"
    expected_y = (P + N) // A
    if y != expected_y:
        return False, f"y={y} != (P+N)/A={expected_y}"

    # 7. z = (Q + N) / A
    if (Q + N) % A != 0:
        return False, f"(Q+N)={Q+N} not divisible by A={A}"
    expected_z = (Q + N) // A
    if z != expected_z:
        return False, f"z={z} != (Q+N)/A={expected_z}"

    # 8. 4*x*y*z = n*(x*y + x*z + y*z)
    lhs = 4 * x * y * z
    rhs = n * (x * y + x * z + y * z)
    if lhs != rhs:
        return False, f"4xyz={lhs} != n*(xy+xz+yz)={rhs}"

    # 9. x, y, z > 0
    if x <= 0 or y <= 0 or z <= 0:
        return False, f"Non-positive values: x={x}, y={y}, z={z}"

    # Check verified flag is True
    if not verified_flag:
        return False, "verified flag is False"

    return True, "OK"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Verify Layer 4 certificates")
    parser.add_argument("--file", default=DEFAULT_PATH, help="Path to JSONL certificate file")
    parser.add_argument("--verbose", action="store_true", help="Print first few failures in detail")
    parser.add_argument("--max-errors", type=int, default=10, help="Max errors to display (default 10)")
    args = parser.parse_args()

    filepath = args.file
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    total = 0
    valid = 0
    invalid = 0
    parse_errors = 0
    failures = []

    with open(filepath, encoding="utf-8-sig") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                cert = json.loads(line)
            except json.JSONDecodeError as e:
                parse_errors += 1
                if len(failures) < args.max_errors:
                    failures.append((i, f"JSON parse error: {e}", repr(line[:80])))
                continue

            total += 1
            ok, reason = verify_certificate(cert)
            if ok:
                valid += 1
            else:
                invalid += 1
                if len(failures) < args.max_errors:
                    failures.append((i, reason, json.dumps(cert)[:80]))

    print("=" * 70)
    print("LAYER 4 CERTIFICATE VERIFICATION REPORT")
    print("=" * 70)
    print(f"File: {filepath}")
    print(f"Total certificates: {total}")
    print(f"Valid: {valid}")
    print(f"Invalid: {invalid}")
    print(f"Parse errors: {parse_errors}")
    print(f"Verification rate: {100*valid/total:.4f}%" if total > 0 else "N/A")
    print()

    if failures:
        print(f"FIRST {min(len(failures), args.max_errors)} FAILURES:")
        for line_num, reason, snippet in failures[:args.max_errors]:
            print(f"  Line {line_num}: {reason}")
            if args.verbose:
                print(f"    Content: {snippet}")
        print()

    if invalid == 0 and parse_errors == 0:
        print("RESULT: ALL CERTIFICATES VALID ✅")
        sys.exit(0)
    else:
        print(f"RESULT: {invalid + parse_errors} ERRORS FOUND ❌")
        sys.exit(1)


if __name__ == "__main__":
    main()