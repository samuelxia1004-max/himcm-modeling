#!/usr/bin/env python3
"""Verify exact primal/dual bounds for min c.x, A.x >= b, x >= 0.

The dual is max b.y, A^T.y <= c, y >= 0. No integer/real-world certification.
"""
import argparse
from _exact_io import keys, vector, matrix, read, emit, code_hashes


def check(d):
    keys(d, ['kind', 'A', 'b', 'c', 'x', 'y'])
    if d['kind'] != 'min_cx_Ax_ge_b_x_ge_0':
        raise ValueError('unsupported problem kind')
    b, c = vector(d['b']), vector(d['c'])
    m, n = len(b), len(c)
    A, x, y = matrix(d['A'], m, n), vector(d['x'], n), vector(d['y'], m)
    primal_slack = [sum(A[i][j] * x[j] for j in range(n)) - b[i] for i in range(m)]
    dual_slack = [c[j] - sum(A[i][j] * y[i] for i in range(m)) for j in range(n)]
    pf = min(x) >= 0 and min(primal_slack) >= 0
    df = min(y) >= 0 and min(dual_slack) >= 0
    upper, lower = sum(c[j] * x[j] for j in range(n)), sum(b[i] * y[i] for i in range(m))
    valid = pf and df
    if valid and lower > upper:
        raise ArithmeticError('weak duality violated')
    return {'status': 'EXACT_LP_OPTIMUM_VERIFIED' if valid and upper == lower else
            'EXACT_LP_BOUNDS_VERIFIED' if valid else 'INVALID_CERTIFICATE',
            'valid_certificate': valid, 'optimal': valid and upper == lower,
            'primal_feasible': pf, 'dual_feasible': df,
            'primal_slack': primal_slack, 'dual_slack': dual_slack,
            'primal_objective': upper, 'dual_objective': lower,
            'lower_bound': lower if df else None, 'upper_bound': upper if pf else None,
            'absolute_gap': upper - lower if valid else None,
            'scope': 'Exact rational mathematical LP only. This does not certify an integer problem, omitted constraints, data or modeling validity.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input'); ap.add_argument('--output')
    args = ap.parse_args()
    try:
        d, sha = read(args.input)
        result = check(d)
        result.update(input_sha256=sha, code_sha256=code_hashes(__file__))
        emit(result, args.output)
    except (ValueError, TypeError, OSError) as exc:
        print('INVALID_INPUT_OR_OUTPUT: ' + str(exc))
        return 2
    return 0 if result['valid_certificate'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
