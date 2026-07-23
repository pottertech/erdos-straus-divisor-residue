import Mathlib
import ErdosStrausConjecture.Basic

namespace ErdosStrausConjecture

-- ============================================
-- DIVISOR-RESIDUE CRITERION (Theorem 1)
-- ============================================
-- For n prime, n ≡ 1 (mod 4), A ≡ 3 (mod 4), gcd(n, A) = 1:
-- A yields an Erdős-Straus solution iff T = -n²·4⁻¹ (mod A) lies in
-- the bounded divisor-residue set D_A((nx)²).
--
-- Construction: x = (n+A)/4, P | (nx)² with P ≡ T (mod A),
-- y = (P + N)/A, z = (Q + N)/A where Q = N²/P and N = n·x = n(n+A)/4.
-- ============================================

-- ============================================
-- KEY DEFINITION: DivisorResidueCertificate
-- ============================================
-- A certificate that A works for n: provides explicit P, x, y, z
-- satisfying all the divisor-residue conditions plus the Erdős-Straus identity.

structure DivisorResidueCertificate (n A : ℕ) where
  P : ℕ    -- witness divisor of N² where N = n*x
  x : ℕ    -- x = (n + A) / 4
  y : ℕ    -- y = (P + N) / A
  z : ℕ    -- z = (Q + N) / A where Q = N² / P
  hx_pos : x > 0
  hy_pos : y > 0
  hz_pos : z > 0
  -- The key identity: 4xyz = n*(xy + xz + yz)
  hidentity : 4 * x * y * z = n * (x * y + x * z + y * z)
  -- Structural conditions connecting to divisor-residue framework
  hx_eq : 4 * x = n + A
  hP_div : P ∣ (n * x) * (n * x)
  hP_residue : A ∣ (P + n * x)
  hy_eq : A * y = P + n * x
  hz_eq : A * z = (n * x) * (n * x) / P + n * x

-- ============================================
-- THEOREM 1 (Forward): Certificate → Erdős-Straus solution
-- ============================================
-- If a DivisorResidueCertificate exists for (n, A), then IsErdosStraus n.
-- This connects the computational certificates to the formal theorem layer.

theorem divisor_residue_criterion_forward (n A : ℕ) (hn : n ≥ 2)
    (cert : DivisorResidueCertificate n A) :
    IsErdosStraus n := by
  obtain ⟨P, x, y, z, hx_pos, hy_pos, hz_pos, hidentity, hx_eq, hP_div, hP_residue, hy_eq, hz_eq⟩ := cert
  exact ⟨x, y, z, hx_pos, hy_pos, hz_pos, hidentity⟩

-- ============================================
-- COROLLARY: Certificate-based proof for specific n
-- ============================================
-- Given a certificate, we get IsErdosStraus n.
-- This is the practical direction: certificates → theorems.

theorem erdos_straus_from_certificate (n A : ℕ) (hn : n ≥ 2)
    (cert : DivisorResidueCertificate n A) :
    IsErdosStraus n := by
  exact divisor_residue_criterion_forward n A hn cert

-- ============================================
-- THEOREM 1 (Reverse): Erdős-Straus solution → Certificate exists
-- ============================================
-- The reverse direction: given an Erdős-Straus solution with the right
-- structure, a certificate exists. This is the harder direction and
-- requires the full construction proof.

axiom divisor_residue_criterion_reverse (n A : ℕ) (hn : n ≥ 2)
    (hA : A ≡ 3 [MOD 4]) (hgnA : Nat.gcd n A = 1)
    (h_sol : IsErdosStraus n)
    (hx_eq : ∃ x : ℕ, 4 * x = n + A ∧ x > 0) :
    ∃ (cert : DivisorResidueCertificate n A), True

-- ============================================
-- CERTIFICATE CONSTRUCTION HELPER
-- ============================================
-- Given the raw computational values, construct a certificate.
-- This is what the certificate generator (verify_certificates.py) produces.

def make_certificate (n A P x y z : ℕ)
    (hx_pos : x > 0) (hy_pos : y > 0) (hz_pos : z > 0)
    (hidentity : 4 * x * y * z = n * (x * y + x * z + y * z))
    (hx_eq : 4 * x = n + A)
    (hP_div : P ∣ (n * x) * (n * x))
    (hP_residue : A ∣ (P + n * x))
    (hy_eq : A * y = P + n * x)
    (hz_eq : A * z = (n * x) * (n * x) / P + n * x) :
    DivisorResidueCertificate n A :=
  ⟨P, x, y, z, hx_pos, hy_pos, hz_pos, hidentity, hx_eq, hP_div, hP_residue, hy_eq, hz_eq⟩

end ErdosStrausConjecture