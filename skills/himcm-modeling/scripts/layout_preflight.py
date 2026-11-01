"""Measure all fixed HTML pages at scale=1; never rewrite content or save a PDF.

Scoped to PyMuPDF insert_htmlbox and the explicitly supplied CSS/rectangle.
Geometric fit does not prove legibility, scientific accuracy or missing-asset coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import pymupdf as fitz


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fits(html: str, css: str, width: float, height: float) -> tuple[float, float]:
    with fitz.open() as doc:
        page = doc.new_page(width=width, height=height)
        result = page.insert_htmlbox(fitz.Rect(0, 0, width, height), html,
                                     css=css, scale_low=1)
        return float(result[0]), float(result[1])


def inspect_pages(pages: list[str], css: str, width: float, height: float,
                  max_height: float = 2400) -> dict:
    if not isinstance(pages, list) or not 1 <= len(pages) <= 100:
        raise ValueError('pages must be a nonempty array with at most 100 entries')
    if any(not isinstance(p, str) or not p.strip() for p in pages):
        raise ValueError('each page must be a nonempty HTML string')
    if not isinstance(css, str):
        raise ValueError('CSS must be text')
    if any(isinstance(x, bool) or not isinstance(x, (int, float))
           or not math.isfinite(x) for x in (width, height, max_height)):
        raise ValueError('dimensions must be finite real numbers')
    if not (36 <= width <= 2000 and 36 <= height <= max_height <= 14400):
        raise ValueError('unsupported dimensions or height search cap')
    rows = []
    for number, html in enumerate(pages, 1):
        spare, scale = fits(html, css, width, height)
        row = {'page': number, 'html_sha256': sha(html.encode()),
               'fits_at_original_scale': spare >= 0 and scale == 1,
               'spare_height': spare, 'scale': scale,
               'height_bound': None, 'height_search_status': None}
        # This is a diagnostic bracket under the fixed-layout API, not a general
        # monotonicity proof for arbitrary HTML/CSS. Confirm both final endpoints.
        low, high = 1.0, float(max_height)
        if fits(html, css, width, high)[0] < 0:
            row['height_search_status'] = 'CAPPED_OR_WIDTH_CONSTRAINED'
        elif fits(html, css, width, low)[0] >= 0:
            row['height_search_status'] = 'NO_POSITIVE_LOWER_BOUND'
        else:
            for _ in range(18):
                mid = (low + high) / 2
                if fits(html, css, width, mid)[0] >= 0:
                    high = mid
                else:
                    low = mid
            low_fits = fits(html, css, width, low)[0] >= 0
            high_fits = fits(html, css, width, high)[0] >= 0
            row['height_bound'] = {'fails_at': low, 'fits_at': high,
                                   'tolerance_pt': high - low,
                                   'endpoints_confirmed': not low_fits and high_fits}
            row['height_search_status'] = 'ENDPOINTS_CONFIRMED' if not low_fits and high_fits else 'UNSTABLE'
        rows.append(row)
    return {'engine': 'PyMuPDF', 'version': fitz.VersionBind,
            'css_sha256': sha(css.encode()), 'width_pt': width, 'height_pt': height,
            'scale_low': 1, 'pages': rows,
            'all_pages_fit': all(r['fits_at_original_scale'] for r in rows),
            'overflow_pages': [r['page'] for r in rows if not r['fits_at_original_scale']],
            'scope': 'Geometry only. Actual PDF text, assets, readability and scientific content require separate verification.'}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pages', required=True, type=Path)
    ap.add_argument('--css', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--width', type=float, default=522)
    ap.add_argument('--height', type=float, default=695)
    ap.add_argument('--max-height', type=float, default=2400)
    args = ap.parse_args()
    if args.output.exists():
        ap.error('output already exists; use a fresh evidence path')
    try:
        report = inspect_pages(json.loads(args.pages.read_text()), args.css.read_text(),
                               args.width, args.height, args.max_height)
    except (ValueError, TypeError, RuntimeError) as exc:
        print(json.dumps({'status': 'INVALID_OR_UNSUPPORTED', 'error': str(exc)}))
        return 2
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'all_pages_fit': report['all_pages_fit'],
                      'overflow_pages': report['overflow_pages']}))
    return 0 if report['all_pages_fit'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
