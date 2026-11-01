#!/usr/bin/env python3
"""Exact worst regret for listed deterministic actions with affine losses on a box."""
import argparse
from fractions import Fraction as F
from _exact_io import keys, names, vector, matrix, read, emit, code_hashes


def analyze(data):
    keys(data, ['schema_version', 'parameter_names', 'bounds', 'actions',
                'offsets', 'coefficients', 'all_actions_feasible_for_entire_box'])
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('schema_version must be integer 1')
    if data['all_actions_feasible_for_entire_box'] is not True:
        raise ValueError('feasibility for all actions over the entire box is required')
    pars, acts = names(data['parameter_names']), names(data['actions'])
    k, n = len(pars), len(acts)
    bounds = matrix(data['bounds'], k, 2)
    if any(lo > hi for lo, hi in bounds):
        raise ValueError('bounds must be nonempty closed intervals')
    offsets = vector(data['offsets'], n)
    coefficients = matrix(data['coefficients'], n, k)

    def maximum(offset, slopes):
        point = [hi if slope > 0 else lo for slope, (lo, hi) in zip(slopes, bounds)]
        value = offset + sum(g * x for g, x in zip(slopes, point))
        return {'value': value, 'attaining_parameters': point}

    pairs, regrets, worst_losses, minima = {}, {}, {}, {}
    witnesses, strict_margins = {}, {}
    for a in range(n):
        label = acts[a]
        pairs[label] = {}
        for b in range(n):
            gap = [x - y for x, y in zip(coefficients[a], coefficients[b])]
            pairs[label][acts[b]] = maximum(offsets[a] - offsets[b], gap)
        opponent = max(acts, key=lambda other: pairs[label][other]['value'])
        win = pairs[label][opponent]
        regrets[label] = win['value']
        point = win['attaining_parameters']
        losses_at_witness = {acts[b]: offsets[b] + sum(g * x for g, x in zip(coefficients[b], point)) for b in range(n)}
        actual_regret = losses_at_witness[label] - min(losses_at_witness.values())
        if actual_regret != win['value'] or actual_regret < 0:
            raise ArithmeticError('internal attaining-regret invariant failed')
        witnesses[label] = {'parameters': point, 'losses_at_witness': losses_at_witness,
                            'regret': actual_regret,
                            'optimal_actions_at_witness': [x for x in acts if losses_at_witness[x] == min(losses_at_witness.values())]}
        worst_losses[label] = maximum(offsets[a], coefficients[a])
        lower = maximum(-offsets[a], [-g for g in coefficients[a]])
        minima[label] = {'value': -lower['value'], 'attaining_parameters': lower['attaining_parameters']}
        others = [-pairs[label][x]['value'] for x in acts if x != label]
        strict_margins[label] = min(others) if others else None

    rstar = min(regrets.values())
    wstar = min(x['value'] for x in worst_losses.values())
    return {'status': 'EXACT_LISTED_ACTION_BOX_ANALYSIS', 'parameters': pars, 'bounds': bounds,
            'pairwise_maximum_loss_difference': pairs,
            'worst_regret': regrets, 'worst_regret_attainment': witnesses,
            'uniformly_weakly_optimal_actions': [a for a in acts if regrets[a] == 0],
            'uniform_strict_dominance_margin': strict_margins,
            'minimax_regret_actions': [a for a in acts if regrets[a] == rstar],
            'minimax_regret_value': rstar,
            'minimax_loss_actions': [a for a in acts if worst_losses[a]['value'] == wstar],
            'minimax_loss_value': wstar, 'maximum_loss': worst_losses, 'minimum_loss': minima,
            'certificate': 'For each linear difference choose the maximizing endpoint in each coordinate; finite max over opponents commutes with max over the entire closed box.',
            'scope': 'Only the listed deterministic actions, declared affine losses, declared common feasibility and supplied continuous box. No probability, physical identification, correlated-set exactness, randomized-action optimum, nonlinear loss, new actions or parameter-dependent feasibility is certified.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input'); ap.add_argument('--output')
    args = ap.parse_args()
    try:
        data, sha = read(args.input)
        result = analyze(data)
        result.update(input_sha256=sha, code_sha256=code_hashes(__file__))
        emit(result, args.output)
    except (ValueError, TypeError, OSError) as exc:
        print('INVALID_INPUT_OR_OUTPUT: ' + str(exc)); return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
