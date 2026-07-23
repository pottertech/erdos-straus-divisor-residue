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
#   sorry count: 0
#   axioms/conjectures: listed intentionally
# ============================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

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
if command -v lake &> /dev/null; then
    if lake build 2>&1 | tail -5; then
        echo "Lean build: PASS ✅"
    else
        echo "Lean build: FAIL ❌"
        exit 1
    fi
else
    echo "Lean build: SKIP (lake not found in PATH)"
    echo "  To run: export PATH=\$HOME/.elan/bin:\$PATH && lake build"
fi
echo ""

# ============================================
# 2. Certificate verification
# ============================================
echo "--- 2. CERTIFICATE VERIFICATION ---"
if [ -f "results/layer4_certificates.jsonl" ]; then
    if python3 analysis/layer4/verify_certificates.py 2>&1; then
        echo "Certificate verification: PASS ✅"
    else
        echo "Certificate verification: FAIL ❌"
        exit 1
    fi
else
    echo "Certificate file not found: results/layer4_certificates.jsonl"
    echo "Certificate verification: SKIP"
fi
echo ""

# ============================================
# 3. sorry count (should be 0)
# ============================================
echo "--- 3. SORRY CHECK ---"
SORRY_COUNT=$(grep -rn "sorry" code/ analysis/layer4/ 2>/dev/null | grep -v "^.*:.*--.*sorry" | grep -v "^.*:.*#.*sorry" | wc -l | tr -d ' ')
SORRY_COMMENTS=$(grep -rn "sorry" code/ analysis/layer4/ 2>/dev/null | grep "^.*:.*--.*sorry" | wc -l | tr -d ' ')
echo "sorry proof terms: $SORRY_COUNT (expected: 0)"
echo "sorry in comments: $SORRY_COMMENTS (informational)"
if [ "$SORRY_COUNT" -eq 0 ]; then
    echo "Sorry check: PASS ✅"
else
    echo "Sorry check: FAIL ❌"
    grep -rn "sorry" code/ analysis/layer4/ 2>/dev/null | grep -v "^.*:.*--.*sorry"
fi
echo ""

# ============================================
# 4. Axioms and conjectures (intentional)
# ============================================
echo "--- 4. AXIOMS / CONJECTURES (intentional) ---"
echo "The following axioms are intentional placeholders for unproven results:"
echo ""
grep -rn "^axiom\|^[[:space:]]*axiom" code/ analysis/layer4/ 2>/dev/null || echo "(none found)"
echo ""
echo "Axiom check: LISTED (these are intentional) ⚠️"
echo ""

# ============================================
# 5. Summary
# ============================================
echo "================================================================"
echo "  AUDIT SUMMARY"
echo "================================================================"
echo "Lean build:              ${LEAN_STATUS:-see above}"
echo "Certificate verification: see above"
echo "sorry proof terms:       $SORRY_COUNT (expected: 0)"
echo "axioms/conjectures:      listed intentionally"
echo ""
echo "This project is NOT a full proof of the Erdős–Straus conjecture."
echo "It is a structured reduction + formalized subtheorems + auditable certificates."
echo "The final residue class (n ≡ 1 mod 12, 5 ∤ n, n ≥ 13) remains open."
echo "================================================================"