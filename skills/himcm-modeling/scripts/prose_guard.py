#!/usr/bin/env python3
"""Compare protected surface tokens. Differences require semantic review."""
import argparse,json,re,collections
from pathlib import Path

def tokens(s):
    pats={'numbers':r'(?<![\w])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?%?',
          'citations':r'\\cite\w*\{[^}]+\}|\[@[^\]]+\]|https?://[^\s)]+',
          'math':r'\$\$[\s\S]*?\$\$|(?<!\$)\$[^\n$]+\$(?!\$)|\\\[[\s\S]*?\\\]'}
    return {k:collections.Counter(re.findall(p,s)) for k,p in pats.items()}

def main():
    p=argparse.ArgumentParser();p.add_argument('before');p.add_argument('after');a=p.parse_args();b=Path(a.before).read_text();c=Path(a.after).read_text();x,y=tokens(b),tokens(c);diff={}
    for k in x:
        if x[k]!=y[k]:diff[k]={'removed':list((x[k]-y[k]).elements()),'added':list((y[k]-x[k]).elements())}
    warnings=[]
    for name,pat in [('inflated_prose',r'\b(?:groundbreaking|delve|tapestry|pivotal|revolutionary)\b'),('formulaic_contrast',r'\bnot (?:just|only)\b'),('chat_residue',r'\b(?:I hope this helps|let me know|Would you like)\b')]:
        if re.search(pat,c,re.I):warnings.append(name)
    print(json.dumps({'status':'TOKEN_DIFFERENCES_REQUIRE_REVIEW' if diff else 'PROTECTED_TOKEN_COUNTS_MATCH','differences':diff,'style_review_flags':warnings,'scientific_meaning_and_authorship':'REQUIRES_HUMAN_OR_AGENT_REVIEW'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
