#!/bin/bash
# ============================================
# Erdős–Straus Project — Full Audit Script
# ============================================
# Runs all verification checks and reports status clearly.
#
# Usage:
#   bash scripts/audit_all.sh          # convenience mode (SKIP allowed)
#   bash scripts/audit_all.sh --strict  # release/reviewer mode (no skips)
#
# In strict mode:
#   - missing Lake fails
#   - missing certificate file fails
#   - any skipped core check fails
# ============================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

STRICT=false
if [ "$1" = "--strict" ]; then
    STRICT=true
fi

EXPECTED_CERT_COUNT=166011
EXPECTED_MAX_A=107

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

pass() { PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { FAIL_COUNT=$((FAIL_COUNT + 1)); }
skip() { SKIP_COUNT=$((SKIP_COUNT + 1)); }

echo "================================================================"
echo "  ERDŐS–STRAUS PROJECT — FULL AUDIT"
echo "  Mode: $( [ "$STRICT" = true ] && echo 'STRICT' || echo 'convenience' )"
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
        echo "Lean build: PASS ✅"
    else
        LEAN_STATUS="FAIL"
        fail
        echo "Lean build: FAIL ❌"
    fi
else
    if [ "$STRICT" = true ]; then
        LEAN_STATUS="FAIL"
        fail
        echo "Lean build: FAIL ❌ (lake not found — strict mode requires Lean)"
    else
        skip
        echo "Lean build: SKIP ⚠️ (lake not found in PATH)"
        echo "  To run: export PATH=\$HOME/.elan/bin:\$PATH && lake build"
    fi
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
        echo "Certificate verification: PASS ✅"
    else
        CERT_STATUS="FAIL"
        fail
        echo "Certificate verification: FAIL ❌"
    fi
else
    if [ "$STRICT" = true ]; then
        CERT_STATUS="FAIL"
        fail
        echo "Certificate verification: FAIL ❌ (file not found — strict mode)"
    else
        skip
        echo "Certificate verification: SKIP ⚠️ (file not found)"
    fi
fi
echo ""

# ============================================
# 3. Certificate count, max-A, uniqueness, and domain coverage
# ============================================
echo "--- 3. CERTIFICATE COUNT, MAX-A, UNIQUENESS, DOMAIN ---"
if [ -f "results/layer4_certificates.jsonl" ]; then
    python3 -c "
import json, sys

EXPECTED_COUNT = $EXPECTED_CERT_COUNT
EXPECTED_MAX_A = $EXPECTED_MAX_A

records = []
parse_errors = 0
seen_n = set()
duplicates = 0

with open('results/layer4_certificates.jsonl', encoding='utf-8-sig') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            cert = json.loads(line)
            n = cert.get('n', 0)
            if n in seen_n:
                duplicates += 1
            seen_n.add(n)
            records.append(cert)
        except json.JSONDecodeError:
            parse_errors += 1

count = len(records)
max_a = max((r.get('A', 0) for r in records), default=0)
unique_n = len(seen_n)

errors = []

if parse_errors > 0:
    errors.append(f'Parse errors: {parse_errors} (expected: 0)')
if count != EXPECTED_COUNT:
    errors.append(f'Count: {count} (expected: {EXPECTED_COUNT})')
if max_a != EXPECTED_MAX_A:
    errors.append(f'Max A: {max_a} (expected: {EXPECTED_MAX_A})')
if duplicates > 0:
    errors.append(f'Duplicate n values: {duplicates} (expected: 0)')
if unique_n != count:
    errors.append(f'Unique n values: {unique_n} != record count: {count}')

print(f'Records: {count} (expected: {EXPECTED_COUNT})')
print(f'Parse errors: {parse_errors} (expected: 0)')
print(f'Unique n values: {unique_n}')
print(f'Duplicates: {duplicates} (expected: 0)')
print(f'Max A: {max_a} (expected: {EXPECTED_MAX_A})')

if errors:
    print('Count/max-A/uniqueness check: FAIL ❌')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print('Count/max-A/uniqueness check: PASS ✅')
    sys.exit(0)
" 2>&1
    if [ $? -eq 0 ]; then
        pass
    else
        fail
    fi
else
    if [ "$STRICT" = true ]; then
        fail
        echo "Certificate count check: FAIL ❌ (file not found — strict mode)"
    else
        skip
        echo "Certificate count check: SKIP ⚠️ (file not found)"
    fi
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
    echo "Sorry check: PASS ✅"
else
    fail
    echo "Sorry check: FAIL ❌"
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
echo "Mode: $( [ "$STRICT" = true ] && echo 'STRICT' || echo 'convenience' )"
echo ""
echo "This project is NOT a full proof of the Erdős–Straus conjecture."
echo "It is a structured reduction + formalized subtheorems + auditable certificates."
echo "The final residue class (n ≡ 1 mod 12, 5 ∤ n, n ≥ 13) remains open."
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi