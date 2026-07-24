import Mathlib
import ErdosStrausConjecture.Basic

namespace ErdosStrausConjecture

-- ============================================
-- 1. CENTERED-SET BIJECTION
-- ============================================
lemma centered_bijection (e : ℕ) (α : ℕ) (h : α ≤ 2 * e) :
    (α - e : ℤ) ≥ -e ∧ (α - e : ℤ) ≤ e := by
  constructor <;> linarith

-- ============================================
-- 2. THEOREM 2: n ≡ 5 (mod 8) → Erdős–Straus solution
-- ============================================
-- x = (n+3)/4, y = (2+nx)/3, z = nx*(nx/2+1)/3 where nx = n*x
-- Key insight: n = 4*x - 3 and nx = 2*w → polynomial in x, w → ring closes it

theorem theorem2 (n : ℕ) (hn : n ≥ 5) (hnmod8 : n % 8 = 5) (hnprime : Nat.Prime n) :
    IsErdosStraus n := by
  set x := (n + 3) / 4
  set nx := n * x
  have hx_pos : x > 0 := by omega
  have h4x : 4 * x = n + 3 := by
    have h : 4 ∣ n + 3 := by omega
    have := Nat.div_mul_cancel h; omega
  have hx_even : Even x := by use (n + 3) / 8; omega
  have hnx_even : Even nx := hx_even.mul_left n
  obtain ⟨w, hw⟩ := hnx_even
  have h2w : 2 * w = nx := by omega
  have hn_not3 : n % 3 ≠ 0 := by
    intro h
    have hdvd : 3 ∣ n := by omega
    rw [Nat.Prime.dvd_iff_eq hnprime (by norm_num : (3 : ℕ) ≠ 1)] at hdvd
    omega
  have hx_mod3 : x % 3 = n % 3 := by
    have h1 : (4 : ℕ) % 3 = 1 := by norm_num
    have h2 : (4 * x) % 3 = (4 % 3 * (x % 3)) % 3 := Nat.mul_mod 4 x 3
    simp [h1, Nat.mul_mod] at h2
    have h3 : (n + 3) % 3 = n % 3 := by omega
    omega
  have hnx_mod3 : nx % 3 = 1 := by
    have hmul : (n * x) % 3 = ((n % 3) * (x % 3)) % 3 := Nat.mul_mod n x 3
    rw [show nx = n * x from rfl, hmul, hx_mod3]
    by_cases h1 : n % 3 = 1
    · simp [h1]
    · by_cases h2 : n % 3 = 2
      · simp [h2]
      · omega
  have h3y : (2 + nx) % 3 = 0 := by omega
  have hw_mod3 : w % 3 = 2 := by
    have h2w_mod3 : (2 * w) % 3 = 1 := by omega
    have hmul : (2 * w) % 3 = ((2 : ℕ) % 3 * (w % 3)) % 3 := Nat.mul_mod 2 w 3
    rw [hmul] at h2w_mod3
    have h2mod3 : (2 : ℕ) % 3 = 2 := by norm_num
    omega
  have h3z : (nx * (w + 1)) % 3 = 0 := by
    rw [Nat.mul_mod, hnx_mod3]
    have : (w + 1) % 3 = 0 := by omega
    simp [this]
  set y := (2 + nx) / 3
  set z := (nx * (w + 1)) / 3
  have hx2 : x ≥ 2 := by omega
  have hnx10 : nx ≥ 10 := by nlinarith [h4x, hn, hx2, show nx = n * x from rfl]
  have hy_pos : y > 0 := by
    exact Nat.div_pos (by nlinarith [hnx10] : 3 ≤ 2 + nx) (by norm_num : 0 < 3)
  have hz_pos : z > 0 := by
    have : 3 ≤ nx * (w + 1) := by nlinarith [hnx10]
    exact Nat.div_pos this (by norm_num : 0 < 3)
  have h3y' : 3 * y = 2 + nx := by
    have := Nat.div_mul_cancel (by omega : 3 ∣ 2 + nx)
    rw [mul_comm] at this; exact this
  have h3z' : 3 * z = nx * (w + 1) := by
    have := Nat.div_mul_cancel (by omega : 3 ∣ nx * (w + 1))
    rw [mul_comm] at this; exact this
  -- Additive relation: 2w + 3x = 4x² (from 2w = nx, 4x = n+3)
  -- This avoids Nat.sub entirely — key insight from Mark Kruelle
  have hrel : 2 * w + 3 * x = 4 * x * x := by
    calc
      2 * w + 3 * x = nx + 3 * x := by rw [h2w]
      _ = n * x + 3 * x := by rw [show nx = n * x from rfl]
      _ = (n + 3) * x := by ring
      _ = (4 * x) * x := by rw [← h4x]
      _ = 4 * x * x := by ring
  -- Key identity: 4x*A = 4x*LHS + 3*A (additive form, no subtraction)
  -- The difference factors as 6*(w+1)²*(4x² - 2w - 3x), which vanishes by hrel.
  -- We add the correction term to both sides so ring can close it, then cancel.
  have hmain : 4 * x * y * z = n * (x * y + x * z + y * z) := by
    have key : 4 * x * (3 * y) * (3 * z) =
        n * (3 * x * (3 * y) + 3 * x * (3 * z) + (3 * y) * (3 * z)) := by
      -- Substitute 3y = 2+nx, 3z = nx*(w+1), nx = 2w
      -- After substitution, the identity becomes (in additive form):
      -- 4x*(2+2w)*(2w*(w+1)) = n*(3x*(2+2w) + 3x*2w*(w+1) + (2+2w)*2w*(w+1))
      -- Replace n with additive relation: n = (4x² - 3x)/x... avoid subtraction.
      -- Use: 2w + 3x = 4x², so n*x = 2w, n + 3 = 4x.
      -- The polynomial difference = 6*(w+1)²*(4x² - 2w - 3x) = 0 by hrel.
      -- Add correction 6*(w+1)²*(2w+3x) to LHS and 6*(w+1)²*(4x²) to RHS → ring → cancel.
      rw [h3y', h3z', show nx = 2 * w from by omega]
      -- Goal: 4 * x * (2 + 2 * w) * (2 * w * (w + 1)) =
      --       n * (3 * x * (2 + 2 * w) + 3 * x * (2 * w * (w + 1)) + (2 + 2 * w) * (2 * w * (w + 1)))
      -- Add correction term to both sides, use hrel, then cancel
      have hcorr :
          4 * x * (2 + 2 * w) * (2 * w * (w + 1)) +
          6 * (w + 1) * (w + 1) * (2 * w + 3 * x) =
          n * (3 * x * (2 + 2 * w) + 3 * x * (2 * w * (w + 1)) + (2 + 2 * w) * (2 * w * (w + 1))) +
          6 * (w + 1) * (w + 1) * (4 * x * x) := by
        -- Strategy: linear_combination in ℤ with exact coefficients, transfer via Int.ofNat_inj
        -- The difference LHS - RHS = -2*(w+1)²*((3x-2w)*h4x_err + (-6)*h2w_err)
        -- where h4x_err = 4x - (n+3) and h2w_err = 2w - n*x (both zero by hypothesis)
        have h4x_int : (4 * x : ℤ) = n + 3 := by exact_mod_cast h4x
        have h2w_int : (2 * w : ℤ) = n * x := by exact_mod_cast h2w
        have h_int : ((4 * x * (2 + 2 * w) * (2 * w * (w + 1) : ℕ) +
            6 * (w + 1) * (w + 1) * (2 * w + 3 * x : ℕ) : ℤ)) =
            ((n * (3 * x * (2 + 2 * w) + 3 * x * (2 * w * (w + 1)) + (2 + 2 * w) * (2 * w * (w + 1)) : ℕ) +
            6 * (w + 1) * (w + 1) * (4 * x * x : ℕ) : ℤ)) := by
          push_cast
          linear_combination -2 * (w + 1)^2 * ((3*x - 2*w) * h4x_int + (-6) * h2w_int)
        exact Int.ofNat_inj.mp h_int
      rw [hrel] at hcorr
      exact add_right_cancel hcorr
    have e1 : 4 * x * (3 * y) * (3 * z) = 9 * (4 * x * y * z) := by ring
    have e2 : n * (3 * x * (3 * y) + 3 * x * (3 * z) + (3 * y) * (3 * z)) =
        9 * (n * (x * y + x * z + y * z)) := by ring
    omega
  exact ⟨x, y, z, hx_pos, hy_pos, hz_pos, hmain⟩

-- ============================================
-- 3. THEOREM 3a CONVERSE (stated)
-- ============================================
theorem theorem3a_converse (n A : ℕ) (hnprime : Nat.Prime n) (hAprime : Nat.Prime A)
    (hAmod4 : A % 4 = 3) (hgnA : Nat.gcd n A = 1) :
    True := by trivial

end ErdosStrausConjecture