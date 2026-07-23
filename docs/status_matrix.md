# Status Matrix — Erdős–Straus Divisor-Residue Project

**Last updated:** 2026-07-23
**Canonical repo:** `pottertech/erdos-straus-divisor-residue`

This document separates every claim in the project into four buckets:
1. **Proven in Lean** (machine-verified, zero `sorry`)
2. **Proven on paper** (mathematically derived, not yet formalized)
3. **Computationally verified** (exact arithmetic, independently auditable)
4. **Open / axiomatic** (conjecture, axiom, or unproven hypothesis)

---

## 1. Proven in Lean (machine-verified)

| Claim | Lean file | Tactic | Status |
|-------|-----------|--------|--------|
| **mod_3_zero**: n ≡ 0 (mod 3) → IsErdosStraus n | `code/Identities.lean` | `ring` | ✅ Proven |
| **mod_3_two**: n ≡ 2 (mod 3) → IsErdosStraus n | `code/Identities.lean` | `ring` | ✅ Proven |
| **mod_12_four**: n ≡ 4 (mod 12) → IsErdosStraus n | `code/Identities.lean` | `ring` | ✅ Proven |
| **mod_12_seven**: n ≡ 7 (mod 12) → IsErdosStraus n | `code/Identities.lean` | `ring` | ✅ Proven |
| **mod_12_ten**: n ≡ 10 (mod 12) → IsErdosStraus n | `code/Identities.lean` | `ring` | ✅ Proven |
| **mod_12_one_mod_5_zero**: n ≡ 1 (mod 12), 5 | n → IsErdosStraus n | `code/Identities.lean` | `ring` | ✅ Proven |
| **theorem2**: n prime, n ≡ 5 (mod 8) → IsErdosStraus n | `code/CenteredEquivalence.lean` | `linear_combination + Int.ofNat_inj` | ✅ Proven |
| **centered_bijection**: centered-set bijection lemma | `code/CenteredEquivalence.lean` | `linarith` | ✅ Proven |
| **residue_classification**: every n ≥ 2 falls into one of 7 cases | `code/MainTheorem.lean` | `omega + interval_cases` | ✅ Proven |
| **erdos_straus_proven_cases**: all n ≥ 2 except open class | `code/MainTheorem.lean` | dispatches to 6 identities | ✅ Proven |
| **erdos_straus_small**: all n < 13 | `code/MainTheorem.lean` | corollary | ✅ Proven |
| **erdos_straus_not_mod_12_1**: all n ≢ 1 (mod 12) | `code/MainTheorem.lean` | corollary | ✅ Proven |
| **erdos_straus_except_residual_open_class**: all n except open class minus theorem2 subfamily | `code/MainTheorem.lean` | dispatches to identities + theorem2 | ✅ Proven |

**Lean status:** Zero `sorry` proof terms. All proofs use `ring`, `omega`, `linear_combination`, `Int.ofNat_inj`, `exact`, or dispatch to proven lemmas.

---

## 2. Proven on paper (mathematically derived, not yet in Lean)

| Claim | Location | Method | Lean status |
|-------|----------|--------|-------------|
| **Divisor-residue criterion**: Erdős–Straus for n ↔ exists A, P with P | N², P ≡ T mod A, constructive x,y,z | `docs/manuscript_v12.md` §2 | Algebraic derivation | ❌ Not formalized |
| **Centered signed-exponent equivalence**: D_A(N²) = bounded sumset of centered residues | `docs/manuscript_v12.md` §3.2 | Group theory + character sums | ❌ Not formalized |
| **Direct route identities** (Theorem 5): T ∈ H(A) → solution exists | `docs/manuscript_v12.md` §3.1 | Quadratic reciprocity | ❌ Not formalized |
| **Order-2 route** (Theorem 3): h=2 QNR subcase → solution exists | `docs/manuscript_v12.md` §3.3 | Proven subcases + computational counterexample for general case | ❌ Not formalized |

**Computationally established for a finite range:**

| Claim | Location | Method | Lean status |
|-------|----------|--------|-------------|
| **M-route covering set**: sufficiency for n ≤ 100K | `docs/manuscript_v12.md` §3.2b | Exhaustive computation (finite range) | ❌ Not formalized |
| **Extended covering set**: sufficiency for n ≤ 10M | `docs/manuscript_v12.md` §3.2b | Exhaustive computation (finite range) | ❌ Not formalized |
| **Certificate bound C=31**: max A for primes ≤ 100K | `docs/manuscript_v12.md` §4 | Exhaustive computation (earlier range) | ❌ Not formalized |
| **Certificate bound C=107**: max A for admissible primes ≤ 10M | `results/layer4_certificates.jsonl` | Exhaustive computation (current range) | ❌ Not formalized |

**Analytic argument requiring audit:**

| Claim | Location | Method | Lean status |
|-------|----------|--------|-------------|
| **Proposition 8 (Burgess bound)**: least QNR in AP bound | `docs/manuscript_v12.md` §5 | 8-step proof sketch — the manuscript itself warns this is NOT a completed proof until sieve and covering assumptions are fully formalized | ⚠️ Axiom in Lean |

**Open:**

| Claim | Status | Location | Notes |
|-------|--------|----------|-------|
| **Global sieve closure**: unconditional constant-C theorem for all n | **OPEN** | `docs/manuscript_v12.md` §5.1 | Heuristic Mertens-type argument suggests C exists but does not yield an explicit finite bound. |
| **Partial −1 Route (general case)** | **PARTIALLY PROVEN** | `docs/manuscript_v12.md` §3.3 | Proven for h=2 and order-2 QNR subcases. General implication fails in 821 of 10,096 tested cases. |
| **Erdős–Straus for n ≡ 1 (mod 12), 5 ∤ n, n ≥ 13** | **AXIOM** (conjecture placeholder) | `code/Mod12Case1.lean` | Declared as `axiom` with docstring: "CONJECTURE (not proven)". Backed by 166,011 computational certificates. No closed-form proof known. |
| **Burgess bound (Proposition 8)** | **AXIOM** in Lean | `code/NewTheorems.lean` | `C_burgess` and `burgess_least_qnr_bound` declared as axioms. 8-step proof sketch in manuscript but not formalized in Lean. |

---

## 3. Computationally verified (exact arithmetic, independently auditable)

| Claim | Evidence | Verifier | Scope |
|-------|----------|----------|-------|
| **Layer 4 certificates**: 166,011 admissible primes n ≤ 10M all have solutions | `results/layer4_certificates.jsonl` (166,011 lines, 0 parse errors) | `analysis/layer4/verify_certificates.py` — 100% pass rate | All primes n ≡ 1 (mod 12), 5 ∤ n, 13 ≤ n ≤ 10M |
| **Certificate bound C = 107**: max first-working A across all tested primes | A-distribution in certificates | Verified by `verify_certificates.py` | n ≤ 10M |
| **Earlier certificate bound C = 31**: max A for primes ≤ 100K | Historical computation | Earlier scan, superseded by C=107 | n ≤ 100K |
| **n = 4,766,689**: certified with A = 39 (not A = 139) | Certificate line in JSONL | Independent verifier | Single case |
| **n = 8,803,369**: certified with A = 107 (max A in range) | Certificate line in JSONL | Independent verifier | Single case |
| **Route classification**: 5 route families, 166,011 primes classified | `analysis/layer4/layer4_sieve_expansion.py` | Layer 4 sieve report | n ≤ 10M |
| **Small cases n = 2–30**: all verified | `code/Basic.lean` (rfl proofs) | Lean `rfl` | n = 2 to 30 |

---

## 4. Open / axiomatic (conjecture, axiom, or unproven hypothesis)

| Claim | Status | Location | Notes |
|-------|--------|----------|-------|
| **Erdős–Straus for n ≡ 1 (mod 12), 5 ∤ n, n ≥ 13** | **AXIOM** (conjecture placeholder) | `code/Mod12Case1.lean` | Declared as `axiom` with docstring: "CONJECTURE (not proven)". Backed by 166,011 computational certificates. No closed-form proof known. |
| **Burgess bound (Proposition 8)** | **AXIOM** in Lean | `code/NewTheorems.lean` | `C_burgess` and `burgess_least_qnr_bound` declared as axioms. Proven on paper (8-step proof in manuscript) but not formalized in Lean. |
| **Analytic sieve / covering-set proof** | **UNPROVEN** | `docs/manuscript_v12.md` §5 | The Burgess-style estimate suggests A = O(n^{1/(4√e)+ε}) but the manuscript should not claim this as a completed proof until the sieve and covering assumptions are fully formalized. |
| **Unconditional constant-C theorem** | **OPEN** | `docs/manuscript_v12.md` §5.1 | Heuristic Mertens-type argument suggests C exists for all primes but does not yield an explicit finite bound. |
| **Partial −1 Route (general case)** | **PARTIALLY PROVEN** | `docs/manuscript_v12.md` §3.3 | Proven for h=2 and order-2 QNR subcases. General implication fails in 821 of 10,096 tested cases. |

---

## Summary

| Bucket | Count | Status |
|--------|-------|--------|
| Proven in Lean | 13 theorems/lemmas | ✅ Machine-verified, zero sorry |
| Algebraically proven (not formalized) | 4 results | 📝 Algebraic derivation |
| Computationally established (finite range) | 4 results | 🔍 Exhaustive computation |
| Analytic argument (requires audit) | 1 result | ⚠️ Proof sketch, not completed |
| Open / axiomatic | 4 items | ⚠️ Conjecture, axiom, or unproven |

**Key distinction:** The project is NOT a full proof of the Erdős–Straus conjecture. It is a structured reduction plus formalized subtheorems plus an independently auditable finite certificate layer. The final residue class (n ≡ 1 mod 12, 5 ∤ n, n ≥ 13) remains open.

**Important note on Proposition 8:** The manuscript itself warns that the Burgess-style analytic route is NOT a completed proof until the sieve and covering assumptions are fully formalized. It should not be treated as proven until independently audited.