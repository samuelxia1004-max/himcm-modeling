#!/usr/bin/env python3
"""Exact small finite-world information policies. Explicit joint priors only."""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path


class LimitExceeded(ValueError):
    pass


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError('Use exact rational strings or integers, not booleans/floats')
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError('Invalid finite rational: ' + str(value)) from error


def names(value, maximum):
    if not isinstance(value, list) or not 1 <= len(value) <= maximum or any(not isinstance(x, str) or not x.strip() for x in value) or len(set(value)) != len(value):
        raise ValueError('Invalid names or supported size exceeded')
    return value


def keys(value, required):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError('Expected exactly fields: ' + ','.join(required))


def parse(d):
    keys(d, ['schema_version', 'actions', 'worlds', 'probabilities', 'losses', 'tests', 'resource_budget', 'all_actions_feasible_in_all_worlds'])
    if type(d['schema_version']) is not int or d['schema_version'] != 1 or d['all_actions_feasible_in_all_worlds'] is not True:
        raise ValueError('Version1 and explicit common feasibility declaration required')
    actions, worlds = names(d['actions'], 16), names(d['worlds'], 64)
    if not isinstance(d['probabilities'], list) or len(d['probabilities']) != len(worlds):
        raise ValueError('One explicit probability per world required')
    p = tuple(map(number, d['probabilities']))
    if min(p) < 0 or sum(p) != 1:
        raise ValueError('Prior probabilities must be nonnegative and sum exactly to one')
    if not isinstance(d['losses'], list) or len(d['losses']) != len(actions) or any(not isinstance(row, list) or len(row) != len(worlds) for row in d['losses']):
        raise ValueError('Loss matrix must be actions by worlds')
    losses = tuple(tuple(map(number, row)) for row in d['losses'])
    raw = d['tests']
    if not isinstance(raw, list) or len(raw) > 8:
        raise ValueError('At most eight one-use tests supported')
    tests = []
    for item in raw:
        keys(item, ['name', 'outcomes_by_world', 'loss_cost', 'resource_cost'])
        if not isinstance(item['name'], str) or not item['name'].strip():
            raise ValueError('Test name required')
        outcomes = item['outcomes_by_world']
        if not isinstance(outcomes, list) or len(outcomes) != len(worlds) or any(not isinstance(x, str) or not x for x in outcomes):
            raise ValueError('One nonempty deterministic outcome label per joint world required')
        cost = number(item['loss_cost'])
        resource = item['resource_cost']
        if cost < 0 or type(resource) is not int or resource < 0:
            raise ValueError('Nonnegative loss cost and integer resource cost required')
        tests.append((item['name'], tuple(outcomes), cost, resource))
    if len({t[0] for t in tests}) != len(tests):
        raise ValueError('Duplicate test names')
    budget = d['resource_budget']
    if type(budget) is not int or not 0 <= budget <= 64:
        raise ValueError('Integer resource budget must be in [0,64]')
    return actions, worlds, p, losses, tests, budget


def analyze(d, max_nodes=50000):
    if type(max_nodes) is not int or max_nodes < 1:
        raise ValueError('Positive integer node cap required')
    actions, worlds, p, losses, tests, budget = parse(d)
    support = tuple(i for i, probability in enumerate(p) if probability)
    available = tuple(range(len(tests)))
    count = [0]

    def stop(support):
        values = tuple(sum(p[w] * row[w] for w in support) for row in losses)
        return min(values), values.index(min(values))

    def branches(support, test):
        grouped = {}
        for w in support:
            grouped.setdefault(tests[test][1][w], []).append(w)
        return {label: tuple(grouped[label]) for label in sorted(grouped)}

    @lru_cache(None)
    def solve(support, available, budget):
        count[0] += 1
        if count[0] > max_nodes:
            raise LimitExceeded('DP node cap reached; no optimal result issued')
        best, action = stop(support)
        choice = ('action', action)
        options = {'stop': best}
        mass = sum(p[w] for w in support)
        for test in available:
            if tests[test][3] > budget:
                continue
            rest = tuple(t for t in available if t != test)
            value = mass * tests[test][2] + sum(solve(part, rest, budget - tests[test][3])[0] for part in branches(support, test).values())
            options[test] = value
            if value < best:  # Prefer stopping on exact ties, then input test order.
                best, choice = value, ('test', test)
        return best, choice, options

    def policy(support, available, budget):
        value, (kind, chosen), _ = solve(support, available, budget)
        mass = sum(p[w] for w in support)
        if kind == 'action':
            return {'action': actions[chosen], 'conditional_expected_loss': str(value / mass)}
        rest = tuple(t for t in available if t != chosen)
        return {'test': tests[chosen][0], 'conditional_expected_total_loss': str(value / mass),
                'outcomes': {label: {'conditional_probability': str(sum(p[w] for w in part) / mass),
                                     'then': policy(part, rest, budget - tests[chosen][3])}
                             for label, part in branches(support, chosen).items()}}

    @lru_cache(None)
    def myopic(support, available, budget):
        immediate, action = stop(support)
        chosen = None
        mass = sum(p[w] for w in support)
        for test in available:
            if tests[test][3] <= budget:
                value = mass * tests[test][2] + sum(stop(part)[0] for part in branches(support, test).values())
                if value < immediate:
                    immediate, chosen = value, test
        if chosen is None:
            return immediate
        rest = tuple(t for t in available if t != chosen)
        return mass * tests[chosen][2] + sum(myopic(part, rest, budget - tests[chosen][3]) for part in branches(support, chosen).values())

    optimal, _, options = solve(support, available, budget)
    policy_result = policy(support, available, budget)
    no_test = stop(support)[0]
    perfect = sum(p[w] * min(row[w] for row in losses) for w in support)
    repeated_myopic = myopic(support, available, budget)
    fixed = []
    for size in range(len(tests) + 1):
        for subset in itertools.combinations(available, size):
            resource = sum(tests[t][3] for t in subset)
            if resource > budget:
                continue
            groups = {}
            for w in support:
                outcome = tuple(tests[t][1][w] for t in subset)
                groups.setdefault(outcome, []).append(w)
            value = sum(tests[t][2] for t in subset) + sum(stop(tuple(part))[0] for part in groups.values())
            fixed.append({'tests': [tests[t][0] for t in subset], 'expected_total_loss': str(value), 'resource_used': resource})
    best_fixed = min(number(x['expected_total_loss']) for x in fixed)
    if not perfect <= optimal <= repeated_myopic <= no_test or optimal > best_fixed:
        raise ArithmeticError('Information-policy comparison invariant violated')
    one_step = {tests[t][0]: str(tests[t][2] + sum(stop(part)[0] for part in branches(support, t).values()))
                for t in available if tests[t][3] <= budget}
    return {'status': 'OPTIMAL_WITHIN_EXPLICIT_FINITE_MODEL',
            'scope': 'Finite explicit joint worlds and prior; one-use pre-action tests, constant nonnegative loss costs, per-path integer resource cap, all terminal actions feasible. This certifies neither real-world prior/feasibility nor larger/continuous/adaptive-intervention models.',
            'tie_rule': 'Stop on exact ties; otherwise input test/action order',
            'no_information_loss': str(no_test), 'perfect_world_information_loss': str(perfect),
            'optimal_adaptive_loss': str(optimal), 'receding_myopic_loss': str(repeated_myopic),
            'best_fixed_set_loss': str(best_fixed), 'net_gain_vs_no_information': str(no_test - optimal),
            'gain_vs_receding_myopic': str(repeated_myopic - optimal), 'gain_vs_fixed_set': str(best_fixed - optimal),
            'single_test_then_stop_losses': one_step,
            'root_choices_with_optimal_continuation': [{'choice': 'STOP' if k == 'stop' else tests[k][0], 'expected_total_loss': str(v)} for k, v in options.items()],
            'optimal_policy': policy_result, 'fixed_set_alternatives': fixed,
            'DP_nodes_evaluated': count[0], 'max_nodes': max_nodes,
            'zero_probability_worlds_excluded': [worlds[w] for w in range(len(worlds)) if not p[w]],
            'Q': None, 'I': None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--max-nodes', type=int, default=50000)
    args = parser.parse_args()
    code = 0
    try:
        raw = args.input.read_bytes()
        data = json.loads(raw, object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))
        result = analyze(data, args.max_nodes)
        result.update(input_sha256=hashlib.sha256(raw).hexdigest(), code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    except LimitExceeded as error:
        result, code = {'status': 'INCOMPLETE_RESOURCE_LIMIT', 'error': str(error), 'optimal_adaptive_loss': None}, 2
    except (ValueError, TypeError, OSError, KeyError) as error:
        result, code = {'status': 'INVALID_INPUT_OR_OUTPUT', 'error': str(error)}, 2
    encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    if args.output:
        try:
            with args.output.open('x', encoding='utf-8') as out:
                out.write(encoded)
        except OSError as error:
            print(json.dumps({'status': 'INVALID_INPUT_OR_OUTPUT', 'error': str(error)}))
            return 2
    print(encoded, end='')
    return code


if __name__ == '__main__':
    raise SystemExit(main())
