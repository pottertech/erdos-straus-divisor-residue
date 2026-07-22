# Layer 4: Proof Obligations

Based on the route classification, the following proof families are needed:

## order_2: Order-2 route
**Count:** 146052 (87.98%)
**Difficulty:** Easy (PROVEN)
**Proof:** If some prime p | nx has ord_A(p) = 2 (i.e., p ≡ -1 mod A), then δ_p = 1 reaches h/2 in the centered sumset. Proven in Theorem 3.3, Case 2a.

## direct_n_qnr: Direct n-QNR route
**Count:** 11116 (6.70%)
**Difficulty:** Medium (COMPUTATIONALLY VERIFIED; proof pending via centered T ∈ D_A)
**Status:** The direct route is computationally verified but not fully proven. The condition (A/n) = -1 ensures n is QNR mod A, which gives h even and contributes a QNR generator. However, the full proof that T ∈ D_A requires the centered criterion h/2 ∈ Σ_A(N), which is verified computationally but not yet proven in general for this route. Theorem 5 provides the Legendre symbol identity for the m-route, not a sufficiency proof for the direct route.

## m_route: M-route
**Count:** 8843 (5.33%)
**Difficulty:** Medium (OPEN; Theorem 5 gives identity, not sufficiency)
**Status:** Theorem 5 proves (p/A) = (n/p) for p | m_A, which identifies QNR factors. However, the existence of a QNR factor in m_A when the direct route fails is not proven in general. The Jacobi identity (n/m_A) = (m_A/A) = 1 when (A/n) = 1 is a zero-information invariant that prevents algebraic proof of m-route sufficiency.

## Proof Strategy

1. **Proven route** (order_2): Already covered by Theorem 3.3, Case 2a. This handles 88% of cases.
2. **Direct n-QNR route**: Need to prove h/2 ∈ Σ_A(N) when (A/n) = -1. Computationally verified; proof pending via centered criterion.
3. **M-route**: Need to prove m_A has QNR factor when direct route fails. Theorem 5 gives the identity (p/A) = (n/p) but not existence of QNR p.
4. **Covering set**: Need to prove finite A set {3,7,11,19,23,31} always covers. Computationally verified to 10M; density-0 sieve argument (Theorem 14) + Burgess bound gives unconditional proof without constant C.

## Important caveat on composite A

For composite A values (15, 27, 35, etc.), the script uses Jacobi symbols as a signal for QNR status. Jacobi symbol -1 is only a necessary condition for QNR modulo composite A, not sufficient. The exact criterion is T ∈ D_A((nx)²), which should be computed directly. The route classification for composite A is therefore approximate. The prime A results (3, 7, 11, 19, 23, 31, 43, 47, 59, 107) use exact Legendre symbol computation and are rigorous.