#!/usr/bin/env python3
"""Exact first-moment and monotone-integral bounds; prospective development only.

No data-validity, global novelty, physical dynamics or award certification.
"""
import argparse
import hashlib
from pathlib import Path
from fractions import Fraction as F
from _exact_io import keys, read, emit
from _moment_core import rational, moment_bounds, integral_bounds, decision


def unpack(d):
    if not isinstance(d, dict):
        raise ValueError('expected object')
    if d.get('kind') == 'first_moment_piecewise_linear':
        keys(d, ['kind', 'points', 'mean'])
        p = d['points']
        if not isinstance(p, list) or not 2 <= len(p) <= 64:
            raise ValueError('expected2..64 ordered breakpoints')
        if any(not isinstance(row, list) or len(row) != 2 for row in p):
            raise ValueError('breakpoints must be [x,y] pairs')
        points = [(rational(x), rational(y)) for x, y in p]
        mu = rational(d['mean'])
        if any(u[0] >= v[0] for u, v in zip(points, points[1:])):
            raise ValueError('x must strictly increase')
        if not points[0][0] <= mu <= points[-1][0]:
            raise ValueError('infeasible mean')
        return points, mu, F(0), F(1), None
    if d.get('kind') == 'bounded_monotone_integral':
        keys(d, ['kind','length','lower_area','upper_area','total_integral','start','stop'], ['available'])
        L,A0,A1,I,a,b = [rational(d[k]) for k in ['length','lower_area','upper_area','total_integral','start','stop']]
        if not (L>0 and 0<=A0<=A1 and 0<=a<=b<=L):
            raise ValueError('invalid domain/shape constraints')
        if not A0*L<=I<=A1*L:
            raise ValueError('infeasible integral')
        available = rational(d['available']) if 'available' in d else None
        if A0==A1:
            return None, None, A0*(b-a), F(0), available
        points=[(t,max(F(0),b-max(a,t))) for t in sorted({F(0),a,b,L})]
        return points,(A1*L-I)/(A1-A0),A0*(b-a),A1-A0,available
    raise ValueError('unsupported kind')


def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x


def solve(d):
    points,mu,offset,scale,available=unpack(d)
    certificate=moment_bounds(points,mu) if points is not None else None
    low=offset+scale*certificate['lower']['value'] if certificate else offset
    high=offset+scale*certificate['upper']['value'] if certificate else offset
    out={'status':'EXACT_BOUNDS','kind':d['kind'],'lower':low,'upper':high,
         'constant_case':points is None,'certificate':certificate,
         'scope':'Only the exact input-defined mathematical class. For monotone integrals jumps are allowed; additional physical/smoothness constraints define a subset and can invalidate an ambiguity claim. These remain valid outer bounds for that subset.'}
    if available is not None:
        out['decision']=decision(available,out)
    return out


def verify(d,result):
    """Feasibility + affine dominance + equality, without rerunning the optimizer.

    Reconstruct model from the separately supplied original input, never from an
    untrusted certificate's claimed mean or knots. Empty problem domains rejected.
    """
    points,mu,offset,scale,available=unpack(d)
    if not isinstance(result,dict) or result.get('kind')!=d['kind'] or result.get('status')!='EXACT_BOUNDS':
        raise ValueError('certificate header mismatch')
    expected_constant=points is None
    if result.get('constant_case') is not expected_constant:
        raise ValueError('constant-case mismatch')
    if points is None:
        if result.get('certificate') is not None:
            raise ValueError('constant case requires direct certificate')
        if rational(result['lower'])!=offset or rational(result['upper'])!=offset:
            raise ValueError('wrong constant bound')
    else:
        c=result.get('certificate')
        keys(c,['mean','points','lower','upper'])
        if rational(c['mean'])!=mu:
            raise ValueError('mean mismatch')
        if not isinstance(c['points'],list) or any(not isinstance(p,list) or len(p)!=2 for p in c['points']):
            raise ValueError('invalid claimed knots')
        if [(rational(x),rational(y)) for x,y in c['points']]!=points:
            raise ValueError('knots mismatch')
        def g(x):
            if not points[0][0]<=x<=points[-1][0]:
                raise ValueError('atom outside support')
            for (a,u),(b,v) in zip(points,points[1:]):
                if a<=x<=b:return u+(v-u)*(x-a)/(b-a)
            raise ValueError('unhandled support')
        for side in ['lower','upper']:
            q=c[side];keys(q,['value','atoms','dual_intercept','dual_slope'])
            if not isinstance(q['atoms'],list) or not 1<=len(q['atoms'])<=2 or any(not isinstance(p,list) or len(p)!=2 for p in q['atoms']):
                raise ValueError('expected1..2 [location,weight] atoms')
            atoms=[(rational(x),rational(w)) for x,w in q['atoms']]
            if any(w<0 for x,w in atoms) or sum(w for x,w in atoms)!=1 or sum(x*w for x,w in atoms)!=mu:
                raise ValueError('infeasible primal mass/mean')
            value=rational(q['value']);a=rational(q['dual_intercept']);b=rational(q['dual_slope'])
            if sum(g(x)*w for x,w in atoms)!=value or a+b*mu!=value:
                raise ValueError('nonzero primal-dual gap')
            if not all(a+b*x<=y if side=='lower' else a+b*x>=y for x,y in points):
                raise ValueError('infeasible affine dual')
            if rational(result[side])!=offset+scale*value:
                raise ValueError('transformed bound mismatch')
    if rational(result['lower'])>rational(result['upper']):
        raise ValueError('bounds reversed')
    if available is not None:
        b={'lower':rational(result['lower']),'upper':rational(result['upper'])}
        if result.get('decision')!=decision(available,b):raise ValueError('decision mismatch')
    elif 'decision' in result:
        raise ValueError('decision without supplied action')
    return {'status':'EXACT_CERTIFICATE_VALID','valid':True,
            'scope':'Mathematical feasibility, affine dominance and equal bounds only; original data, modeling assumptions and program provenance require separate verification.'}


def code_hashes():
    here=Path(__file__).resolve().parent
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),here/'_moment_core.py',here/'_exact_io.py']}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input');ap.add_argument('--verify');ap.add_argument('--output')
    args=ap.parse_args()
    try:
        d,h=read(args.input)
        if args.verify:
            cert,ch=read(args.verify);result=verify(d,cert);result['certificate_file_sha256']=ch
        else:result=solve(d)
        result.update(input_sha256=h,code_sha256=code_hashes())
        emit(encode(result),args.output)
    except (ValueError,TypeError,KeyError,OSError,ArithmeticError) as e:
        print('INVALID_INPUT_OR_CERTIFICATE_OR_OUTPUT: '+str(e))
        return 2
    return 0


if __name__=='__main__':raise SystemExit(main())
