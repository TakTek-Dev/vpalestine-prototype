"""VPalestine marks, drawn from Anybody's own outlines.

python -I tools/brand.py            -> assets/brand/*.svg + assets/js/marks.js
python -I tools/brand.py --explore  -> .impeccable/marks/explore.html (construction variants, not shipped)

The mark is the V printed the way the posters were: two screens, two inks.
The left stroke is pulled in the film ink, the right stroke in the music ink, and where the two strokes
cross at the foot of the letter the inks overprint into a third colour that belongs to both.
PALESTINE is Anybody set at the same cap height, in the key plate.
"""
import os, sys, json
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'research', 'font-src', 'Anybody_wdth-wght.ttf')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inks import INK  # noqa: E402

CAP = 1350  # Anybody cap height (2000 upm)


def instance(wdth, wght):
    return instancer.instantiateVariableFont(TTFont(SRC), {'wdth': wdth, 'wght': wght})


def kerning(font):
    """Pair kerning from GPOS 'kern' lookups (PairPos formats 1 and 2), as {(left, right): xAdvance}."""
    gpos = font['GPOS'].table
    idx = set()
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'kern':
            idx.update(fr.Feature.LookupListIndex)
    pairs = {}
    for li in sorted(idx):
        lookup = gpos.LookupList.Lookup[li]
        for st in lookup.SubTable:
            if st.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, 'LookupType', 2) != 2:
                continue
            cov = st.Coverage.glyphs
            if st.Format == 1:
                for i, first in enumerate(cov):
                    for pvr in st.PairSet[i].PairValueRecord:
                        v = pvr.Value1.XAdvance if pvr.Value1 and hasattr(pvr.Value1, 'XAdvance') else 0
                        pairs.setdefault((first, pvr.SecondGlyph), v or 0)
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs
                c2 = st.ClassDef2.classDefs
                seconds = {}
                for g, c in c2.items():
                    seconds.setdefault(c, []).append(g)
                for first in cov:
                    k1 = c1.get(first, 0)
                    rec = st.Class1Record[k1]
                    for k2, r2 in enumerate(rec.Class2Record):
                        v = r2.Value1.XAdvance if r2.Value1 and hasattr(r2.Value1, 'XAdvance') else 0
                        if not v:
                            continue
                        for second in seconds.get(k2, []):
                            pairs.setdefault((first, second), v)
    return pairs


def set_text(font, text, tracking=0):
    """Outline path (y up, baseline 0) and advance of a string, kerned, with extra tracking in font units."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    kern = kerning(font)
    names = [cmap[ord(c)] for c in text]
    pen = SVGPathPen(gs)
    x = 0
    dots = []
    for i, n in enumerate(names):
        if n == 'i':
            # Anybody's tittle is a flat bar that reads as a macron at display sizes; the wordmark's i takes
            # a round dot instead: one halftone dot, the only round form in the identity
            rec = RecordingPen()
            gs[n].draw(rec)
            contour, keep = [], []
            for op, args in rec.value:
                contour.append((op, args))
                if op == 'closePath':
                    ys = [p[1] for _, a in contour for p in a]
                    if min(ys) < 1250:
                        keep += contour
                    else:
                        x0 = min(p[0] for _, a in contour for p in a)
                        x1 = max(p[0] for _, a in contour for p in a)
                        dots.append((x + (x0 + x1) / 2, max(ys)))
                    contour = []
            rp = RecordingPen()
            rp.value = keep
            rp.replay(TransformPen(pen, (1, 0, 0, 1, x, 0)))
        else:
            gs[n].draw(TransformPen(pen, (1, 0, 0, 1, x, 0)))
        x += font['hmtx'][n][0] + tracking
        if i + 1 < len(names):
            x += kern.get((n, names[i + 1]), 0)
    d = pen.getCommands()
    for cx, top in dots:
        r = 150
        cy = top - r
        d += f'M{cx + r:.1f} {cy:.1f}A{r} {r} 0 1 0 {cx - r:.1f} {cy:.1f}A{r} {r} 0 1 0 {cx + r:.1f} {cy:.1f}Z'
    return d, x - tracking


def bounds_of(font, text):
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    bp = BoundsPen(gs)
    gs[cmap[ord(text)]].draw(bp)
    return bp.bounds


def v_strokes(top_w, foot, cross_y, cap=CAP, width=None):
    """The V as two straight strokes.

    top_w   horizontal width of each stroke at the cap line
    foot    half-width of the flat foot at the baseline
    cross_y height where the inner edges cross (the top of the overprint)
    Returns (left polygon, right polygon, overprint polygon) in font units, y up.
    """
    W = width or 1067
    c = W / 2
    # outer edges run from the cap corners to the ends of the foot
    lo_top, lo_bot = (0, cap), (c - foot, 0)
    ro_top, ro_bot = (W, cap), (c + foot, 0)
    # inner edges run from the inner cap corners through the crossing point to the far end of the foot
    li_top = (top_w, cap)
    ri_top = (W - top_w, cap)
    # left inner edge passes through (c, cross_y); extend it to the baseline
    def at_base(p, q):
        (x1, y1), (x2, y2) = p, q
        return x1 + (x2 - x1) * (0 - y1) / (y2 - y1)
    li_bot = (at_base(li_top, (c, cross_y)), 0)
    ri_bot = (at_base(ri_top, (c, cross_y)), 0)
    left = [lo_top, li_top, li_bot, lo_bot]
    right = [ri_top, ro_top, ro_bot, ri_bot]
    # overprint: below the crossing, bounded by the two inner edges, clipped to the foot
    over = [(c, cross_y), (min(li_bot[0], c + foot), 0), (max(ri_bot[0], c - foot), 0)]
    return left, right, over


def poly(points, dx=0, dy=0, cap=CAP):
    """Polygon in font units (y up) to an SVG path in a y-down box of height cap."""
    return 'M' + 'L'.join(f'{x + dx:.1f} {cap - y + dy:.1f}' for x, y in points) + 'Z'


def glyph_path(cmds, dx=0, cap=CAP):
    """Wrap font-space outline commands in a flip so they draw y-down."""
    return f'<path transform="translate({dx:.1f} {cap}) scale(1 -1)" d="{cmds}"/>'


def explore():
    out = os.path.join(ROOT, '.impeccable', 'marks')
    os.makedirs(out, exist_ok=True)
    variants = [
        ('A · glyph split, sliver', dict(top_w=384, foot=277, cross_y=268)),
        ('B · keystone 1/4', dict(top_w=384, foot=277, cross_y=340)),
        ('C · keystone 1/3', dict(top_w=372, foot=250, cross_y=450)),
        ('D · keystone 2/5, narrow foot', dict(top_w=360, foot=190, cross_y=540)),
        ('E · pointed foot', dict(top_w=360, foot=60, cross_y=520)),
        ('F · light strokes, deep', dict(top_w=300, foot=150, cross_y=430)),
    ]
    font = instance(72, 860)
    word, adv = set_text(font, 'PALESTINE', tracking=10)
    word_lc, adv_lc = set_text(font, 'Palestine', tracking=0)
    cells = []
    for label, p in variants:
        L, R, O = v_strokes(**p)
        gap = 70
        w = 1067 + gap + adv
        svg = (f'<svg viewBox="-40 -40 {w + 80:.0f} {CAP + 80}" width="560">'
               f'<path fill="{INK["film"]}" d="{poly(L)}"/>'
               f'<path fill="{INK["music"]}" d="{poly(R)}"/>'
               f'<path fill="{INK["over"]}" d="{poly(O)}"/>'
               f'<g fill="{INK["key"]}">{glyph_path(word, 1067 + gap)}</g></svg>')
        mono = (f'<svg viewBox="-40 -40 1147 1430" width="120">'
                f'<path fill="{INK["film"]}" d="{poly(L)}"/><path fill="{INK["music"]}" d="{poly(R)}"/>'
                f'<path fill="{INK["over"]}" d="{poly(O)}"/></svg>')
        small = mono.replace('width="120"', 'width="24"')
        cells.append(f'<figure><figcaption>{label}</figcaption>{svg}<div class="row">{mono}{small}'
                     f'<span class="dark">{mono.replace(INK["film"], INK["film_d"]).replace(INK["music"], INK["music_d"]).replace(INK["over"], INK["over_d"])}</span></div></figure>')
    L, R, O = v_strokes(**variants[2][1])
    lc = (f'<svg viewBox="-40 -40 {1067 + 70 + adv_lc + 80:.0f} {CAP + 80}" width="560">'
          f'<path fill="{INK["film"]}" d="{poly(L)}"/><path fill="{INK["music"]}" d="{poly(R)}"/>'
          f'<path fill="{INK["over"]}" d="{poly(O)}"/><g fill="{INK["key"]}">{glyph_path(word_lc, 1137)}</g></svg>')
    cells.append(f'<figure><figcaption>C with mixed-case Palestine</figcaption>{lc}</figure>')
    html = ('<!doctype html><meta charset="utf-8"><style>body{background:' + INK['stock'] + ';font:13px system-ui;margin:24px;'
            'display:grid;grid-template-columns:repeat(2,1fr);gap:28px}figure{margin:0}figcaption{margin-bottom:8px;font-weight:600}'
            '.row{display:flex;gap:18px;align-items:end;margin-top:10px}.dark{background:' + INK['stock_d'] + ';padding:8px}</style>'
            + ''.join(cells))
    open(os.path.join(out, 'explore.html'), 'w', encoding='utf-8').write(html)
    print('wrote', os.path.join(out, 'explore.html'))


if __name__ == '__main__':
    if '--explore' in sys.argv:
        explore()


# the shipped construction: variant D from the explore sheet (keystone at two fifths, narrow foot)
V = dict(top_w=360, foot=190, cross_y=540)
GAP = 70          # V to P, in font units
WORD = (72, 860)  # Anybody wdth, wght for "Palestine"


def build():
    os.makedirs(os.path.join(ROOT, 'assets', 'brand'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'tools', 'out'), exist_ok=True)
    L, R, O = v_strokes(**V)
    font = instance(*WORD)
    word, adv = set_text(font, 'Palestine')
    vw = 1067
    total = vw + GAP + adv
    # the ascenders of l and t and the dot of the i rise above the cap line: the wordmark's box includes them
    asc = max(bounds_of(font, c)[3] for c in 'lti')
    top = round(asc - CAP)
    marks = {
        'v': {'film': poly(L), 'music': poly(R), 'over': poly(O), 'w': vw, 'h': CAP},
        'word': {'d': word, 'x': vw + GAP, 'w': round(total), 'h': CAP, 'top': top},
    }
    json.dump(marks, open(os.path.join(ROOT, 'tools', 'out', 'marks.json'), 'w', encoding='utf-8'))

    def v_svg(film, music, over, pad=0):
        return (f'<path fill="{film}" d="{marks["v"]["film"]}"/><path fill="{music}" d="{marks["v"]["music"]}"/>'
                f'<path fill="{over}" d="{marks["v"]["over"]}"/>')

    def write(name, body, w, h, pad=0, bg=None, top=0):
        rect = f'<rect x="{-pad}" y="{-pad - top}" width="{w + 2 * pad}" height="{h + top + 2 * pad}" fill="{bg}"/>' if bg else ''
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad - top} {w + 2 * pad} {h + top + 2 * pad}">'
               f'{rect}{body}</svg>\n')
        open(os.path.join(ROOT, 'assets', 'brand', name), 'w', encoding='utf-8').write(svg)

    day = (INK['film'], INK['music'], INK['over'])
    night = (INK['film_d'], INK['music_d'], INK['over_d'])
    write('v.svg', v_svg(*day), vw, CAP)
    write('v-night.svg', v_svg(*night), vw, CAP)
    wd = lambda key: f'<g fill="{key}">{glyph_path(word, vw + GAP)}</g>'
    write('wordmark.svg', v_svg(*day) + wd(INK['key']), round(total), CAP, top=top)
    write('wordmark-night.svg', v_svg(*night) + wd(INK['key_d']), round(total), CAP, top=top)
    write('wordmark-on-stock.svg', v_svg(*day) + wd(INK['key']), round(total), CAP, pad=300, bg=INK['stock'], top=top)
    write('wordmark-on-black.svg', v_svg(*night) + wd(INK['key_d']), round(total), CAP, pad=300, bg=INK['stock_d'], top=top)
    write('avatar.svg', v_svg(*day), vw, CAP, pad=420, bg=INK['stock'])
    write('avatar-night.svg', v_svg(*night), vw, CAP, pad=420, bg=INK['stock_d'])
    # favicon follows the browser's scheme: day inks on light tabs, night inks on dark tabs
    fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-160 -60 {vw + 320} {CAP + 120}">'
           f'<style>.f{{fill:{INK["film"]}}}.m{{fill:{INK["music"]}}}.o{{fill:{INK["over"]}}}'
           f'@media (prefers-color-scheme:dark){{.f{{fill:{INK["film_d"]}}}.m{{fill:{INK["music_d"]}}}.o{{fill:{INK["over_d"]}}}}}</style>'
           f'<path class="f" d="{marks["v"]["film"]}"/><path class="m" d="{marks["v"]["music"]}"/><path class="o" d="{marks["v"]["over"]}"/></svg>\n')
    open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8').write(fav)
    print('marks written; wordmark', round(total), 'x', CAP, 'units')


if __name__ == '__main__' and '--explore' not in sys.argv:
    build()
