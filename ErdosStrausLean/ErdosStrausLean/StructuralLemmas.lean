/-
  Structural Lemmas for the Erdős-Straus Conjecture

  These lemmas establish the QNR (Quadratic Non-Residue) inheritance machinery
  that underpins the u-method for prime hard cases.

  Key results:
  - -1 is QNR mod p when p ≡ 3 mod 4 (Euler's criterion via Mathlib)
  - Legendre symbol multiplicativity: QR × QNR = QNR
  - 4 is always QR (it's 2²)
  - If n is QNR mod u, then 4n is QNR mod u
  - If n is QR mod u and u ≡ 3 mod 4, then -n is QNR mod u
  - If n is QR mod u and u ≡ 3 mod 4, then -4n is QNR mod u

  The last result is the key u-method step: the target -nx in the
  factorization (uy - nx)(uz - nx) = n²x² is automatically QNR mod u
  when n is QR mod u, guaranteeing a QNR prime factor that provides
  divisor coverage.
-/

import Mathlib
import ErdosStrausLean.Basic

open Nat legendreSym

/-- -1 is a quadratic non-residue mod p when p ≡ 3 mod 4.
    This follows from ZMod.exists_sq_eq_neg_one_iff by contraposition. -/
theorem neg_one_qnr_mod_4_3 (p : ℕ) [Fact p.Prime] (hp : p % 4 = 3) :
    ¬ IsSquare (-1 : ZMod p) := by
  intro h_sq
  have h : p % 4 ≠ 3 := ZMod.exists_sq_eq_neg_one_iff.mp h_sq
  exact absurd hp h

/-- QR × QNR = QNR via Legendre symbol multiplicativity.
    legendreSym.mul: legendreSym p (a * b) = legendreSym p a * legendreSym p b -/
theorem qr_times_qnr_is_qnr (p : ℕ) [Fact p.Prime] (a b : ℤ)
    (ha : legendreSym p a = 1) (hb : legendreSym p b = -1) :
    legendreSym p (a * b) = -1 := by
  rw [legendreSym.mul, ha, hb]
  ring

/-- 4 is a perfect square mod p (witness: 2² = 4). -/
theorem four_is_square_mod_p (p : ℕ) [Fact p.Prime] (hp : p > 2) :
    IsSquare (4 : ZMod p) := by
  use 2
  show (4 : ZMod p) = 2 * 2
  push_cast
  ring

/-- legendreSym u 4 = 1 when u is an odd prime.
    Uses sq_one': legendreSym p (a^2) = 1 when a ≢ 0 mod p. -/
theorem legendre_four_eq_one (u : ℕ) [Fact u.Prime] (hu : u > 2) :
    legendreSym u 4 = 1 := by
  have h4eq : (4 : ℤ) = (2 : ℤ) ^ 2 := by norm_num
  rw [h4eq]
  apply sq_one'
  have h2ne0 : ((2 : ℤ) : ZMod u) ≠ 0 := by
    intro h
    have hdvd : (u : ℤ) ∣ (2 : ℤ) :=
      (ZMod.intCast_zmod_eq_zero_iff_dvd (2 : ℤ) u).mp h
    have hfact : u.Prime := Fact.out
    have hle : (u : ℤ) ≤ 2 := Int.le_of_dvd (by positivity) hdvd
    omega
  exact h2ne0

/-- If n is QNR mod u, then 4*n is QNR mod u (since 4 is QR). -/
theorem nqr_inheritance (u : ℕ) [Fact u.Prime] (hu : u > 2)
    (n : ℤ) (hn_qnr : legendreSym u n = -1) :
    legendreSym u (4 * n) = -1 := by
  rw [legendreSym.mul, legendre_four_eq_one u hu, hn_qnr]
  ring

/-- -n is QNR mod u when n is QR mod u and u ≡ 3 mod 4.
    Uses legendreSym.at_neg: legendreSym p (-a) = χ₄ p * legendreSym p a
    and χ₄_nat_three_mod_four: χ₄ u = -1 when u ≡ 3 mod 4. -/
theorem neg_n_qnr (u : ℕ) [Fact u.Prime] (hu3 : u % 4 = 3) (n : ℤ)
    (hn_qr : legendreSym u n = 1) :
    legendreSym u (-n) = -1 := by
  rw [legendreSym.at_neg (show u ≠ 2 from by omega), hn_qr]
  have hchi : ZMod.χ₄ u = -1 := ZMod.χ₄_nat_three_mod_four hu3
  rw [hchi]
  ring

/-- -4n is QNR mod u when n is QR and u ≡ 3 mod 4.
    This is the key u-method step: the target -nx is QNR mod u,
    guaranteeing a QNR prime factor in the divisor set of n²x². -/
theorem neg_four_n_qnr (u : ℕ) [Fact u.Prime] (hu3 : u % 4 = 3) (hu2 : u > 2)
    (n : ℤ) (hn_qr : legendreSym u n = 1) :
    legendreSym u (-4 * n) = -1 := by
  rw [legendreSym.mul]
  have h_neg4 : legendreSym u (-4) = -1 := by
    rw [legendreSym.at_neg (show u ≠ 2 from by omega)]
    have hchi : ZMod.χ₄ u = -1 := ZMod.χ₄_nat_three_mod_four hu3
    have h4 := legendre_four_eq_one u hu2
    rw [hchi, h4]
    ring
  rw [h_neg4, hn_qr]
  ring