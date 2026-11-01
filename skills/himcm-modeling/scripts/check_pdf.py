#!/usr/bin/env python3
"""Inspect submission PDF properties (v7.1). --main-pages is pages before the AI-use report.
--max-main-pages is the cap of the contest YEAR being solved (2026: 25); it is no longer hard-coded."""
import argparse,json,hashlib,re,sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('pdf');p.add_argument('--team',required=True);p.add_argument('--main-pages',type=int,required=True);p.add_argument('--max-main-pages',type=int,default=None,help='page cap of that contest year');a=p.parse_args();fp=Path(a.pdf)
    try:import pymupdf as fitz
    except ImportError:
        try:import fitz
        except ImportError:raise SystemExit('PyMuPDF is required for PDF inspection; visual review is still separate.')
    errors=[];review=[];data=fp.read_bytes()
    if not data.startswith(b'%PDF'):raise SystemExit('Not a PDF')
    with fitz.open(fp) as doc:
        total=len(doc)
        if not 1<=a.main_pages<=total:errors.append('INVALID_MAIN_REPORT_PAGE_COUNT')
        if a.max_main_pages is not None and a.main_pages>a.max_main_pages:review.append({'issue':'MAIN_REPORT_OVER_YEAR_CAP_UNLESS_EXCLUDED_SECTIONS (check_gate.py decides, using rules.excluded_from_cap)'})
        if a.max_main_pages is None:review.append({'issue':'NO_YEAR_CAP_GIVEN_PASS_--max-main-pages'})
        if len(data)>=20_000_000:errors.append('FILE_AT_OR_OVER_CONSERVATIVE_20_MB_LIMIT')
        if fp.name!=a.team+'.pdf':errors.append('FILE_NAME_DOES_NOT_MATCH_TEAM')
        for i,page in enumerate(doc):
            text=page.get_text()
            header=page.get_text(clip=fitz.Rect(0,0,page.rect.width,page.rect.height*.18))
            if a.team not in header:review.append({'page':i+1,'issue':'TEAM_HEADER_NOT_DETECTED'})
            if not re.search(r'\bPage\s*\d+',header,re.I):review.append({'page':i+1,'issue':'PAGE_HEADER_NOT_DETECTED'})
            spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['text'].strip()]
            if any(s['size']<11.9 for s in spans):review.append({'page':i+1,'issue':'TEXT_BELOW_12_PT_DETECTED_REVIEW_CAPTIONS_AND_BODY'})
        ai='\n'.join(doc[i].get_text() for i in range(a.main_pages,total))
        if total>a.main_pages and 'Report on Use of AI' not in ai:errors.append('EXTRA_PAGES_NOT_IDENTIFIED_AS_AI_REPORT')
        if total>a.main_pages and 'Report on Use of AI' not in doc[a.main_pages].get_text():errors.append('DECLARED_MAIN_REPORT_BOUNDARY_DOES_NOT_START_AI_REPORT')
        if any(doc.metadata.get(k) for k in ['author','subject','keywords']):review.append({'issue':'DOCUMENT_METADATA_REQUIRES_ANONYMITY_REVIEW'})
    print(json.dumps({'status':'FAIL' if errors else 'STATIC_CHECK_COMPLETE','total_pages':total,'main_pages_declared':a.main_pages,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'errors':errors,'review':review,'visual_review_and_anonymity':'NOT_VERIFIED'},indent=2));sys.exit(1 if errors else 0)

if __name__=='__main__':main()
