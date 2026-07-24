import ErdosStrausConjecture.Basic

namespace ErdosStrausConjecture

-- ============================================
-- PROPER GENERAL PROOFS OF MODULAR IDENTITIES
-- Using ring tactic for polynomial identities
-- ============================================

-- ============================================
-- IDENTITY 1: n ≡ 0 (mod 3), n = 3k
-- 4/n = 1/n + 1/(2k) + 1/(2k)
-- x = n, y = z = 2k
-- ============================================

theorem mod_3_zero (n : ℕ) (hn : n ≥ 3) (hmod : n % 3 = 0) :
    IsErdosStraus n := by
  set k := n / 3
  have hn_eq : n = 3 * k := by omega
  refine ⟨n, 2 * k, 2 * k, ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · omega
  · rw [hn_eq]
    ring

-- ============================================
-- IDENTITY 2: n ≡ 2 (mod 3), n = 3k+2
-- 4/n = 1/n + 1/(k+1) + 1/(n(k+1))
-- ============================================

theorem mod_3_two (n : ℕ) (hn : n ≥ 2) (hmod : n % 3 = 2) :
    IsErdosStraus n := by
  set k := n / 3
  have hn_eq : n = 3 * k + 2 := by omega
  refine ⟨n, k + 1, n * (k + 1), ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · exact Nat.mul_pos (by omega) (by omega)
  · rw [hn_eq]
    ring

-- ============================================
-- IDENTITY 3: n ≡ 4 (mod 12), n = 12m+4
-- Symmetric: x = y = z = 3n/4 = 9m+3
-- ============================================

theorem mod_12_four (n : ℕ) (hn : n ≥ 4) (hmod : n % 12 = 4) :
    IsErdosStraus n := by
  set m := n / 12
  have hn_eq : n = 12 * m + 4 := by omega
  refine ⟨9 * m + 3, 9 * m + 3, 9 * m + 3, ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · omega
  · rw [hn_eq]
    ring

-- ============================================
-- IDENTITY 4: n ≡ 10 (mod 12), n = 12m+10
-- x = 6m+5, y = z = 12m+10
-- ============================================

theorem mod_12_ten (n : ℕ) (hn : n ≥ 10) (hmod : n % 12 = 10) :
    IsErdosStraus n := by
  set m := n / 12
  have hn_eq : n = 12 * m + 10 := by omega
  refine ⟨6 * m + 5, 12 * m + 10, 12 * m + 10, ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · omega
  · rw [hn_eq]
    ring

-- ============================================
-- IDENTITY 5: n ≡ 7 (mod 12), n = 12m+7
-- x = 3m+2, y = z = n*(n+1)/2 = (12m+7)*(6m+4)
-- ============================================

theorem mod_12_seven (n : ℕ) (hn : n ≥ 7) (hmod : n % 12 = 7) :
    IsErdosStraus n := by
  set m := n / 12
  have hn_eq : n = 12 * m + 7 := by omega
  refine ⟨3 * m + 2, (12 * m + 7) * (6 * m + 4), (12 * m + 7) * (6 * m + 4), ?_, ?_, ?_, ?_⟩
  · omega
  · exact Nat.mul_pos (by omega) (by omega)
  · exact Nat.mul_pos (by omega) (by omega)
  · rw [hn_eq]
    ring

-- ============================================
-- IDENTITY 6: n ≡ 1 (mod 12), n ≡ 0 (mod 5), n = 60m+25
-- x = 2n/5 = 24m+10, y = n = 60m+25, z = 2n = 120m+50
-- ============================================

theorem mod_12_one_mod_5_zero (n : ℕ) (hn : n ≥ 25)
    (hmod1 : n % 12 = 1) (hmod2 : n % 5 = 0) :
    IsErdosStraus n := by
  set m := n / 60
  have hn_eq : n = 60 * m + 25 := by omega
  refine ⟨24 * m + 10, 60 * m + 25, 120 * m + 50, ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · omega
  · rw [hn_eq]
    ring

end ErdosStrausConjecture