/-
  The u-Method Identity

  If 4xyz = n(xz + yz + xy) and u = 4x - n, then (uy - nx)(uz - nx) = n²x².
  This is pure algebra, proven by ring.
-/

import Mathlib
import ErdosStrausLean.Basic

open Nat

theorem umethod_identity (n x y z u : ℤ)
    (hn : n > 0) (hx : x > 0) (hy : y > 0) (hz : z > 0)
    (hu : u = 4 * x - n)
    (hes : 4 * x * y * z = n * (x * z + y * z + x * y)) :
    (u * y - n * x) * (u * z - n * x) = n^2 * x^2 := by
  -- From hes: 4xyz = n(xz + yz + xy)
  -- Substitute u = 4x - n, so 4x = u + n:
  -- (u + n)yz = n(xz + yz + xy)
  -- uyz + nyz = nxz + nyz + nxy
  -- uyz = nxz + nxy = nx(y + z)
  have h_uyz : u * y * z = n * x * (y + z) := by
    have h4x : 4 * x = u + n := by linarith
    -- (u + n) * y * z = n * (x * z + y * z + x * y)
    have : (u + n) * y * z = n * (x * z + y * z + x * y) := by
      rw [← h4x]; exact hes
    linarith
  -- Now: (uy - nx)(uz - nx) = u²yz - nxu(y+z) + n²x²
  -- = u(uyz) - nxu(y+z) + n²x²
  -- = u·nx(y+z) - nxu(y+z) + n²x²  [using h_uyz]
  -- = 0 + n²x² = n²x²
  have : (u * y - n * x) * (u * z - n * x) = u * (u * y * z) - n * x * u * (y + z) + n^2 * x^2 := by ring
  rw [this, h_uyz]
  ring