/-
  Erdős-Straus Conjecture: Formalization in Lean 4

  The conjecture states: for every integer n ≥ 2, there exist positive integers
  x, y, z such that 4/n = 1/x + 1/y + 1/z.

  We formalize the proven parts:
  - 6 modular identities covering all n except hard-case primes
  - The u-method algebraic identity
  - CRT coverage theorem
  - Parametric solutions for n ≡ 5 mod 8 and n ≡ 13 mod 24

  The cross-multiplied form: 4*x*y*z = n*(x*z + y*z + x*y)
-/

import Mathlib

open Nat

/-- The Erdős-Straus equation in cross-multiplied form -/
def erdos_straus (n x y z : ℕ) : Prop :=
  n ≥ 1 ∧ x ≥ 1 ∧ y ≥ 1 ∧ z ≥ 1 ∧ 4 * x * y * z = n * (x * z + y * z + x * y)

/-- The conjecture for all n ≥ 2 -/
def erdos_straus_conjecture : Prop :=
  ∀ n : ℕ, n ≥ 2 → ∃ x y z : ℕ, erdos_straus n x y z

/-- Hard case: n ≡ 1 mod 12, 5 ∤ n, all odd prime factors of B₃ ≡ 1 mod 3 -/
def is_hard_case (n : ℕ) : Prop :=
  n ≡ 1 [MOD 12] ∧ ¬(5 ∣ n) ∧
  ∀ p : ℕ, p.Prime → p ≠ 2 → p ∣ (n * (n + 3) / 4) → p ≡ 1 [MOD 3]

/-- The A-parameter: A = 4x - n (requires 4x ≥ n) -/
def A_param' (n x : ℕ) : ℕ := 4 * x - n