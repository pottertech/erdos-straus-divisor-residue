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

set -o pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

STRICT=false
if [ "$1" = "--strict" ]; then
    STRICT=true
fi

EXPECTED_CERT_COUNT=166011
EXPECTED_MAX_A=107

# Whitelist of intentional axioms (file: name)
EXPECTED_AXIOMS=(
    "code/Mod12Case1.lean:erdos_straus_mod_12_1_not_div_5_conjecture"
    "code/DivisorResidue.lean:divisor_residue_criterion_reverse"
    "code/NewTheorems.lean:C_burgess"
    "code/NewTheorems.lean:burgess_least_qnr_bound"
)

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
    LEAN_LOG=$(mktemp)
    if lake build >"$LEAN_LOG" 2>&1; then
        tail -5 "$LEAN_LOG"
        LEAN_STATUS="PASS"
        pass
        echo "Lean build: PASS ✅"
    else
        tail -20 "$LEAN_LOG"
        LEAN_STATUS="FAIL"
        fail
        echo "Lean build: FAIL ❌"
    fi
    rm -f "$LEAN_LOG"
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
# 5. Axiom whitelist check
# ============================================
echo "--- 5. AXIOM WHITELIST CHECK ---"
echo "Expected axioms (intentional placeholders):"
for ax in "${EXPECTED_AXIOMS[@]}"; do
    echo "  $ax"
done
echo ""

# Find all axiom declarations in code/
AXIOM_FOUND=$(grep -rn "^axiom\|^[[:space:]]*axiom" code/ analysis/layer4/ 2>/dev/null || true)

# Normalize discovered axioms to file:name format
FOUND_AXIOMS=()
if [ -n "$AXIOM_FOUND" ]; then
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        # Extract file path (everything before first :)
        file=$(echo "$line" | cut -d: -f1)
        # Extract axiom name: remove line number and whitespace, then take first token after 'axiom'
        name=$(echo "$line" | sed 's/.*axiom[[:space:]]*//' | awk '{print $1}')
        FOUND_AXIOMS+=("${file}:${name}")
    done <<< "$AXIOM_FOUND"
fi

AXIOM_COUNT=${#FOUND_AXIOMS[@]}
echo "Found $AXIOM_COUNT axiom(s) in code:"
for ax in "${FOUND_AXIOMS[@]}"; do
    echo "  $ax"
done
echo ""

# Compare against whitelist: check for missing expected and unexpected found
AXIOM_ERRORS=""

# Check each expected axiom is present
for expected in "${EXPECTED_AXIOMS[@]}"; do
    found=false
    for actual in "${FOUND_AXIOMS[@]}"; do
        if [ "$actual" = "$expected" ]; then
            found=true
            break
        fi
    done
    if [ "$found" = false ]; then
        AXIOM_ERRORS="${AXIOM_ERRORS}Missing expected axiom: ${expected}\n"
    fi
done

# Check each found axiom is expected
for actual in "${FOUND_AXIOMS[@]}"; do
    expected=false
    for allowed in "${EXPECTED_AXIOMS[@]}"; do
        if [ "$actual" = "$allowed" ]; then
            expected=true
            break
        fi
    done
    if [ "$expected" = false ]; then
        AXIOM_ERRORS="${AXIOM_ERRORS}Unexpected axiom: ${actual}\n"
    fi
done

if [ -z "$AXIOM_ERRORS" ]; then
    echo "Axiom whitelist: PASS ✅"
    pass
else
    echo -e "$AXIOM_ERRORS"
    echo "Axiom whitelist: FAIL ❌"
    fail
fi
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
echo "axioms:                  $AXIOM_COUNT (whitelisted, intentional)"
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