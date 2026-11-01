#!/usr/bin/env python3
"""Exact finite loss-table analysis, conditional on all actions being feasible.

No solver or model validity certification. Missing priors stay unknown.
"""
import argparse
from fractions import Fraction
from _exact_io import keys, matrix, names, probability, number, read, emit, code_hashes


def analyze(d):
    keys(d, ['schema_version', 'actions', 'states', 'losses',
             'all_actions_feasible_in_all_states'], ['probabilities', 'signals'])
    if type(d['schema_version']) is not int or d['schema_version'] != 1:
        raise ValueError('schema_version must be integer 1')
    if d['all_actions_feasible_in_all_states'] is not True:
        raise ValueError('this tool requires all actions feasible in every listed state')
    actions, states = names(d['actions']), names(d['states'])
    n, m = len(actions), len(states)
    loss = matrix(d['losses'], n, m)
    ideal = [min(row[s] for row in loss) for s in range(m)]
    worst = [max(row) for row in loss]
    regret = [max(row[s] - ideal[s] for s in range(m)) for row in loss]
    winners = lambda values: [actions[a] for a in range(n) if values[a] == min(values)]
    nondominated = [actions[a] for a in range(n) if not any(
        all(loss[b][s] <= loss[a][s] for s in range(m)) and
        any(loss[b][s] < loss[a][s] for s in range(m))
        for b in range(n) if b != a)]
    result = {'status': 'FINITE_TABLE_ANALYZED',
              'scope': 'Listed actions/states only; loss semantics, feasibility declaration and real-world probabilities are not certified.',
              'actions': actions, 'states': states,
              'statewise_ideal_loss': ideal, 'worst_loss': dict(zip(actions, worst)),
              'worst_regret': dict(zip(actions, regret)),
              'minimax_loss_actions': winners(worst),
              'minimax_regret_actions': winners(regret),
              'nondominated_actions': nondominated, 'expected': None, 'signals': None}
    if 'probabilities' not in d:
        if 'signals' in d:
            raise ValueError('signal information value requires explicit prior probabilities')
        return result
    p = probability(d['probabilities'], m)
    exp = [sum(p[s] * row[s] for s in range(m)) for row in loss]
    v0 = min(exp)
    perfect = sum(p[s] * ideal[s] for s in range(m))
    result['expected'] = {'loss': dict(zip(actions, exp)), 'best_actions': winners(exp),
                          'best_loss': v0, 'perfect_information_loss': perfect,
                          'EVPI': v0 - perfect}
    if 'signals' in d:
        sig = d['signals']
        keys(sig, ['names', 'conditional_on_state', 'cost'])
        zs = names(sig['names'])
        q = matrix(sig['conditional_on_state'], m, len(zs))
        for row in q:
            probability([str(x) for x in row], len(zs))
        cost = number(sig['cost'])
        if cost < 0:
            raise ValueError('observation cost must be nonnegative')
        branch, value = {}, Fraction(0)
        for z, label in enumerate(zs):
            joint = [p[s] * q[s][z] for s in range(m)]
            mass = sum(joint)
            weighted = [sum(joint[s] * row[s] for s in range(m)) for row in loss]
            value += min(weighted)
            branch[label] = {'probability': mass,
                             'optimal_actions': winners(weighted) if mass else [],
                             'conditional_expected_loss': min(weighted) / mass if mass else None}
        evsi = v0 - value
        if not 0 <= evsi <= v0 - perfect:
            raise ArithmeticError('information value invariant violated')
        result['signals'] = {'branches': branch, 'loss_before_cost': value,
                             'loss_after_cost': value + cost, 'EVSI': evsi,
                             'net_expected_gain': evsi - cost,
                             'expected_cost_decision': 'BUY' if evsi > cost else 'INDIFFERENT' if evsi == cost else 'DECLINE',
                             'condition': 'Signal is observed before action; same feasible actions and losses; constant observation cost.'}
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input'); ap.add_argument('--output')
    args = ap.parse_args()
    try:
        d, sha = read(args.input)
        result = analyze(d)
        result.update(input_sha256=sha, code_sha256=code_hashes(__file__))
        emit(result, args.output)
    except (ValueError, TypeError, OSError) as exc:
        print('INVALID_INPUT_OR_OUTPUT: ' + str(exc))
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
