# Layer 4: Proof Obligations

Based on the route classification, the following proof families are needed:

## direct_n_qnr: Direct n-QNR route
**Count:** 11116 (6.70%)
**Difficulty:** Easy (PROVEN)

## m_route: M-route
**Count:** 8843 (5.33%)
**Difficulty:** Medium (OPEN)

## order_2: Order-2 route
**Count:** 146052 (87.98%)
**Difficulty:** Easy (PROVEN)

## Proof Strategy

1. **Proven routes** (order_2, direct_n_qnr): Already covered by Theorems 2, 5
2. **M-route**: Need to prove m_A has QNR factor when direct route fails
3. **Centered routes**: Need Kneser-type argument for signed sumsets
4. **Covering set**: Need to prove finite A set always covers
