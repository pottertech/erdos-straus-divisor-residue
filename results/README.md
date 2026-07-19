# Result Artifacts

Pre-generated computational artifacts for the Erdős–Straus divisor-residue manuscript.

## Files

### `search_100k.json`
- **Contents**: Full `(x, y, z, A)` witnesses for all admissible `n ≤ 100,000`.
- **Method**: `python3 code/search_solutions.py 100000 31 results/search_100k.json`
- **Result**: All 6,666 admissible values covered with `A ≤ 31` (Theorem 6).

### `search_10m_summary.json`
- **Contents**: Summary only (no per-n witnesses) for `n ≤ 10,000,000` with `A ≤ 99`.
- **Method**: `python3 code/search_solutions.py 10000000 99 results/search_10m_full.json`
- **Result**: 666,665/666,666 covered. The single outlier is `n = 8,803,369` (Theorem 7).

### `outlier_8803369.json`
- **Contents**: Full witness for the single uncovered case up to 10M.
- **Solution**: `A = 107` required; `x = 2,200,869`, `y = 181,085,300,330`, `z = 3,293,760,527,702,370`.

### `a_distribution_100k.csv`
- **Contents**: Distribution of A-values used for `n ≤ 100,000`.
- **Key stat**: `A = 3` covers 83.0% of cases.

## Regenerating

All artifacts can be regenerated from the code in `code/`:

```bash
# Full 100K witnesses (slow, ~2 minutes)
python3 code/search_solutions.py 100000 31 results/search_100k.json

# 10M summary (slow, ~10 minutes)
python3 code/search_solutions.py 10000000 99 results/search_10m_full.json

# Outlier witness
python3 code/search_solutions.py --witness 8803369 200
```

## Verification

Run `python3 code/verify.py` for fast CI smoke test (n ≤ 1000 subset).

All results are **computational, not proven**. See `paper/manuscript.md` for proven vs. computational result labeling.