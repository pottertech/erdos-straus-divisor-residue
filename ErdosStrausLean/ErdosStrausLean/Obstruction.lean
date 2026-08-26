import Mathlib
import ErdosStrausLean.Basic
import ErdosStrausLean.UMethod
import ErdosStrausLean.StructuralLemmas

open Nat legendreSym

instance : Fact (7 : ℕ).Prime := ⟨by norm_num⟩

theorem qr_ne_qnr_mod_p (a b : ℤ) (ha : legendreSym 7 a = 1) (hb : legendreSym 7 b = -1) :
    a % 7 ≠ b % 7 := by
  intro h
  have hmod_a : legendreSym 7 a = legendreSym 7 (a % 7) := legendreSym.mod (p := 7) a
  have hmod_b : legendreSym 7 b = legendreSym 7 (b % 7) := legendreSym.mod (p := 7) b
  rw [hmod_a] at ha; rw [hmod_b] at hb
  rw [h] at ha; rw [hb] at ha; norm_num at ha

theorem qr_prod_of_qr_factors (a b : ℕ)
    (hqr_a : legendreSym 7 (a : ℤ) = 1) (hqr_b : legendreSym 7 (b : ℤ) = 1) :
    legendreSym 7 ((a * b : ℕ) : ℤ) = 1 := by
  have h : ((a * b : ℕ) : ℤ) = (a : ℤ) * (b : ℤ) := Int.cast_mul a b
  rw [h, legendreSym.mul, hqr_a, hqr_b]; ring

theorem all_qr_factors_implies_qr : ∀ m : ℕ, m ≥ 1 →
    (∀ p : ℕ, p.Prime → p ∣ m → legendreSym 7 (p : ℤ) = 1) →
    legendreSym 7 (m : ℤ) = 1 := by
  intro m
  induction m using Nat.strong_induction_on with
  | h m ih =>
    intro hm hqr
    by_cases hm1 : m = 1
    · rw [hm1]; exact legendreSym.at_one 7
    · have hm2 : m ≥ 2 := by omega
      have hdvd : m.minFac ∣ m := Nat.minFac_dvd m
      have hm_ne_1 : m ≠ 1 := by assumption
      have hpr : m.minFac.Prime := Nat.minFac_prime hm_ne_1
      have hqr_p : legendreSym 7 (m.minFac : ℤ) = 1 := hqr m.minFac hpr hdvd
      have hm_pos : 0 < m := by omega
      have hmf_pos : 1 < m.minFac := hpr.two_le
      have hlt : m / m.minFac < m := Nat.div_lt_self hm_pos hmf_pos
      have hfac : m = m.minFac * (m / m.minFac) := by
        have h1 : m = m / m.minFac * m.minFac := (Nat.div_mul_cancel hdvd).symm
        exact mul_comm (m / m.minFac) m.minFac ▸ h1
      have hqr_rest : ∀ q : ℕ, q.Prime → q ∣ (m / m.minFac) → legendreSym 7 (q : ℤ) = 1 := by
        intro q qpr qdvd
        apply hqr q qpr
        rw [hfac]
        exact dvd_mul_of_dvd_right qdvd m.minFac
      have hrest_pos : m / m.minFac ≥ 1 := by
        have h1 : m / m.minFac * m.minFac = m := Nat.div_mul_cancel hdvd
        have hm_pos : m > 0 := by omega
        have hne0 : m / m.minFac ≠ 0 := by
          intro h0
          rw [h0, zero_mul] at h1
          exact absurd h1 (Ne.symm (ne_of_gt hm_pos))
        exact Nat.pos_iff_ne_zero.mpr hne0
      have hih := ih (m / m.minFac) hlt hrest_pos hqr_rest
      rw [hfac]
      exact qr_prod_of_qr_factors m.minFac (m / m.minFac) hqr_p hih

-- If n is QR mod 7, then -n is QNR mod 7 (since 7 ≡ 3 mod 4)
theorem neg_n_qnr_mod_7 (n : ℤ) (hn_qr : legendreSym 7 n = 1) :
    legendreSym 7 (-n) = -1 := by
  rw [legendreSym.at_neg (show (7 : ℕ) ≠ 2 from by norm_num) n, hn_qr]
  have h7mod4 : (7 : ℕ) % 4 = 3 := by norm_num
  have hchi : ZMod.χ₄ (7 : ℕ) = -1 := ZMod.χ₄_nat_three_mod_four h7mod4
  -- The goal has ZMod.χ₄ ↑7 (Int cast), but hchi has ZMod.χ₄ 7 (Nat)
  -- Use show to match
  exact hchi ▸ rfl

-- 4 is QR mod 7
theorem four_qr_mod_7 : legendreSym 7 (4 : ℤ) = 1 := legendre_four_eq_one 7 (by norm_num)

-- If n and x are both QR mod 7, then -n*x is QNR mod 7
theorem neg_nx_qnr_when_n_qr (n x : ℤ) (hn : legendreSym 7 n = 1) (hx : legendreSym 7 x = 1) :
    legendreSym 7 (-n * x) = -1 := by
  have h : (-n * x : ℤ) = (-1 : ℤ) * n * x := by ring
  rw [h, legendreSym.mul, legendreSym.mul]
  have h_neg1 : legendreSym 7 (-1 : ℤ) = -1 := by
    apply neg_n_qnr_mod_7
    exact legendreSym.at_one 7
  rw [h_neg1, hn, hx]; ring

-- No QR divisor matches QNR target
theorem no_qr_divisor_matches_qnr_target (D : ℕ) (target : ℤ)
    (h_all_qr : ∀ d : ℕ, d ∣ D → d ≥ 1 → legendreSym 7 (d : ℤ) = 1)
    (h_target_qnr : legendreSym 7 target = -1) :
    ¬ ∃ d : ℕ, d ∣ D ∧ d ≥ 1 ∧ (d : ℤ) % 7 = target % 7 := by
  intro ⟨d, hdvd, hdpos, hdmod⟩
  have hqr_d := h_all_qr d hdvd hdpos
  exact qr_ne_qnr_mod_p (d : ℤ) target hqr_d h_target_qnr hdmod
