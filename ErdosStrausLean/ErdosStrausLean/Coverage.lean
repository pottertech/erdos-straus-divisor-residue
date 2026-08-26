/-
  CRT Coverage Theorem

  The modular identities cover all n ≥ 2 except n ≡ 1 mod 12 with 5 ∤ n.
-/

import Mathlib
import ErdosStrausLean.Basic

open Nat

/-- Every n ≥ 2 falls into one of these cases.
    The only uncovered case is n ≡ 1 mod 12 with 5 ∤ n (the "hard case"). -/
theorem hard_case_classification (n : ℕ) (hn : n ≥ 2) :
    3 ∣ n ∨ n ≡ 2 [MOD 3] ∨ 4 ∣ n ∨ (2 ∣ n ∧ ¬ 4 ∣ n) ∨ n ≡ 7 [MOD 12] ∨
    (n ≡ 1 [MOD 12] ∧ 5 ∣ n) ∨ (n ≡ 1 [MOD 12] ∧ ¬ 5 ∣ n) := by
  by_cases h3 : 3 ∣ n
  · exact Or.inl h3
  · by_cases h3c : n % 3 = 2
    · have h2_mod : n ≡ 2 [MOD 3] := by
        rw [Nat.ModEq]
        rw [show (2 : ℕ) % 3 = 2 from by norm_num]
        omega
      exact Or.inr (Or.inl h2_mod)
    · have h3c' : n % 3 = 1 := by
        by_contra h
        have : n % 3 < 3 := by omega
        omega
      by_cases h4 : 4 ∣ n
      · exact Or.inr (Or.inr (Or.inl h4))
      · by_cases h2 : 2 ∣ n
        · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨h2, h4⟩)))
        · have hn_odd : n % 2 = 1 := by
            by_contra h
            have : n % 2 < 2 := by omega
            omega
          have h12_mod3 : (n % 12) % 3 = n % 3 := by
            have : 12 = 3 * 4 := by norm_num
            rw [this]
            exact Nat.mod_mul_right_mod n 3 4
          have h12_mod2 : (n % 12) % 2 = n % 2 := by
            have : 12 = 2 * 6 := by norm_num
            rw [this]
            exact Nat.mod_mul_right_mod n 2 6
          by_cases h12 : n % 12 = 7
          · have h7_mod : n ≡ 7 [MOD 12] := by
              rw [Nat.ModEq]
              rw [show (7 : ℕ) % 12 = 7 from by norm_num]
              exact h12
            exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl h7_mod))))
          · have h12c : n % 12 = 1 := by
              have h_mod3 : (n % 12) % 3 = 1 := by rw [h12_mod3]; exact h3c'
              have h_mod2 : (n % 12) % 2 = 1 := by rw [h12_mod2]; exact hn_odd
              have h_bound : n % 12 < 12 := by omega
              have h_not7 : n % 12 ≠ 7 := h12
              omega
            have h12_eq : n ≡ 1 [MOD 12] := by
              rw [Nat.ModEq]
              rw [show (1 : ℕ) % 12 = 1 from by norm_num]
              exact h12c
            by_cases h5 : 5 ∣ n
            · have h_case : n ≡ 1 [MOD 12] ∧ 5 ∣ n := ⟨h12_eq, h5⟩
              exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl h_case)))))
            · have h_case : n ≡ 1 [MOD 12] ∧ ¬ 5 ∣ n := ⟨h12_eq, h5⟩
              exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr h_case)))))