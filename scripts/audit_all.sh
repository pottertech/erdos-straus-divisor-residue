#!/bin/bash
# ============================================
# Erdős–Straus Project — Full Audit Script
# ============================================
# Runs all verification checks and reports status clearly.
#
# Usage:
#   bash scripts/audit_all.sh
#
# Expected output:
#   Lean build: PASS (or SKIP if lake not installed)
#   Certificate verification: PASS
#   Certificate count: 166011 (expected)
#   Max A in certificates: 107 (expected)
#   sorry count: 0
#   axioms/conjectures: listed intentionally
# ============================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

EXPECTED_CERT_COUNT=166011
EXPECTED_MAX_A=107

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

pass() { echo "PASS ✅"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "FAIL ❌"; FAIL_COUNT=$((FAIL_COUNT + 1)); }
skip() { echo "SKIP ⚠️"; SKIP_COUNT=$((SKIP_COUNT + 1)); }

echo "================================================================"
echo "  ERDŐS–STRAUS PROJECT — FULL AUDIT"
echo "================================================================"
echo "Repo: $(git remote get-url origin 2>/dev/null || echo 'unknown')"
echo "Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# ============================================
# 1. Lean build
# ============================================
echo "--- 1. LEAN BUILD ---"
LEAN_STATUS="SKIP"
if command -v lake &> /dev/null; then
    if lake build 2>&1 | tail -5; then
        LEAN_STATUS="PASS"
        pass
    else
        LEAN_STATUS="FAIL"
        fail
        echo "  Lean build failed. Check toolchain and Mathlib version."
    fi
else
    echo "lake not found in PATH"
    echo "  To run: export PATH=\$HOME/.elan/bin:\$PATH && lake build"
    skip
fi
echo ""

# ============================================
# 2. Certificate verification
# ============================================
echo "--- 2. CERTIFICATE VERIFICATION ---"
CERT_STATUS="SKIP"
if [ -f "results/layer4_certificates.jsonl" ]; then
    if python3 analysis/layer4/verify_certificates.py 2>&1; then
        CERT_STATUS="PASS"
        pass
    else
        CERT_STATUS="FAIL"
        fail
    fi
else
    echo "Certificate file not found: results/layer4_certificates.jsonl"
    skip
fi
echo ""

# ============================================
# 3. Certificate count and max-A verification
# ============================================
echo "--- 3. CERTIFICATE COUNT AND MAX-A ---"
if [ -f "results/layer4_certificates.jsonl" ]; then
    python3 -c "
import json
count = 0
max_a = 0
with open('results/layer4_certificates.jsonl', encoding='utf-8-sig') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            cert = json.loads(line)
            count += 1
            a = cert.get('A', 0)
            if a > max_a:
                max_a = a
        except json.JSONDecodeError:
            pass

expected_count = $EXPECTED_CERT_COUNT
expected_max_a = $EXPECTED_MAX_A
print(f'Certificate count: {count} (expected: {expected_count})')
print(f'Max A in certificates: {max_a} (expected: {expected_max_a})')
if count == expected_count and max_a == expected_max_a:
    print('Count and max-A check: PASS ✅')
else:
    print('Count and max-A check: FAIL ❌')
    if count != expected_count:
        print(f'  Count mismatch: got {count}, expected {expected_count}')
    if max_a != expected_max_a:
        print(f'  Max-A mismatch: got {max_a}, expected {expected_max_a}')
" 2>&1
else
    echo "Certificate file not found — skipping count/max-A check"
    skip
fi
echo ""

# ============================================
# 4. sorry count (should be 0)
# ============================================
echo "--- 4. SORRY CHECK ---"
SORRY_COUNT=$(grep -rn "sorry" code/ analysis/layer4/ 2>/dev/null | grep -v "^.*:.*--.*sorry" | grep -v "^.*:.*#.*sorry" | wc -l | tr -d ' ')
SORRY_COMMENTS=$(grep -rn "sorry" code/ analysis/layer4/ 2>/dev/null | grep "^.*:.*--.*sorry" | wc -l | tr -d ' ')
echo "sorry proof terms: $SORRY_COUNT (expected: 0)"
echo "sorry in comments: $SORRY_COMMENTS (informational)"
if [ "$SORRY_COUNT" -eq 0 ]; then
    pass
else
    fail
    echo "  Found sorry proof terms:"
    grep -rn "sorry" code/ analysis/layer4/ 2>/dev/null | grep -v "^.*:.*--.*sorry"
fi
echo ""

# ============================================
# 5. Axioms and conjectures (intentional)
# ============================================
echo "--- 5. AXIOMS / CONJECTURES (intentional) ---"
echo "The following axioms are intentional placeholders for unproven results:"
echo ""
AXIOM_COUNT=$(grep -rn "^axiom\|^[[:space:]]*axiom" code/ analysis/layer4/ 2>/dev/null | wc -l | tr -d ' ')
grep -rn "^axiom\|^[[:space:]]*axiom" code/ analysis/layer4/ 2>/dev/null || echo "(none found)"
echo ""
echo "Axiom count: $AXIOM_COUNT (intentional — these are conjectural placeholders)"
echo "Axiom check: LISTED ⚠️"
echo ""

# ============================================
# 6. Summary
# ============================================
echo "================================================================"
echo "  AUDIT SUMMARY"
echo "================================================================"
echo "Lean build:              $LEAN_STATUS"
echo "Certificate verification: $CERT_STATUS"
echo "sorry proof terms:       $SORRY_COUNT (expected: 0)"
echo "axioms/conjectures:      $AXIOM_COUNT (intentional)"
echo "Pass: $PASS_COUNT  Fail: $FAIL_COUNT  Skip: $SKIP_COUNT"
echo ""
echo "This project is NOT a full proof of the Erdős–Straus conjecture."
echo "It is a structured reduction + formalized subtheorems + auditable certificates."
echo "The final residue class (n ≡ 1 mod 12, 5 ∤ n, n ≥ 13) remains open."
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi