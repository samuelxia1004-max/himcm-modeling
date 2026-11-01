"""Small strict JSON/rational helpers. No external dependencies."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path


def number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError('expected integer, decimal, or rational string')
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError('invalid finite rational: ' + repr(value)) from exc


def keys(obj, required, optional=()):
    if not isinstance(obj, dict):
        raise ValueError('expected object')
    missing = set(required) - obj.keys()
    extra = obj.keys() - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f'missing keys {sorted(missing)}; unknown keys {sorted(extra)}')


def vector(v, n=None):
    if not isinstance(v, list) or not v or (n is not None and len(v) != n):
        raise ValueError('invalid vector length')
    return [number(x) for x in v]


def matrix(v, rows, cols):
    if not isinstance(v, list) or len(v) != rows:
        raise ValueError('invalid matrix rows')
    return [vector(row, cols) for row in v]


def names(v):
    if (not isinstance(v, list) or not v or
            any(not isinstance(x, str) or not x.strip() for x in v) or
            len(set(v)) != len(v)):
        raise ValueError('names must be a nonempty list of distinct nonempty strings')
    return v


def probability(v, n):
    v = vector(v, n)
    if min(v) < 0 or sum(v) != 1:
        raise ValueError('probabilities must be nonnegative and sum exactly to 1')
    return v


def strict_pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key: ' + k)
        result[k] = v
    return result


def read(path):
    raw = Path(path).read_bytes()
    return json.loads(raw, parse_float=str, object_pairs_hook=strict_pairs,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s))), hashlib.sha256(raw).hexdigest()


def encode(x):
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, list):
        return [encode(v) for v in x]
    return x


def emit(result, output=None):
    body = json.dumps(encode(result), ensure_ascii=False, indent=2) + '\n'
    if output:
        with open(output, 'x', encoding='utf-8') as f:
            f.write(body)
    else:
        print(body, end='')


def code_hashes(script):
    return {Path(p).name: hashlib.sha256(Path(p).read_bytes()).hexdigest()
            for p in [script, __file__]}
