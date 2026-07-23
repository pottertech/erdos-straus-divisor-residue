#!/bin/bash
# ============================================
# Erdős–Straus Project — Full Audit Script
# ============================================
# Runs all verification checks and reports status clearly.
#
# Usage:
#   bash scripts/audit_all.sh            # convenience mode (SKIP allowed)
#   bash scripts/audit_all.sh --strict   # release/reviewer mode (no skips)
#
# In strict mode:
#   - missing Lake fails
#   - missing certificate file fails
#   - any skipped core check fails
# ============================================

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
# 2. Certificate verification (per-record)
# ============================================
echo "--- 2. CERTIFICATE VERIFICATION (per-record) ---"
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
# 3. Certificate dataset integrity (count, max-A, uniqueness, domain)
# ============================================
echo "--- 3. CERTIFICATE DATASET INTEGRITY ---"
DATASET_STATUS="SKIP"
if [ -f "results/layer4_certificates.jsonl" ] && [ -f "analysis/layer4/check_certificate_dataset.py" ]; then
    if python3 analysis/layer4/check_certificate_dataset.py 2>&1; then
        DATASET_STATUS="PASS"
        pass
        echo "Dataset integrity: PASS ✅"
    else
        DATASET_STATUS="FAIL"
        fail
        echo "Dataset integrity: FAIL ❌"
    fi
else
    if [ "$STRICT" = true ]; then
        DATASET_STATUS="FAIL"
        fail
        echo "Dataset integrity: FAIL ❌ (file not found — strict mode)"
    else
        skip
        echo "Dataset integrity: SKIP ⚠️ (file not found)"
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
echo "Dataset integrity:       $DATASET_STATUS"
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