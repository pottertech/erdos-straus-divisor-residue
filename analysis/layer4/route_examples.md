# Layer 4 Sieve: Route Classification Examples

Total primes: 166011 | Unresolved: 0

## direct_n_qnr: Direct n-QNR route
Count: 11116

| n | A | h | route | n_qr | m_qnr | shortest_repr |
|---|---|---|-------|------|-------|---------------|
| 73 | 7 | 6 | direct_n_qnr | False | [5] | [('2', -2), ('5', -1)] |
| 241 | 7 | 6 | direct_n_qnr | False | [31] | [('2', -1), ('31', -1)] |
| 313 | 7 | 6 | direct_n_qnr | False | [5] | [('2', -4), ('5', 1)] |
| 1129 | 11 | 10 | direct_n_qnr | False | [19] | [('3', -1), ('19', 1)] |
| 1201 | 23 | 22 | direct_n_qnr | False | [17] | [('3', -2), ('1201', -1)] |

## m_route: M-route
Count: 8843

| n | A | h | route | n_qr | m_qnr | shortest_repr |
|---|---|---|-------|------|-------|---------------|
| 193 | 7 | 6 | m_route | True | [5] | [('2', -1), ('5', 1)] |
| 673 | 7 | 6 | m_route | True | [5, 17] | [('2', -1), ('5', 1)] |
| 1873 | 7 | 6 | m_route | True | [5, 47] | [('2', -1), ('5', 1)] |
| 2473 | 7 | 6 | m_route | True | [5, 31] | [('2', -2), ('5', -1)] |
| 2689 | 15 | ? | m_route | True | [] |  |

## order_2: Order-2 route
Count: 146052

| n | A | h | route | n_qr | m_qnr | shortest_repr |
|---|---|---|-------|------|-------|---------------|
| 13 | 3 | 2 | order_2 | True | [2] | [('2', -1)] |
| 37 | 3 | 2 | order_2 | True | [2, 5] | [('2', -1)] |
| 61 | 3 | 2 | order_2 | True | [2] | [('2', -3)] |
| 97 | 3 | 2 | order_2 | True | [5] | [('5', -1)] |
| 109 | 3 | 2 | order_2 | True | [2] | [('2', -1)] |

