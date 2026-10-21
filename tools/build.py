"""home.html from tools/edition.py, research/news.json (sources), tools/out/photos.json and tools/out/marks.json.

python -I tools/build.py      (run tools/brand.py and tools/photos.py first)
Never hand-edit home.html. Bump V on every CSS/JS/font change (browsers cache hard).
"""
import json, os, re, sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edition as E  # noqa: E402
from listings import EVENTS  # noqa: E402

V = 20
NEWS = {x['id']: x for x in json.load(open(os.path.join(ROOT, 'research', 'news.json'), encoding='utf-8'))}
PHOTOS = json.load(open(os.path.join(ROOT, 'tools', 'out', 'photos.json'), encoding='utf-8'))
MARKS = json.load(open(os.path.join(ROOT, 'tools', 'out', 'marks.json'), encoding='utf-8'))
CONTRACT = open(os.path.join(ROOT, 'tools', 'contract.txt'), encoding='utf-8').read().strip()
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()

# ---------- marks ----------
VB = {'film': '0 0 650 1350', 'music': '417 0 650 1350', 'both': '0 0 1067 1350'}


def vk(desk, state='on', label=None):
    paths = {'film': ['f'], 'music': ['m'], 'both': ['f', 'm', 'o']}[desk]
    d = {'f': MARKS['v']['film'], 'm': MARKS['v']['music'], 'o': MARKS['v']['over']}
    cls = {'on': '', 'due': ' due', 'gone': ' gone'}[state]
    aria = f' role="img" aria-label="{escape(label)}"' if label else ' aria-hidden="true"'
    return (f'<svg class="vk{cls}" viewBox="{VB[desk]}" preserveAspectRatio="xMidYMid meet"{aria}>'
            + ''.join(f'<path class="{p}" d="{d[p]}"/>' for p in paths) + '</svg>')


def wordmark(cls='mark', label='VPalestine, home'):
    v, w = MARKS['v'], MARKS['word']
    return (f'<svg viewBox="0 {-w["top"]} {w["w"]} {w["h"] + w["top"]}" role="img" aria-label="{escape(label)}">'
            f'<path class="f" d="{v["film"]}"/><path class="m" d="{v["music"]}"/><path class="o" d="{v["over"]}"/>'
            f'<g class="w"><path transform="translate({w["x"]} {w["h"]}) scale(1 -1)" d="{w["d"]}"/></g></svg>')


DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
        + ''.join(f'<pattern id="tint-{k}" width="110" height="110" patternUnits="userSpaceOnUse">'
                  f'<circle cx="27" cy="27" r="26" fill="var({c})"/><circle cx="82" cy="82" r="26" fill="var({c})"/></pattern>'
                  for k, c in (('f', '--film'), ('m', '--music'), ('o', '--over')))
        + '</defs></svg>')

# ---------- pieces ----------
DESK_NAME = {'film': 'Film', 'music': 'Music', 'both': 'Film and music'}
STATE_NAME = {'on': 'confirmed', 'due': 'expected', 'gone': 'over'}


LINKS = {
    'suleiman-athens': 'article.html', 'mc-abdul': 'artist.html', 'boston': 'festival.html', 'doha': 'work.html',
    'el-gouna': 'film.html#elgouna-2026-opens', 'lff': 'film.html#lff-2026-palestinian-titles', 'rome': 'film.html#rome-ff-yesterday-eye',
    'siege': 'film.html#chronicles-from-the-siege', 'dc': 'film.html#dc-pfaf-2026', 'unsung': 'film.html#pfi-durban-showcase',
    'jerusalem': 'music.html#jerusalem-festival-closes', 'saint-levant': 'music.html#saint-levant-tour-postponed',
    'rasha-nahas': 'music.html#rasha-nahas-manaqish', 'faraj': 'music.html#faraj-suleiman-solo', 'nai': 'music.html#nai-barghouti-hong-kong',
    'al-festival': 'music.html#al-festival-berlin-jubran-daboor',
}


def lines(item, tag='h2', cls='', fit=True, href=None):
    href = href or LINKS.get(item['id'], f'#{item["id"]}')
    spans = ''.join(f'<span class="ln">{l.rstrip(",")}</span>' for l in item['lines'])
    title = escape(item['title']).replace('&amp;', '&')
    # the visible lines are the poster; the full headline is what assistive tech reads
    return (f'<{tag} class="lines {cls}"{" data-fit" if fit else ""}>'
            f'<a class="stretch" href="{href}"><span class="vh">{title}</span><span aria-hidden="true">{spans}</span></a></{tag}>')


def plate(p, cls='', lazy=True, lpi=None):
    m = PHOTOS[p['slug']]
    fx, fy = p.get('focus', (0.5, 0.5))
    extra = f' data-zoom="{p["zoom"]}"' if p.get('zoom') else ''
    extra += f' data-lpi="{lpi}"' if lpi else ''
    extra += f' data-gamma="{p["gamma"]}"' if p.get('gamma') else ''
    return (f'<figure class="plate {cls}" data-fx="{fx}" data-fy="{fy}"{extra}>'
            f'<img src="assets/img/photo/{p["slug"]}.webp?v={V}" width="{m["w"]}" height="{m["h"]}" alt="{escape(p["alt"])}"'
            f'{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async"></figure>')


def credit(slug, override=None):
    m = PHOTOS[slug]
    who = override or f'{m["author"].replace("User:", "")} / Wikimedia Commons, {m["license"]}'
    return f'<span class="cr">Photo: <a href="{escape(m["page"])}">{escape(who)}</a></span>'


def caption(p, override=None):
    return f'<p class="cap">{p["caption"]} {credit(p["slug"], override)}</p>'


def sources(ids, cap=3, fold=False):
    seen, out, pool = set(), [], []
    for i in ids:
        for s in NEWS[i]['sources']:
            name = s['name'].split(' (')[0]
            if name in seen or s['url'] in seen or 'not reachable' in s['name']:
                continue
            seen.update((name, s['url']))
            pool.append((name, s))
    wiki = [x for x in pool if x[0].startswith('Wikipedia')]
    pool = [x for x in pool if not x[0].startswith('Wikipedia')] or wiki
    if cap:
        pool = pool[:cap]
    for name, s in pool:
            date = ''
            if s.get('date'):
                y, mo, d = s['date'].split('-')
                date = f' {int(d)} {MONTHS[int(mo) - 1]}' + ('' if y == '2026' else f' {y}')
            out.append(f'<a href="{escape(s["url"])}">{escape(name)}</a>{date}')
    if fold:
        return f'<details class="src"><summary>Sources for these dates ({len(out)})</summary><p>{", ".join(out)}</p></details>'
    return f'<p class="src">Sources: {", ".join(out)}</p>'


def band(rows):
    return '<dl class="band">' + ''.join(f'<div><dt>{escape(k)}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


def ink_cls(item, fmt=''):
    desk = {'film': 'ink-film', 'music': 'ink-music', 'both': 'ink-over'}[item['desk']]
    state = {'on': '', 'due': ' st-due', 'gone': ' st-gone'}[item['state']]
    return f'{desk}{state}'


# ---------- sections ----------
NAV = [('film.html', 'Film'), ('music.html', 'Music'), ('calendar.html', 'What’s on'), ('festival.html', 'Festivals'),
       ('search.html', 'Search'), ('about.html', 'About')]


def masthead(current=None):
    links = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a></li>' for h, t in NAV)
    return (f'<header class="mast"><a class="mark" href="./home.html">{wordmark()}</a>'
            f'<div class="mid"><p class="dateline"><time datetime="{E.DATE}">{E.DATELINE}</time></p>'
            f'<nav aria-label="Sections"><ul>{links}</ul></nav></div>'
            '<button class="stock" type="button" aria-pressed="false"><span class="lbl">Black stock</span>'
            '<span class="sw" aria-hidden="true"><i></i><i></i></span></button></header>')


def tonight():
    L, S = E.LEAD, E.SLEEVE
    one = (f'<article class="one ink ink-film p-film" id="{L["id"]}">'
           f'{plate(L["photo"], lazy=False, lpi=132)}'
           f'<div class="body p-key">{lines(L, "h1")}'
           f'<p class="deck">{L["deck"]}</p>{band([(k, escape(v)) for k, v in L["band"]])}'
           f'{caption(L["photo"])}{sources(L["src"])}</div></article>')
    sleeve = (f'<article class="sleeve ink ink-music p-music" id="{S["id"]}">'
              f'{plate(S["photo"], lazy=False, lpi=96)}'
              f'<div class="txt p-key">{lines(S, "h2")}<p class="hed">{escape(S["title"])}</p>'
              f'<p class="copy">{S["text"]}</p>{band([(k, escape(v)) for k, v in S["band"]])}'
              f'<p class="cap">{S["photo"]["caption"]} {credit(S["photo"]["slug"])}</p>{sources(S["src"])}</div></article>')
    return f'<section class="tonight" id="tonight" aria-label="Tonight and tomorrow">{one}{sleeve}</section>'


def thumb(ev):
    ph = ev.get('photo')
    if not ph or ph['slug'] not in PHOTOS:
        return ''
    ink = {'film': 'ink-film', 'music': 'ink-music', 'both': 'ink-over'}[ev['desk']]
    return plate(ph, f'{ink} th', lpi=26)


def week():
    from datetime import date
    days = {}
    for ev in EVENTS:
        if ev['start'] and '2026-10-15' <= ev['start'] <= '2026-10-18':
            days.setdefault(ev['start'], []).append(ev)
    cols = ''
    for iso in sorted(days):
        y, m, d = map(int, iso.split('-'))
        wd = 'Mon Tue Wed Thu Fri Sat Sun'.split()[date(y, m, d).weekday()]
        rows = ''
        for ev in days[iso]:
            th = thumb(ev)
            mark = th or vk(ev['desk'], ev['state'], DESK_NAME[ev['desk']] + ', ' + STATE_NAME[ev['state']])
            rows += (f'<li class="{ev["state"]}{" has-th" if th else ""}">{mark}'
                     f'<div><p class="w"><a href="{ev["link"]}">{ev["what"]}</a></p><p class="p">{escape(ev["venue"])}{" · expected" if ev["state"] == "due" else ""}</p></div>'
                     f'<p class="t">{escape(ev["city"])}{("<br>" + escape(ev["time"])) if ev["time"] else ""}</p></li>')
        cols += f'<div class="day"><h3><span>{wd}</span> {d}</h3><ol>{rows}</ol></div>'
    return (f'<section class="week" id="week" aria-labelledby="week-h"><div class="wk-head"><h2 id="week-h">This week</h2>'
            f'<p class="how">Local times, Thursday to Sunday. <span>{vk("film")} Film</span><span>{vk("music")} Music</span>'
            f'<span>{vk("film", "due")} Tint: expected</span> <a href="calendar.html">Every date ahead</a></p></div><div class="days">{cols}</div></section>')


def on_stock(item):
    """Window cards, lobby cards and small gig posters print key on stock; their photo keeps the screen's ink."""
    return item['state'] == 'on' and item['fmt'] in ('window', 'lobby', 'gig')


def sheet(item):
    fmt = item['fmt']
    cls = f'sheet {fmt} ink ' + ('ink-stock' if on_stock(item) else ink_cls(item))
    ph = item.get('photo')
    head = lines(item, 'h3')
    body = (f'<p class="hed">{escape(item["title"])}</p><p class="copy">{item["text"]}</p>'
            + (('<ol class="dates">' + ''.join(f'<li><b>{d}</b><span>{w}</span><span>{v}</span></li>' for d, w, v in item['list']) + '</ol>') if item.get('list') else '')
            + band([(k, escape(v)) for k, v in item['band']]))
    cap = caption(ph, item.get('credit')) if ph else ''
    src = sources(item['src'])
    if fmt == 'half':
        return (f'<article class="{cls}" id="{item["id"]}">{plate(ph, lpi=80)}'
                f'<div class="txt">{head}{body}{cap}{src}</div></article>')
    if fmt == 'strip':
        return f'<article class="{cls}" id="{item["id"]}"><div>{head}</div><div>{body}{src}</div></article>'
    pl = plate(ph, 'ink-film', lpi=90) if ph else ''
    return f'<article class="{cls}" id="{item["id"]}">{pl}{head}{body}{cap}{src}</article>'


def screens():
    return ('<section class="sec" id="screens" aria-labelledby="screens-h"><div class="head"><h2 id="screens-h">Screenings this week</h2>'
            '<p>Where Palestinian films are playing between now and Sunday, festival by festival. Solid ink is confirmed; '
            'a tint is still expected.</p></div>'
            '<div class="wall">' + ''.join(sheet(x) for x in E.CIRCUIT) + '</div></section>')


def doha():
    D = E.DOHA
    films = ''
    for f in D['films']:
        stops = ''.join(f'<li><b>{escape(c)}</b><small>{escape(n)}</small></li>' for c, n in f['road'])
        meta = ' · '.join(x for x in (f['by'], f['rt']) if x)
        films += (f'<li class="{f["state"]}"><p class="t"><b><em>{escape(f["title"])}</em></b><span>{escape(meta)}'
                  f'{" · listed by trade press" if f["state"] == "due" else ""}</span></p><ol class="road">{stops}</ol></li>')
    strip = ''.join(f'<figure>{plate(p, lpi=96)}<figcaption class="cap">{p["caption"]} {credit(p["slug"])}</figcaption></figure>' for p in D['photos'])
    return (f'<section class="sec" id="doha" aria-labelledby="doha-h"><div class="head"><h2 id="doha-h">The road to Doha</h2>'
            '<p>Each film’s festival run, stop by stop, the way a tour poster lists its dates.</p></div>'
            f'<article class="doha"><div class="strip">{strip}</div><div class="runs"><div class="top">{lines(D, "h3")}'
            f'<p class="copy">{D["text"]}</p></div><ol class="road-list">{films}</ol>'
            f'{band([(k, escape(v)) for k, v in D["band"]])}{sources(D["src"])}</div></article></section>')


def bridge():
    B = E.BRIDGE
    return (f'<section class="bridge" id="{B["id"]}" aria-label="Film and music"><i class="b-film" aria-hidden="true"></i><i class="b-music" aria-hidden="true"></i>'
            f'<div class="b-title">{vk("both", "on", "Film and music")}{lines(B, "h2")}</div>'
            f'<div class="b-copy">{plate(B["photo"], "b-plate", lpi=70) if B.get("photo") else ""}<p class="copy">{B["text"]}</p>'
            f'{band([(k, escape(v)) for k, v in B["band"]])}{caption(B["photo"]) if B.get("photo") else ""}{sources(B["src"])}</div></section>')


def record():
    out = []
    for i, x in enumerate(E.RECORD):
        cls = f'sheet ink {ink_cls(x)}'
        ph = x.get('photo')
        body = (f'<p class="hed">{escape(x["title"])}</p><p class="copy">{x["text"]}</p>'
                + band([(k, escape(v)) for k, v in x['band']]))
        cap = caption(ph, x.get('credit')) if ph else ''
        if x['fmt'] == 'gig' and i == 0:
            out.append(f'<article class="{cls} gig big" id="{x["id"]}">{plate(ph, lpi=150)}<div class="txt">{lines(x, "h3")}{body}{cap}{sources(x["src"])}</div></article>')
        elif x['fmt'] == 'sleeve':
            out.append(f'<article class="{cls} sleeve-s" id="{x["id"]}">{plate(ph, lpi=64)}<div class="txt">{lines(x, "h3")}{body}{cap}{sources(x["src"])}</div></article>')
        else:
            if on_stock(x):
                cls = 'sheet ink ink-stock'
            pl = plate(ph, 'ink-music', lpi=80) if ph else ''
            out.append(f'<article class="{cls} gig small" id="{x["id"]}">{pl}{lines(x, "h3")}{body}{cap}{sources(x["src"])}</article>')
    return ('<section class="sec" id="record" aria-labelledby="record-h"><div class="head"><h2 id="record-h">Records and stages</h2>'
            '<p>Releases, tours and concerts. An outlined sheet is a date that has passed or moved.</p></div>'
            '<div class="wall">' + ''.join(out) + '</div></section>')


def coming():
    import pages as P
    evs = [e for e in P.upcoming() if e['home'] and (not e['start'] or e['start'] > '2026-10-18')]
    return ('<section class="sec" id="coming" aria-labelledby="coming-h"><div class="head"><h2 id="coming-h">Coming attractions</h2>'
            '<p>The dates ahead, set like a tour poster. A tinted date is expected and may change; times are local to each venue. '
            '<a href="calendar.html">Every date, with filters</a>.</p></div>'
            f'{P.tour(evs)}<div class="pad">{sources(sorted({e["src"] for e in evs}), cap=0, fold=True)}</div></section>')


def reissue():
    R = E.REISSUE
    small = ''.join(f'<figure>{plate(p, "key", lpi=60)}<figcaption class="cap">{p["caption"]} {credit(p["slug"])}</figcaption></figure>' for p in R['small'])
    return (f'<section class="sec" id="reissue" aria-labelledby="reissue-h"><div class="head"><h2 id="reissue-h">Reissue</h2>'
            '<p>The archive is printed in the key plate alone: one ink, the way a reissued poster comes back.</p></div>'
            f'<article class="reissue"><div class="big">{plate(R["photo"], "key", lpi=150)}{caption(R["photo"])}</div>'
            f'<div class="txt"><h3>{escape(R["title"])}</h3>' + ''.join(f'<p class="copy">{p}</p>' for p in R['text'])
            + f'{band([(k, escape(v)) for k, v in R["band"]])}<div class="pair">{small}</div>{sources(R["src"])}</div></article></section>')


def signup():
    return ('<section class="signup" aria-labelledby="bill-sign"><div><h2 id="bill-sign">The Thursday bill</h2>'
            '<p>One email a week: what premiered, what came out, and what is on near you.</p></div>'
            '<form action="#" method="post" novalidate><label for="em">Email address</label>'
            '<input id="em" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>'
            '<button type="submit">Subscribe</button><p class="note" role="status">[NEWSLETTER BACKEND] Placeholder: no list exists yet.</p></form></section>')


HOME_PHOTOS = [E.LEAD['photo'], E.SLEEVE['photo']] + [x['photo'] for x in E.CIRCUIT if x.get('photo')] + E.DOHA['photos'] \
    + [x['photo'] for x in E.RECORD if x.get('photo')] + [E.REISSUE['photo']] + E.REISSUE['small'] + ([E.BRIDGE['photo']] if E.BRIDGE.get('photo') else []) \
    + [e['photo'] for e in EVENTS if e.get('photo') and e['photo']['slug'] in PHOTOS]


def imprint(photos=None):
    photos = [p for p in (HOME_PHOTOS if photos is None else photos) if p['slug'] in PHOTOS]
    used, label = [], {}
    for p in photos:
        if p['slug'] not in used:
            used.append(p['slug'])
        label.setdefault(p['slug'], re.split(r'[,.] ', re.sub(r'<[^>]+>', '', p['caption']))[0])
    over = {'rasha-nahas': 'Jacob Crawfurd / WOMEX', 'faraj': 'Jacob Crawfurd / WOMEX'}
    cred = ''.join(f'<p>{escape(label[s])} — <a href="{escape(PHOTOS[s]["page"])}">'
                   f'{escape(over.get(s, PHOTOS[s]["author"].replace("User:", "")))}</a>, {escape(PHOTOS[s]["license"])}</p>' for s in used)
    nav = [('About', 'about.html'), ('Send us a screening', 'about.html#send'), ('Corrections', 'about.html#corrections'),
           ('Contact', 'about.html#contact'), ('Identity book', 'index.html'), ('[SOCIAL HANDLES]', '#')]
    return (f'<footer class="imprint"><a class="foot-mark mark" href="#top">{wordmark(label="VPalestine, back to top")}</a>'
            + '<div class="furniture" aria-hidden="true"><svg class="reg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="11"/><path d="M20 0V40M0 20H40"/></svg>'
            '<span class="bar"><i class="c-film"></i><i class="c-film t"></i><i class="c-music"></i><i class="c-music t"></i><i class="c-over"></i><i class="c-key"></i><i class="c-key t"></i></span>'
            '<svg class="reg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="11"/><path d="M20 0V40M0 20H40"/></svg></div>'
            f'<p class="legend"><span>{vk("film")} Film screen</span><span>{vk("music")} Music screen</span>'
            f'<span>{vk("both")} Overprint: both</span><span>{vk("film", "due")} Tint: expected</span><span>{vk("film", "gone")} Outline: passed or moved</span></p>'
            '<div class="cols"><div><p class="line">Palestinian film and music, followed from premiere to audience. Printed in two screens and a key, '
            'on white stock by day and black stock by night.</p>'
            '<nav aria-label="Footer"><ul>' + ''.join(f'<li><a href="{h}">{t}</a></li>' for t, h in nav) + '</ul></nav></div>'
            + (f'<div class="credits"><h3>Photographs, all via Wikimedia Commons; none is a film still</h3>{cred}</div>' if used else '<div></div>') + '</div>'
            '<p class="legal">Design prototype · edition of Thursday 15 October 2026, rebuilt from public sources checked that day · '
            'name and wordmark: VPalestine · photographs printed as halftones from the credited originals · © 2026 VPalestine</p></footer>')


HOME_TITLE = 'VPalestine — Palestinian film and music · Thursday 15 October 2026'
HOME_DESC = "Palestinian film and music, followed from premiere to audience: tonight Elia Suleiman opens Athens, tomorrow MC Abdul's first album."

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#FAFAF6">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VPalestine">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://taktek-dev.github.io/vpalestine-prototype/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg?v={V}" type="image/svg+xml">
<link rel="preload" href="assets/fonts/anybody-var.woff2?v=1" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/besley-var.woff2?v=1" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/vp.css?v={V}">{CSS}
<script>(function(){{var d=document.documentElement;try{{if(localStorage.getItem('vp-stock')==='black')d.dataset.stock='black'}}catch(e){{}}
var seen=false;try{{seen=sessionStorage.getItem('vp-pulled')==='1'}}catch(e){{}}
if((location.search.indexOf('pull')>-1||!seen)&&!matchMedia('(prefers-reduced-motion: reduce)').matches&&document.visibilityState!=='hidden'){{d.classList.add('pulling');setTimeout(function(){{d.classList.remove('pulling')}},6000)}}}})();</script>
</head>
"""


def head(title=HOME_TITLE, desc=HOME_DESC, css=()):
    extra = ''.join(f'\n<link rel="stylesheet" href="assets/css/{c}?v={V}">' for c in css)
    return HEAD.format(V=V, TITLE=escape(title), DESC=escape(desc), CSS=extra)


def page(name, title, desc, main, current=None, photos=(), css=('pages.css',), js=(), skip='Skip to the page'):
    """Every inner page: same press, same chrome; the footer credits only the photos this page printed."""
    html = (head(title, desc, css) + f'<body id="top">\n<!--\n{CONTRACT}\n-->\n'
            + f'<a class="skip" href="#main">{skip}</a>' + DEFS
            + '<div class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="squeegee" aria-hidden="true"></div>'
            + masthead(current) + f'<main id="main">{main}</main>' + imprint(list(photos))
            + f'<script src="assets/js/vp.js?v={V}" defer></script>'
            + ''.join(f'<script src="assets/js/{j}?v={V}" defer></script>' for j in js) + '\n</body>\n</html>\n')
    open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(html)
    print(name, len(html) // 1024, 'KB')


def build():
    html = (head() + f'<body id="top">\n<!--\n{CONTRACT}\n-->\n'
            + '<a class="skip" href="#main">Skip to the edition</a>' + DEFS
            + '<div class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="squeegee" aria-hidden="true"></div>'
            + masthead() + '<main id="main">' + tonight() + week() + screens() + doha() + bridge() + record() + coming() + reissue()
            + signup() + '</main>' + imprint()
            + f'<script src="assets/js/vp.js?v={V}" defer></script>\n</body>\n</html>\n')
    open(os.path.join(ROOT, 'home.html'), 'w', encoding='utf-8').write(html)
    print('home.html', len(html) // 1024, 'KB')


if __name__ == '__main__':
    build()
