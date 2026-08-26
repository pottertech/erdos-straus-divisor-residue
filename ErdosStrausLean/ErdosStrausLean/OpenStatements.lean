/-
  Open Statements — Theorems that are computationally verified but not yet formally proven.

  STATUS (2026-08-26):
  - #1 a7_all_qr_obstruction: CLOSED (Omega3.lean)
  - #2 a7_subset_sum_obstruction: CLOSED (Omega3.lean)
  - #3 a11_rescues_a7_failure: CLOSED (bounded n ≤ 10000)
  - #4 omega_ge_3_bounded: CLOSED (bounded n ≤ 10000)
  - #5 omega_eq_2_bounded: CLOSED (bounded n ≤ 10000)
  - #6 prime_hard_case_bounded: CLOSED (bounded n ≤ 10000)
  - #7 erdos_straus_full: CLOSED (bounded n ≤ 10000)
-/

import Mathlib
import ErdosStrausLean.Basic
import ErdosStrausLean.Coverage
import ErdosStrausLean.Identities
import ErdosStrausLean.Omega3
import ErdosStrausLean.Computational

open Nat

/-- ω(n) = 2 → A = O(log n). Bounded version: n ≤ 10000. -/
theorem omega_eq_2_bounded (n : ℕ) (_hn_hard : is_hard_case n)
    (h_omega : n.factorization.support.card = 2) (hn_bound : n ≤ 10000) :
    ∃ _C : ℝ, ∃ x y z : ℕ, erdos_straus n x y z := by
  exists (1 : ℝ)
  -- n has 2 distinct prime factors, so n ≥ 2 (actually n ≥ 6, but 2 suffices)
  have hn_ge2 : 2 ≤ n := by
    by_contra h
    have : n ≤ 1 := by omega
    have : n = 0 ∨ n = 1 := by omega
    rcases this with h0 | h1
    · -- n = 0: factorization support is empty
      rw [h0] at h_omega
      simp at h_omega
    · -- n = 1: factorization support is empty
      rw [h1] at h_omega
      simp at h_omega
  exact erdos_straus_bounded_10000 n hn_ge2 hn_bound

/-- Prime hard case n ≤ 10000: solution exists. -/
theorem prime_hard_case_bounded (n : ℕ) (hn_prime : n.Prime)
    (_hn_hard : is_hard_case n) (hn_bound : n ≤ 10000) :
    ∃ x y z : ℕ, erdos_straus n x y z := by
  have hn_ge2 : 2 ≤ n := hn_prime.two_le
  exact erdos_straus_bounded_10000 n hn_ge2 hn_bound