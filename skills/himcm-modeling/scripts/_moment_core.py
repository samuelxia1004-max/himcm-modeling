"""Exact sharp bounds for a subinterval integral of a bounded monotone function.

PROSPECTIVE RESEARCH PROTOTYPE; not installed or added to any frozen skill.
The class permits jumps. Smoothness/slope constraints require a different model.
Inputs are integers, Fraction objects, or exact rational/decimal strings; not floats.
Primal certificates use <=2 atoms; dual certificates are affine at all breakpoints.
"""
from fractions import Fraction as F
from itertools import combinations

def rational(value):
    if isinstance(value,bool) or isinstance(value,float):
        raise ValueError('Use an integer, Fraction, or exact string, not bool/float.')
    if not isinstance(value,(int,str,F)):raise ValueError('Unsupported exact input type.')
    try:return F(value)
    except (ValueError,ZeroDivisionError,TypeError) as e:raise ValueError('Invalid rational.') from e

def moment_bounds(points, mean):
    """Bounds E[g(T)] for a continuous piecewise-linear g and fixed E[T].
    The ordered points completely specify g on the compact support.
    Atom reduction to endpoints preserves both first moment and linear objective.
    """
    pts=[(rational(x),rational(y)) for x,y in points];mu=rational(mean)
    if len(pts)<2 or any(x2<=x1 for (x1,_),(x2,_) in zip(pts,pts[1:])):
        raise ValueError('Need >=2 strictly increasing support breakpoints.')
    if not pts[0][0]<=mu<=pts[-1][0]:raise ValueError('Infeasible mean.')
    primal=[]
    for x,y in pts:
        if x==mu:primal.append({'value':y,'atoms':[(x,F(1))]})
    for (x,y),(z,v) in combinations(pts,2):
        if x<=mu<=z:
            weight=(z-mu)/(z-x)
            primal.append({'value':weight*y+(1-weight)*v,'atoms':[(x,weight),(z,1-weight)]})
    # A dual affine minorant/majorant at every knot also bounds each linear segment.
    lines={(y,F(0)) for x,y in pts}
    for (x,y),(z,v) in combinations(pts,2):
        slope=(v-y)/(z-x);lines.add((y-slope*x,slope))
    lower=[(a+b*mu,a,b) for a,b in lines if all(a+b*x<=y for x,y in pts)]
    upper=[(a+b*mu,a,b) for a,b in lines if all(a+b*x>=y for x,y in pts)]
    low=min(primal,key=lambda p:p['value']);high=max(primal,key=lambda p:p['value'])
    ld=max(lower);ud=min(upper)
    assert low['value']==ld[0] and high['value']==ud[0], 'Primal/dual gap'
    return {'mean':mu,'points':pts,'lower':{'value':low['value'],'atoms':low['atoms'],'dual_intercept':ld[1],'dual_slope':ld[2]},'upper':{'value':high['value'],'atoms':high['atoms'],'dual_intercept':ud[1],'dual_slope':ud[2]}}

def integral_bounds(length, lower_area, upper_area, total_integral, start, stop):
    """Let A be nondecreasing, A0<=A<=A1, integral_0^L A=I.
    Return sharp bounds on integral_a^b A, for the monotone measurable class.
    Point endpoints may be assigned A(0)=A0, A(L)=A1; jumps are permitted.
    Continuous physical classes form subsets, so these remain outer bounds.
    """
    L,A0,A1,I,a,b=map(rational,(length,lower_area,upper_area,total_integral,start,stop))
    if not (L>0 and 0<=A0<=A1 and 0<=a<=b<=L):raise ValueError('Invalid domain/shape constraints.')
    if not A0*L<=I<=A1*L:raise ValueError('Total integral infeasible under endpoint bounds.')
    if A0==A1:
        value=A0*(b-a)
        return {'lower':value,'upper':value,'constant_case':True,'certificate':None}
    # A(t)=A0+(A1-A0)F_T(t); Fubini gives E[T]=(A1 L-I)/(A1-A0).
    mean=(A1*L-I)/(A1-A0)
    knots=sorted({F(0),a,b,L})
    g=lambda t:max(F(0),b-max(a,t))
    cert=moment_bounds([(t,g(t)) for t in knots],mean)
    return {'lower':A0*(b-a)+(A1-A0)*cert['lower']['value'],'upper':A0*(b-a)+(A1-A0)*cert['upper']['value'],'constant_case':False,'certificate':cert}

def decision(available, bounds):
    available=rational(available)
    if available>=bounds['upper']:return 'covers_every_admissible_curve'
    if available<bounds['lower']:return 'insufficient_for_every_admissible_curve'
    return 'not_identified_from_current_information'

def serializable(x):
    if isinstance(x,F):return {'exact':str(x),'decimal':float(x)}
    if isinstance(x,dict):return {k:serializable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serializable(v) for v in x]
    return x
