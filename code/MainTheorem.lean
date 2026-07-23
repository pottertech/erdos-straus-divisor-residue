import Mathlib
import ErdosStrausConjecture.Basic
import ErdosStrausConjecture.Identities
import ErdosStrausConjecture.CenteredEquivalence

namespace ErdosStrausConjecture

-- ============================================
-- COVERAGE THEOREM: Every n ≥ 2 falls into one of 7 cases
-- ============================================
-- The 7 cases partition all n ≥ 2:
--   Case 1: n ≡ 0 (mod 3)           — proven (mod_3_zero)
--   Case 2: n ≡ 2 (mod 3)           — proven (mod_3_two)
--   Case 3: n ≡ 4 (mod 12)          — proven (mod_12_four)
--   Case 4: n ≡ 7 (mod 12)          — proven (mod_12_seven)
--   Case 5: n ≡ 10 (mod 12)         — proven (mod_12_ten)
--   Case 6: n ≡ 1 (mod 12), 5 | n   — proven (mod_12_one_mod_5_zero)
--   Case 7: n ≡ 1 (mod 12), 5 ∤ n   — conjecture (open)
--
-- Note: Cases 1-2 cover all n ≢ 1 (mod 3).
-- Cases 3-5 cover n ≡ 1 (mod 3) except n ≡ 1 (mod 12).
-- Case 6-7 split n ≡ 1 (mod 12) by divisibility by 5.
-- ============================================

lemma residue_classification (n : ℕ) (hn : n ≥ 2) :
    n % 3 = 0 ∨
    n % 3 = 2 ∨
    n % 12 = 4 ∨
    n % 12 = 7 ∨
    n % 12 = 10 ∨
    (n % 12 = 1 ∧ n % 5 = 0) ∨
    (n % 12 = 1 ∧ n % 5 ≠ 0) := by
  -- n mod 3 ∈ {0, 1, 2}
  have hmod3 : n % 3 < 3 := Nat.mod_lt n (by norm_num)
  -- Case: n ≡ 0 (mod 3)
  by_cases h0 : n % 3 = 0
  · exact Or.inl h0
  -- Case: n ≡ 2 (mod 3)
  by_cases h2 : n % 3 = 2
  · exact Or.inr (Or.inl h2)
  -- Remaining: n % 3 = 1
  have h1 : n % 3 = 1 := by omega
  -- n mod 12: since n ≡ 1 (mod 3), n mod 12 ∈ {1, 4, 7, 10}
  have hmod12 : n % 12 < 12 := Nat.mod_lt n (by norm_num)
  -- n mod 12 mod 3 = n mod 3 = 1
  have hmod12_mod3 : (n % 12) % 3 = 1 := by
    have : n % 12 % 3 = n % 3 := Nat.mod_mod_eq n 12 3 ▸ Nat.mod_mod_eq n 4 3 (by norm_num : 3 * 4 = 12)
    -- Actually let's use omega directly
    omega
  -- So n % 12 ∈ {1, 4, 7, 10}
  have h_options : n % 12 = 1 ∨ n % 12 = 4 ∨ n % 12 = 7 ∨ n % 12 = 10 := by
    have h_le12 : n % 12 < 12 := hmod12
    have h_ge0 : n % 12 ≥ 0 := Nat.zero_le (n % 12)
    -- n % 12 mod 3 = 1 and n % 12 < 12
    -- Possible values: 1, 4, 7, 10
    interval_cases n % 12 <;> omega
  -- Subcase on n mod 12
  rcases h_options with h12_1 | h12_4 | h12_7 | h12_10
  · -- n ≡ 1 (mod 12): split by 5 | n
    by_cases h5 : n % 5 = 0
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨h12_1, h5⟩)))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨h12_1, h5⟩))))
  · exact Or.inr (Or.inr (Or.inl h12_4))
  · exact Or.inr (Or.inr (Or.inr (Or.inl h12_7)))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl h12_10))))

-- ============================================
-- MAIN THEOREM: Erdős-Straus for all proven cases
-- ============================================
-- For every n ≥ 2, EXCEPT n ≡ 1 (mod 12), 5 ∤ n, n ≥ 13:
-- there exist positive integers x, y, z with 4/n = 1/x + 1/y + 1/z.
--
-- The excluded case (n ≡ 1 mod 12, 5 ∤ n, n ≥ 13) is the open conjecture.
-- Small cases (n = 1, excluded by hypothesis; n = 2-12) are covered.
-- ============================================

theorem erdos_straus_proven_cases (n : ℕ) (hn : n ≥ 2)
    (h_not_open : ¬(n % 12 = 1 ∧ n % 5 ≠ 0 ∧ n ≥ 13)) :
    IsErdosStraus n := by
  -- Get the residue classification
  have hclass := residue_classification n hn
  rcases hclass with h0 | h2 | h4 | h7 | h10 | ⟨h1_12, h5_0⟩ | ⟨h1_12, h5_ne0⟩
  · -- n ≡ 0 (mod 3): proven
    exact mod_3_zero n hn h0
  · -- n ≡ 2 (mod 3): proven
    exact mod_3_two n hn h2
  · -- n ≡ 4 (mod 12): proven
    exact mod_12_four n (by omega) h4
  · -- n ≡ 7 (mod 12): proven
    exact mod_12_seven n (by omega) h7
  · -- n ≡ 10 (mod 12): proven
    exact mod_12_ten n (by omega) h10
  · -- n ≡ 1 (mod 12), 5 | n: proven
    exact mod_12_one_mod_5_zero n (by omega) h1_12 h5_0
  · -- n ≡ 1 (mod 12), 5 ∤ n: this is the open case
    -- But h_not_open excludes n ≥ 13, so n must be < 13
    -- n ≡ 1 (mod 12), n < 13, n ≥ 2: only n = 1 (excluded by n ≥ 2... wait n=1 mod 12 means n could be 1)
    -- Actually n ≥ 2 and n ≡ 1 mod 12 and n < 13: n = 1 (excluded) or n = 13 (excluded by h_not_open)
    -- Hmm, n=1 is excluded by hn. n=13 is excluded by h_not_open since 13 % 12 = 1, 13 % 5 ≠ 0, 13 ≥ 13.
    -- So this branch should be unreachable under h_not_open... unless n = 1 which is excluded.
    -- Wait: n ≡ 1 mod 12 means n ∈ {1, 13, 25, ...}. With n ≥ 2, smallest is 13.
    -- With h_not_open excluding n ≥ 13, we need n < 13, so n = 1, but n ≥ 2. Contradiction.
    exfalso
    -- n ≡ 1 (mod 12) and n ≥ 2 means n ≥ 13
    have h_ge13 : n ≥ 13 := by
      -- n % 12 = 1, n ≥ 2 → n ≥ 13
      -- n = 12 * (n/12) + 1, and n ≥ 2, so n/12 ≥ 1 (since n=1 is excluded by n≥2)
      have : n = 12 * (n / 12) + n % 12 := (Nat.div_add_mod n 12).symm
      rw [h1_12] at this
      -- n = 12*(n/12) + 1, n ≥ 2 → n/12 ≥ 1 → n ≥ 13
      have h_div : n / 12 ≥ 1 := by
        by_contra h
        push_neg at h
        -- n / 12 = 0, so n = 1, contradicting n ≥ 2
        rw [this, show n / 12 = 0 from by omega] at *
        omega
      omega
    -- Now n ≥ 13, n % 12 = 1, n % 5 ≠ 0 → contradicts h_not_open
    exact h_not_open ⟨h1_12, h5_ne0, h_ge13⟩

-- ============================================
-- COROLLARY: Erdős-Straus for n < 13 (all verified)
-- ============================================
-- Small cases n = 2 to 12 are all covered by the theorem above.
-- This is because the open case requires n ≥ 13.

theorem erdos_straus_small (n : ℕ) (hn : n ≥ 2) (hn_small : n < 13) :
    IsErdosStraus n := by
  apply erdos_straus_proven_cases n hn
  intro ⟨h1_12, h5_ne0, h_ge13⟩
  exact absurd h_ge13 (by omega : ¬(n ≥ 13))

-- ============================================
-- COROLLARY: Erdős-Straus for all n ≢ 1 (mod 12)
-- ============================================
-- If n is not ≡ 1 (mod 12), then n is in one of the proven cases.

theorem erdos_straus_not_mod_12_1 (n : ℕ) (hn : n ≥ 2) (h : n % 12 ≠ 1) :
    IsErdosStraus n := by
  apply erdos_straus_proven_cases n hn
  intro ⟨h1_12, _⟩
  exact absurd h1_12 h

-- ============================================
-- SUMMARY
-- ============================================
-- The Erdős-Straus conjecture is machine-verified for:
--   • All n ≢ 1 (mod 12)  [erdos_straus_not_mod_12_1]
--   • All n < 13          [erdos_straus_small]
--   • All n ≡ 1 (mod 12) with 5 | n  [mod_12_one_mod_5_zero]
--   • All primes n ≡ 5 (mod 8)       [theorem2 in CenteredEquivalence.lean]
--
-- The only remaining open case is:
--   • n ≡ 1 (mod 12), 5 ∤ n, n ≥ 13  [conjecture in Mod12Case1.lean]
--
-- Computational verification: 166,011 certificates for all admissible
-- primes n ≤ 10M (Layer 4), with independent verification via
-- analysis/layer4/verify_certificates.py.

end ErdosStrausConjecture