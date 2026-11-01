#!/usr/bin/env python3
"""Exact finite-sample state/stock accounting; monotone piecewise-linear curves only."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,sys

def fields(d,expected):
 if not isinstance(d,dict):raise ValueError('JSON object required.')
 if set(d)!=set(expected):raise ValueError('Missing or unknown fields: '+str(sorted(set(d)^set(expected))))

def unique_object(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('Duplicate JSON field: '+k)
  d[k]=v
 return d

def number(x):
 if isinstance(x,bool) or not isinstance(x,(int,str)):raise ValueError('Use integer or exact decimal/fraction string; no float/bool.')
 try:return F(x)
 except (ValueError,ZeroDivisionError) as e:raise ValueError('Invalid finite rational.') from e

def interpolate(x,xs,ys):
 if x<xs[0] or x>xs[-1]:raise ValueError('Outside curve domain; no clipping/extrapolation.')
 for j in range(len(xs)-1):
  if xs[j]<=x<=xs[j+1]:return ys[j]+(ys[j+1]-ys[j])*(x-xs[j])/(xs[j+1]-xs[j])
 raise ValueError('Curve lookup failed.')

def solve(d):
 fields(d,['schema','increment_kind','state_unit','stock_unit','time_unit','curve','samples','initial_time','initial_incremental_stock'])
 if d.get('schema')!='finite-state-stock-v1':raise ValueError('Unsupported schema.')
 if d.get('increment_kind')!='interval_stock_change':raise ValueError('Each increment is an integrated stock change, not a rate.')
 for name in ['state_unit','stock_unit','time_unit']:
  if not isinstance(d.get(name),str) or not d[name].strip():raise ValueError('Explicit units required.')
 c=d.get('curve');s=d.get('samples')
 if not isinstance(c,list) or len(c)<2 or not all(isinstance(r,list) and len(r)==2 for r in c):raise ValueError('Need at least two [state,stock] knots.')
 if not isinstance(s,list) or not s:raise ValueError('Nonempty samples required.')
 xs=[number(r[0]) for r in c];vs=[number(r[1]) for r in c]
 if any(b<=a for a,b in zip(xs,xs[1:])) or any(b<=a for a,b in zip(vs,vs[1:])):raise ValueError('Curve must increase strictly in both coordinates.')
 t0=number(d['initial_time']);credit=number(d['initial_incremental_stock']);last=t0;rows=[];weights=[]
 for item in s:
  fields(item,['time','baseline_state','interval_increment','weight'])
  t=number(item['time']);h=number(item['baseline_state']);dv=number(item['interval_increment']);weight=number(item['weight'])
  if t<=last:raise ValueError('Sample times must increase after initial_time.')
  if weight<0:raise ValueError('Weights must be nonnegative.')
  credit+=dv;base=interpolate(h,xs,vs);new=base+credit;state=interpolate(new,vs,xs)
  rows.append({'time':t,'baseline_state':h,'baseline_stock':base,'interval_increment':dv,'cumulative_increment':credit,'state_after_increment':state});weights.append(weight);last=t
 if sum(weights)!=1:raise ValueError('Explicit observation weights must sum exactly to one.')
 mean_h=sum(w*r['baseline_state'] for w,r in zip(weights,rows));mean_credit=sum(w*r['cumulative_increment'] for w,r in zip(weights,rows));mean_state=sum(w*r['state_after_increment'] for w,r in zip(weights,rows));mean_stock=sum(w*(r['baseline_stock']+r['cumulative_increment']) for w,r in zip(weights,rows));base_at_mean=interpolate(mean_h,xs,vs)
 # A comparison proxy is a separate claim: its domain failure must not erase
 # the valid original observation target. Never clip or extrapolate the proxy.
 def proxy(stock):
  defined=vs[0]<=stock<=vs[-1]
  return {'status':'DEFINED' if defined else 'UNDEFINED_OUTSIDE_CURVE_DOMAIN',
          'stock_argument':stock,'stock_domain':[vs[0],vs[-1]],
          'value':interpolate(stock,vs,xs) if defined else None}
 diagnostics={'end_credit_at_mean_baseline':proxy(base_at_mean+credit),
              'mean_credit_at_mean_baseline':proxy(base_at_mean+mean_credit)}
 proxy_endpoint=diagnostics['end_credit_at_mean_baseline']['value']
 proxy_mean_credit=diagnostics['mean_credit_at_mean_baseline']['value']
 amin=min((b-a)/(y-x) for x,y,a,b in zip(xs,xs[1:],vs,vs[1:]))
 bound=None
 if proxy_endpoint is not None:
  stock_gap=sum(w*abs(r['baseline_stock']-base_at_mean+r['cumulative_increment']-credit) for w,r in zip(weights,rows));bound=stock_gap/amin
  assert abs(proxy_endpoint-mean_state)<=bound
 return {'schema':'finite-state-stock-result-v2','status':'EXACT_TARGET_AND_PROXIES' if all(p['value'] is not None for p in diagnostics.values()) else 'EXACT_TARGET_WITH_UNDEFINED_PROXY','units':{k:d[k] for k in ['state_unit','stock_unit','time_unit']},'rows':rows,'weights':weights,'target_weighted_sample_state':mean_state,'weighted_stock':mean_stock,'stock_at_weighted_baseline_state':base_at_mean,'weighted_incremental_stock':mean_credit,'end_incremental_stock':credit,'proxy_end_credit_at_mean_baseline':proxy_endpoint,'proxy_mean_credit_at_mean_baseline':proxy_mean_credit,'proxy_diagnostics':diagnostics,'proxy_end_minus_target':proxy_endpoint-mean_state if proxy_endpoint is not None else None,'inverse_lipschitz_constant':1/amin,'absolute_proxy_error_bound':bound,'bound_verified':True if bound is not None else None,'scope':'Exact only for supplied finite samples and declared piecewise-linear monotone curve. Weights define the observation target. Each proxy separately requires its stock argument inside the declared curve domain; undefined proxies have no value or associated error-bound certification. Not physical identification, continuous-time mean, rate integration, feedback simulation or automatic unit conversion.'}

def encode(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,list):return [encode(y) for y in x]
 if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
 return x

def main():
 ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);args=ap.parse_args()
 try:
  d=json.loads(args.input.read_text(),object_pairs_hook=unique_object);result=solve(d)
 except (ValueError,KeyError,TypeError,OSError) as e:
  print(json.dumps({'status':'INVALID_INPUT','error':str(e)}));return 2
 print(json.dumps(encode(result),ensure_ascii=False,indent=2));return 0
if __name__=='__main__':sys.exit(main())
