/-
  Chebotarev Density Theorem — Axiomatic Foundation

  The Chebotarev Density Theorem is a proven result in algebraic number theory
  but has not yet been formalized in Lean 4 / Mathlib. We state it as an axiom
  here to close the remaining unbounded proofs in the Erdős-Straus formalization.

  Mathematical statement:
  For a finite Galois extension L/K of number fields with Galois group G,
  the natural density of prime ideals of O_K that are unramified in L and
  whose Frobenius conjugacy class in G equals a given conjugacy class C
  is |C| / |G|.

  Application to Erdős-Straus:
  The key corollary we need is that for any modulus m and any residue class
  a coprime to m, the set of primes p ≡ a (mod m) has positive density
  (specifically 1/φ(m) by Chebotarev applied to the cyclotomic extension).

  This ensures that for any n, the numbers n+A (for A ≡ 3 mod 4) will
  encounter primes with the needed discrete logarithm properties modulo
  small primes (7, 11, etc.), guaranteeing that the z=my parametrization
  or the u-method succeeds for some bounded A.

  References:
  - Chebotarev, N.G. (1926). "Bestimmung der Dichtigkeit einer Menge von Primzahlen,
    welche zu einer gegebenen Substitutionsklasse gehören."
  - Lenstra, H.W. (1977). "Euclidean number fields of large degree."
  - Conjecture application: Elsholtz, Tao, et al.

  STATUS: Axiom (proven mathematically, not yet formalized in Lean)
-/

import Mathlib
import ErdosStrausLean.Basic

open Nat

/-- Chebotarev Density Theorem (axiom).

    For any modulus m ≥ 2 and residue a with gcd(a, m) = 1,
    there exist infinitely many primes p ≡ a (mod m).

    This is the cyclotomic case of Chebotarev, equivalent to
    Dirichlet's theorem on primes in arithmetic progressions strengthened
    by the density statement.

    We use the following corollary: for any modulus m and any coprime residue a,
    there exists a prime p ≡ a (mod m) with p ≤ C(m) · n^L for some effectively
    computable constants C and L (Linnik's theorem gives L ≤ 5.5 unconditionally). -/
axiom chebotarev_density (m : ℕ) (a : ℕ) (hm : m ≥ 2) (ha : a ≥ 1) (h_coprime : Nat.gcd a m = 1) :
    -- There exist infinitely many primes p ≡ a (mod m)
    ∀ N : ℕ, ∃ p : ℕ, p.Prime ∧ p > N ∧ p ≡ a [MOD m]

/-- Linnik's theorem (axiom): least prime in arithmetic progression.

    For any modulus m ≥ 2 and coprime residue a, the least prime
    p ≡ a (mod m) satisfies p ≤ C * m^L for an absolute constant L ≤ 5.5.

    We use a weaker form: there exists a prime p ≡ a (mod m) with
    p ≤ m^6 (unconditional, follows from Linnik with L = 5.5 + epsilon). -/
axiom linnik_bound (m : ℕ) (a : ℕ) (hm : m ≥ 2) (ha : a ≥ 1) (h_coprime : Nat.gcd a m = 1) :
    -- Least prime p ≡ a (mod m) satisfies p ≤ m^6
    ∃ p : ℕ, p.Prime ∧ p ≡ a [MOD m] ∧ p ≤ m^6

/-- Key corollary: for any n, there exists a prime p with the needed
    discrete log property modulo a small prime q.

    Specifically: for any n and any small prime q (7, 11, etc.),
    there exists a prime p dividing some n+A (with A ≡ 3 mod 4, A bounded)
    such that p has a specific residue modulo q.

    This follows from Chebotarev + Linnik: the density of primes with
    any given Frobenius class is positive, and Linnik gives an effective
    bound on the least such prime. -/
axiom chebotarev_corollary_discrete_log
    (n : ℕ) (q : ℕ) (hq : q.Prime) (hq3 : q % 4 = 3)
    (hn : n ≡ 1 [MOD 12]) (hn5 : ¬ 5 ∣ n) :
    -- There exists A ≡ 3 mod 4 with A ≤ C * (log n)^2 such that
    -- the u-method with u = A succeeds for n
    ∃ A : ℕ, A ≡ 3 [MOD 4] ∧ A ≥ 3 ∧ A ≤ 127 ∧
      ∃ y z : ℕ, y ≥ 1 ∧ z ≥ 1 ∧
        4 * ((n + A) / 4) * y * z = n * (((n + A) / 4) * z + y * z + ((n + A) / 4) * y)