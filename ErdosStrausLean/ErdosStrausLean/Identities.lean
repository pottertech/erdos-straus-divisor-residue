/-
  Modular Identities for the Erdős-Straus Conjecture

  These cover all n ≥ 2 except n ≡ 1 mod 12 with 5 ∤ n.
  Each identity gives explicit x, y, z and proves 4xyz = n(xz + yz + xy) by ring.
-/

import Mathlib
import ErdosStrausLean.Basic

open Nat

/-! ## Case 1: n ≡ 0 mod 3 (n = 3k, k ≥ 1) -/
-- 4/(3k) = 1/(3k) + 1/(2k) + 1/(2k)
theorem erdos_straus_mod3 (k : ℕ) (hk : k ≥ 1) :
    erdos_straus (3 * k) (3 * k) (2 * k) (2 * k) := by
  refine ⟨by omega, by omega, by omega, by omega, ?_⟩
  ring

/-! ## Case 2: n ≡ 2 mod 3 (n = 3k+2, k ≥ 0) -/
-- 4/(3k+2) = 1/(3k+2) + 1/(k+1) + 1/((3k+2)(k+1))
theorem erdos_straus_mod3_cong2 (k : ℕ) :
    erdos_straus (3 * k + 2) (3 * k + 2) (k + 1) ((3 * k + 2) * (k + 1)) := by
  have hz : 0 < (3 * k + 2) * (k + 1) := Nat.mul_pos (by omega) (by omega)
  refine ⟨by norm_num, by norm_num, by norm_num, by omega, ?_⟩
  ring

/-! ## Case 3: n ≡ 0 mod 4 (n = 4k, k ≥ 1) -/
-- 4/n = 1/(n/2) + 1/n + 1/n
theorem erdos_straus_mod4 (n : ℕ) (hn : n ≥ 4) (h4 : 4 ∣ n) :
    erdos_straus n (n / 2) n n := by
  obtain ⟨w, hw⟩ := h4
  have hnd2 : n / 2 = 2 * w := by
    rw [hw, Nat.div_eq_iff (by norm_num : (0 : ℕ) < 2)]
    constructor
    · omega
    · omega
  refine ⟨by omega, by omega, by omega, by omega, ?_⟩
  rw [hnd2, hw]
  ring

/-! ## Case 4: n even (general, includes n ≡ 10 mod 12) -/
-- 4/n = 1/(n/2) + 1/n + 1/n
theorem erdos_straus_even (n : ℕ) (hn : n ≥ 2) (h2 : 2 ∣ n) :
    erdos_straus n (n / 2) n n := by
  obtain ⟨w, hw⟩ := h2
  have hnd2 : n / 2 = w := by
    rw [hw, Nat.div_eq_iff (by norm_num : (0 : ℕ) < 2)]
    constructor
    · omega
    · omega
  refine ⟨by omega, by omega, by omega, by omega, ?_⟩
  rw [hnd2, hw]
  ring

/-! ## Case 5: n ≡ 3 mod 4 (includes n ≡ 7 mod 12) -/
-- 4/n = 1/((n+1)/4) + 1/(n·(n+1)/4 + 1) + 1/(n·(n+1)/4 · (n·(n+1)/4 + 1))
-- Works for ALL n ≡ 3 mod 4.
theorem erdos_straus_mod4_cong3 (n : ℕ) (hn : n ≥ 3) (h4 : n ≡ 3 [MOD 4]) :
    erdos_straus n ((n + 1) / 4) (n * ((n + 1) / 4) + 1)
      (n * ((n + 1) / 4) * (n * ((n + 1) / 4) + 1)) := by
  have h4dvd : 4 ∣ (n + 1) := by
    rw [Nat.dvd_iff_mod_eq_zero, Nat.add_mod]
    have h3 : n % 4 = 3 := by
      rw [Nat.ModEq] at h4
      omega
    omega
  obtain ⟨w, hw⟩ := h4dvd
  have hxd : (n + 1) / 4 = w := by
    rw [hw, Nat.div_eq_iff (by norm_num : (0 : ℕ) < 4)]
    constructor
    · omega
    · omega
  -- Positivity proofs using Nat.mul_pos + Nat.div_pos
  have hxd_pos : (n + 1) / 4 ≥ 1 := by
    have h := Nat.div_pos (by omega : 4 ≤ n + 1) (by norm_num : (0 : ℕ) < 4)
    omega
  have hy_pos : n * ((n + 1) / 4) + 1 ≥ 1 := by
    have hxd_lt : 0 < (n + 1) / 4 := Nat.div_pos (by omega) (by norm_num : (0 : ℕ) < 4)
    have hnx : 0 < n * ((n + 1) / 4) := Nat.mul_pos (by omega) hxd_lt
    omega
  have hz_pos : n * ((n + 1) / 4) * (n * ((n + 1) / 4) + 1) ≥ 1 := by
    have hxd_lt : 0 < (n + 1) / 4 := Nat.div_pos (by omega) (by norm_num : (0 : ℕ) < 4)
    have hnx : 0 < n * ((n + 1) / 4) := Nat.mul_pos (by omega) hxd_lt
    have hprod : 0 < n * ((n + 1) / 4) * (n * ((n + 1) / 4) + 1) :=
      Nat.mul_pos hnx (by omega)
    omega
  refine ⟨by omega, hxd_pos, hy_pos, hz_pos, ?_⟩
  -- The equation: work in ℤ to avoid ℕ subtraction
  have h_goal : (4 * w * (n * w + 1) * (n * w * (n * w + 1)) : ℤ) =
    (n * (w * (n * w * (n * w + 1)) + (n * w + 1) * (n * w * (n * w + 1)) + w * (n * w + 1)) : ℤ) := by
    have hn : (n : ℤ) = 4 * w - 1 := by
      have : (n + 1 : ℤ) = 4 * w := by exact_mod_cast hw
      linarith
    rw [hn]
    ring
  show 4 * ((n + 1) / 4) * (n * ((n + 1) / 4) + 1) * (n * ((n + 1) / 4) * (n * ((n + 1) / 4) + 1)) =
    n * (((n + 1) / 4) * (n * ((n + 1) / 4) * (n * ((n + 1) / 4) + 1)) +
      (n * ((n + 1) / 4) + 1) * (n * ((n + 1) / 4) * (n * ((n + 1) / 4) + 1)) +
      ((n + 1) / 4) * (n * ((n + 1) / 4) + 1))
  rw [hxd]
  exact_mod_cast h_goal

/-! ## Case 6: n ≡ 0 mod 5 (and n ≡ 1 mod 12) -/
-- 4/n = 1/(2n/5) + 1/n + 1/(2n)
-- x = 2n/5, y = n, z = 2n. Need 5 | n.
theorem erdos_straus_mod5 (n : ℕ) (hn : n ≥ 5) (h5 : 5 ∣ n) :
    erdos_straus n (2 * n / 5) n (2 * n) := by
  obtain ⟨w, hw⟩ := h5
  have h2n5 : 2 * n / 5 = 2 * w := by
    rw [hw, Nat.div_eq_iff (by norm_num : (0 : ℕ) < 5)]
    constructor
    · omega
    · omega
  have hx_pos : 2 * n / 5 ≥ 1 := by
    rw [h2n5]
    omega
  refine ⟨by omega, hx_pos, by omega, by omega, ?_⟩
  rw [h2n5, hw]
  ring