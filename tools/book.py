"""index.html: the VPalestine identity book, printed with the same press as the homepage.

python -I tools/book.py     (after tools/brand.py, tools/photos.py, tools/build.py)
Never hand-edit index.html.
"""
import json, os, sys, zipfile
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402
from inks import INK, multiply  # noqa: E402

V = B.V
M = B.MARKS


def v_svg(cls='', label=None, extra=''):
    v = M['v']
    aria = f' role="img" aria-label="{escape(label)}"' if label else ' aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="0 0 {v["w"]} {v["h"]}"{aria}>{extra}'
            f'<path class="f" d="{v["film"]}"/><path class="m" d="{v["music"]}"/><path class="o" d="{v["over"]}"/></svg>')


def construction():
    """The V with its measurements, in font units (Anybody, 2000 upm, cap height 1350)."""
    v = M['v']
    pad = 240
    ln = 'stroke="var(--key)" stroke-width="5" fill="none"'
    tx = 'fill="var(--key)" font-family="Anybody" font-weight="700" font-stretch="118%" font-size="54" letter-spacing="2"'
    return (f'<svg class="build" viewBox="{-pad} {-pad} {v["w"] + 2 * pad + 420} {v["h"] + 2 * pad}" role="img" '
            'aria-label="Construction of the V: two straight strokes, each 360 units wide at the cap line; their inner edges cross at two fifths of the cap height and the overprint fills the triangle below; the foot is 380 units wide.">'
            f'<path class="f" d="{v["film"]}"/><path class="m" d="{v["music"]}"/><path class="o" d="{v["over"]}"/>'
            # cap line and baseline
            f'<path {ln} stroke-dasharray="14 12" d="M-200 0H{v["w"] + 200}M-200 {v["h"]}H{v["w"] + 200}"/>'
            # stroke width at the cap line
            f'<path {ln} d="M0 -90V-40M360 -90V-40M0 -65H360"/><text {tx} x="180" y="-115" text-anchor="middle">360</text>'
            f'<path {ln} d="M707 -90V-40M1067 -90V-40M707 -65H1067"/><text {tx} x="887" y="-115" text-anchor="middle">360</text>'
            # crossing height
            f'<path {ln} d="M{v["w"] + 90} {v["h"]}V810M{v["w"] + 60} 810H{v["w"] + 120}M{v["w"] + 60} {v["h"]}H{v["w"] + 120}"/>'
            f'<path {ln} stroke-dasharray="8 10" d="M533 810H{v["w"] + 60}"/>'
            f'<text {tx} x="{v["w"] + 150}" y="1095">540 · two fifths</text><text {tx} x="{v["w"] + 150}" y="1160">of the cap height</text>'
            # foot
            f'<path {ln} d="M343 {v["h"] + 40}V{v["h"] + 90}M723 {v["h"] + 40}V{v["h"] + 90}M343 {v["h"] + 65}H723"/>'
            f'<text {tx} x="533" y="{v["h"] + 150}" text-anchor="middle">foot 380</text>'
            f'<text {tx} x="{v["w"] + 150}" y="40">cap height 1350</text><text {tx} x="{v["w"] + 150}" y="{v["h"] - 10}">baseline</text>'
            '</svg>')


def contrast(a, b):
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def pairs_table():
    """Contrast of the text each ink carries, computed from the inks (WCAG 2.2 ratios)."""
    over = multiply(INK['film'], INK['music'])
    dark, white = INK['key'], INK['stock']
    rows = [('Film', (INK['film'], dark, 'key'), (INK['film_d'], dark, 'dark key')),
            ('Music', (INK['music'], white, 'white'), (INK['music_d'], dark, 'dark key')),
            ('Overprint', (over, white, 'white'), (INK['over_d'], dark, 'dark key')),
            ('Stock', (INK['stock'], dark, 'key'), (INK['stock_d'], INK['key_d'], 'underbase white'))]
    body = ''.join(f'<tr><th scope="row">{n}</th>' + ''.join(f'<td>{t} text, {contrast(bg, fg):.1f} : 1</td>' for bg, fg, t in (d, nt)) + '</tr>'
                   for n, d, nt in rows)
    return ('<table class="pairs"><caption>Text on each ink, contrast computed from the ink values</caption><thead><tr><th scope="col">Ink</th>'
            '<th scope="col">White stock</th><th scope="col">Black stock</th></tr></thead><tbody>' + body + '</tbody></table>')


def swatch(name, var, value, night, role, on):
    return (f'<figure class="sw ink" style="--ink:var({var});--on:{on}"><div class="chip"><b>{name}</b><span>{role}</span></div>'
            f'<figcaption><span>White stock <code>{value}</code></span><span>Black stock <code>{night}</code></span></figcaption></figure>')


def chapter(cid, title, lede, body, cls=''):
    return (f'<section class="ch {cls}" id="{cid}" aria-labelledby="{cid}-h"><header class="ch-head">'
            f'<h2 id="{cid}-h" class="lines" data-fit><span class="ln">{title}</span></h2><p>{lede}</p></header>{body}</section>')


def book():
    chapters = []
    over = multiply(INK['film'], INK['music'])

    chapters.append(chapter('idea', 'Two screens and a key',
        'Palestinian film weeks and concerts were announced on silkscreened posters: a few flat inks pulled by hand onto white stock. '
        'VPalestine prints its pages the same way. Film is pulled in one ink, music in the other, and wherever the two land on each other '
        'they make a third colour that belongs to both. Type and photographs go down last, in the key plate.',
        '<div class="idea"><div class="press" id="press" aria-label="Drag the music screen over the film screen to see the overprint">'
        '<div class="scr film"><span>Film</span></div><div class="scr music" tabindex="0" role="slider" aria-label="Music screen position" '
        'aria-valuemin="0" aria-valuemax="100" aria-valuenow="55"><span>Music</span></div></div>'
        '<div class="idea-notes"><p class="copy">Drag the music screen. On white stock the inks are transparent, so fuchsia over yellow '
        f'prints red (<code>{over}</code>) by itself; nobody picks the red, the press makes it. That is the whole identity: two subjects, '
        'one page, and a colour that only exists where they meet.</p>'
        '<ul class="rules"><li><b>The stock is the light.</b> White on the page is unprinted paper, never a card or a panel.</li>'
        '<li><b>One screen per ink.</b> An ink’s fields, type and halftone register together.</li>'
        '<li><b>Ink fields bleed.</b> They run to the edge of the sheet or into another ink; nothing floats with rounded corners.</li></ul></div></div>'))

    chapters.append(chapter('mark', 'The V is two strokes',
        'The mark is the V of VPalestine, taken from Anybody’s own V and split into the two strokes a printer would cut as two screens. '
        'The film stroke always leans in from the left, the music stroke from the right, and the overprint is the keystone where they cross.',
        '<div class="mark-grid"><div class="mk-build">' + construction() + '</div>'
        '<div class="mk-uses"><figure class="on-white">' + v_svg('vm', 'The V on white stock') + '<figcaption>White stock</figcaption></figure>'
        '<figure class="on-black">' + v_svg('vm', 'The V on black stock') + '<figcaption>Black stock: brighter, opaque inks</figcaption></figure>'
        '<figure class="on-key">' + v_svg('vm key-only', 'The V in the key plate alone') + '<figcaption>One ink only: key</figcaption></figure>'
        '<figure class="sizes">' + ''.join(f'<span style="--s:{s}px">{v_svg("vm")}<i>{s}</i></span>' for s in (16, 24, 40, 64)) +
        '<figcaption>Smallest: 16 px on screen, 6 mm in print</figcaption></figure></div></div>'
        '<ul class="donts" aria-label="What the mark never does">'
        + ''.join(f'<li><span class="dn {c}">{v_svg("vm")}</span><p>{t}</p></li>' for c, t in (
            ('swap', 'Never swap the inks: film is always the left stroke.'),
            ('tilt', 'Never rotate or slant it.'),
            ('flat', 'Never print it in one hue other than the key.'),
            ('gap', 'Never pull the strokes apart; the overprint is the point.')))
        + '</ul>'))

    chapters.append(chapter('wordmark', 'VPalestine, in its own type',
        'Palestine is Anybody at width 72 and weight 860, set at the V’s cap height with 70 units between them. The wordmark is drawn as outlines, '
        'so it never depends on the font loading. Clear space on every side is one V stroke.',
        '<div class="wm-grid"><figure class="wm white"><span class="clear">' + B.wordmark('wm', 'VPalestine wordmark on white stock') + '</span><figcaption>Primary, white stock. The dashed box is the clear space: one stroke.</figcaption></figure>'
        '<figure class="wm black">' + B.wordmark('wm', 'VPalestine wordmark on black stock') + '<figcaption>Black stock</figcaption></figure>'
        '<figure class="wm yellow ink ink-film">' + B.wordmark('wm', 'VPalestine wordmark printed on the film ink') + '<figcaption>On the film ink the film stroke would vanish, so it prints in key; the music stroke still overprints red.</figcaption></figure>'
        '<figure class="wm keyonly">' + B.wordmark('wm key-only', 'VPalestine wordmark in key only') + '<figcaption>One-colour jobs: everything in key.</figcaption></figure></div>'))

    sw = ''.join([
        swatch('Film', '--film', INK['film'], INK['film_d'], 'Projector yellow. Everything about films.', 'var(--on-film)'),
        swatch('Music', '--music', INK['music'], INK['music_d'], 'Fuchsia. Records, concerts, tours.', 'var(--on-music)'),
        swatch('Overprint', '--over', over, INK['over_d'], 'Film × music. Only where both meet.', 'var(--on-over)'),
        swatch('Key', '--key', INK['key'], INK['key_d'], 'Type, rules and the halftone dots.', 'var(--stock)'),
    ])
    chapters.append(chapter('inks', 'Four inks, two stocks',
        'The palette is a print run, not a set of brand colours. Yellow and fuchsia are the two screens, red is what they make together, and the key '
        'carries the words. By day the page is white stock; by night it is black stock, where the inks are printed opaque over a white underbase so they stay as bright.',
        f'<div class="swatches">{sw}</div>'
        + pairs_table()
        + '<p class="copy note">Inks are never text colours: type is always key, or the stock knocked out of an ink. Inks own whole sheets; they are not accents.</p>'))

    chapters.append(chapter('type', 'Set to the measure',
        'Poster type was chosen to fill the line. VPalestine does it with Anybody’s width axis: every title line is set, one by one, to the width of its sheet, '
        'from width 58 for long lines to 150 for short ones, so a sheet’s lines are equal in length and different in width. Besley, a Clarendon, carries the reading.',
        '<div class="type-demo"><label class="label" for="measure">Sheet width <output id="measure-out">100%</output></label>'
        '<input id="measure" type="range" min="34" max="100" value="100">'
        '<div class="measure-box ink ink-film" id="measure-box"><p class="lines" data-fit><span class="ln">Four films,</span><span class="ln">one</span><span class="ln">competition</span></p></div></div>'
        '<div class="specimens"><div class="spec"><p class="label">Anybody · titles, dates, bands, navigation</p>'
        '<p class="a1">Elia Suleiman</p><p class="a2">Day by Day, Shway Shway</p><p class="a3">THU 15 · 20:00 · TRIANON, ATHENS</p>'
        '<p class="axis">' + ''.join(f'<span style="font-stretch:{w}%">V</span>' for w in (58, 76, 94, 112, 130, 150)) + '<i>width 58 → 150</i></p></div>'
        '<div class="spec"><p class="label">Besley · decks, story text, captions</p>'
        '<p class="b1">Hosam Abu Dan’s first fiction feature was filmed inside the Strip with a local cast and crew.</p>'
        '<p class="b2"><em>It Must Be Heaven</em> (2019) opens the Athens Palestine Film Festival at the Trianon at 20:00.</p>'
        '<p class="b3">Kamel El Basha, who stars in <em>Conversation With the Sea</em>, 23 October 2021.</p></div></div>'
        '<ul class="rules"><li><b>Titles</b> Anybody 850–900, all caps, set to the measure. Headlines that repeat a title in full sentence case use Anybody 800 at width 94.</li>'
        '<li><b>Bands</b> The billing block: labels in Anybody 650 at width 120, values in Anybody 750, tabular figures.</li>'
        '<li><b>Reading</b> Besley 400 at 17–21 px, 1.45–1.55 leading, 38 em measure. Work titles in italics in running text; poster lines stay upright.</li></ul>'))

    pl = B.plate({'slug': 'el-basha', 'focus': (0.3, 0.42), 'zoom': 1.3, 'alt': 'Kamel El Basha seated before a lit dressing-room mirror'}, 'ink-film demo-plate', lpi=110)
    pl2 = B.plate({'slug': 'alhambra-jaffa', 'focus': (0.5, 0.45), 'alt': 'The Alhambra cinema in Jaffa, 1937'}, 'key demo-key', lpi=110)
    chapters.append(chapter('halftone', 'Every photograph is a screen',
        'Photographs are printed, not placed. Each one is screened at 45 degrees into round dots sized from the picture, over the ink of the sheet it sits on; '
        'shadows stop short of solid so the ink always shows between the dots. Archive pictures come back in the key plate alone, like a reissued poster. '
        'The screen is drawn in the browser at the reader’s resolution, so it stays sharp at any size.',
        f'<div class="ht"><div class="ht-plates">{pl}{pl2}</div><div class="ht-ctl"><label class="label" for="ruling">Screen ruling <output id="ruling-out">110</output> cells across</label>'
        '<input id="ruling" type="range" min="40" max="190" value="110"><p class="copy">Coarse screens for big sheets, fine screens for faces at small sizes. '
        'Without JavaScript the same grayscale plate is multiplied over its ink: a duotone, still in the world.</p>'
        '<ul class="rules"><li><b>Never a film still or a poster.</b> Only photographs we can credit; the caption says what, where and when.</li>'
        '<li><b>Never colour.</b> Colour comes from the ink, not the photograph.</li><li><b>Crop to the person.</b> Every plate carries a focal point.</li></ul>'
        f'<p class="cap">{escape("Kamel El Basha, 23 October 2021 · The Alhambra, Jaffa, 1937.")} {B.credit("el-basha")} · {B.credit("alhambra-jaffa")}</p></div></div>'))

    fm = [('one', 'One-sheet', 'The lead. Solid ink, bleeds to the edge, the biggest halftone.'),
          ('sleeve', 'Sleeve', 'A record. Square plate, music ink, overprints whatever it lands on.'),
          ('half', 'Half-sheet', 'A festival with a programme. Solid ink, dates listed.'),
          ('window', 'Window card', 'A single screening or opening. Key on stock, photo on its ink.'),
          ('lobby', 'Lobby card', 'A short notice. Key on stock, no photo needed.'),
          ('bill', 'Handbill', 'Listings by day: the week, the dates ahead.')]
    chapters.append(chapter('formats', 'Rank is the size of the sheet',
        'Hierarchy comes from the format a story is printed on, the way cinema posters come in sizes, not from type size alone.',
        '<ul class="formats">' + ''.join(f'<li class="fm fm-{c}"><div class="mini" aria-hidden="true"><i></i><b></b><s></s></div><h3>{t}</h3><p>{d}</p></li>' for c, t, d in fm) + '</ul>'))

    chapters.append(chapter('states', 'Solid, tint, outline',
        'State is ink density, never a new colour. A confirmed date prints solid. Something expected — a release without a date, a result still to come — prints as a halftone tint '
        'of its ink until it is confirmed. A date that has passed or moved keeps only its outline.',
        '<ul class="states">'
        f'<li class="ink ink-film"><span class="big">{B.vk("film")}</span><b>Solid</b><p>Confirmed. <em>It Must Be Heaven</em>, Thu 15 Oct, 20:00.</p></li>'
        f'<li class="ink ink-film st-due"><span class="big">{B.vk("film", "due")}</span><b>Tint</b><p>Expected. London names its documentary winner on Sunday.</p></li>'
        f'<li class="ink ink-music st-gone"><span class="big">{B.vk("music", "gone")}</span><b>Outline</b><p>Passed or moved. Saint Levant’s Los Angeles dates, now spring 2027.</p></li>'
        '</ul><p class="copy note">The V strokes are the legend: the left stroke marks film, the right stroke music, the whole V both.</p>'))

    chapters.append(chapter('motion', 'How the press moves',
        'Motion is what a print shop does, done once. The first page of a visit is pulled screen by screen; after that the page stays still and only answers the reader.',
        '<div class="motion"><div class="pull-demo" id="pull-demo" aria-hidden="true"><i class="pm"></i><div class="d-film"></div><div class="d-music"></div>'
        '<div class="d-key">' + B.wordmark('dm', 'VPalestine') + '</div><span class="d-sq"></span></div>'
        '<div><button class="btn" type="button" id="replay">Pull it again</button> <a class="btn ghost" href="home.html?pull">See it on the homepage</a>'
        '<table class="pairs motion-t"><caption>The pull, in print order</caption><thead><tr><th scope="col">Step</th><th scope="col">What happens</th><th scope="col">Timing</th></tr></thead><tbody>'
        '<tr><th scope="row">Crop marks</th><td>The sheet is laid on the bed</td><td>0–180 ms</td></tr>'
        '<tr><th scope="row">Film screen</th><td>Yellow pulled left to right behind a squeegee line</td><td>180–800 ms, <code>cubic-bezier(.62,0,.18,1)</code></td></tr>'
        '<tr><th scope="row">Music screen</th><td>Fuchsia pulled top to bottom; the red appears where it lands on yellow</td><td>720–1220 ms</td></tr>'
        '<tr><th scope="row">Key plate</th><td>Type lands 5 px out of register and settles; halftone dots grow</td><td>1180–1900 ms, <code>cubic-bezier(.22,1.18,.36,1)</code></td></tr>'
        '<tr><th scope="row">Hover</th><td>A sheet’s key plate jogs out of register and back</td><td>420 ms</td></tr>'
        '<tr><th scope="row">Stock</th><td>Changing white and black stock pulls the new paper across</td><td>700 ms</td></tr></tbody></table>'
        '<p class="copy note">Once per session, skipped by any key, click or scroll, and never shown with reduced motion or in a background tab. Content is printed without JavaScript.</p></div></div>'))

    chapters.append(chapter('voice', 'How VPalestine writes',
        'Facts first, the work first, every date with its place and its source. VPalestine follows films and records; it does not decorate them with war imagery or pity.',
        '<ul class="voice">'
        '<li><b>Name the work, then the event.</b><p class="do">Elia Suleiman: all four films, from tonight in Athens</p><p class="dont">Palestinian cinema shines in Greece</p></li>'
        '<li><b>Expected stays expected.</b><p class="do">Her third album has no date yet.</p><p class="dont">Rasha Nahas’s new album is out this month</p></li>'
        '<li><b>Local time, with the place.</b><p class="do">Thu 15 Oct, 20:00 Athens time, Trianon</p><p class="dont">Tonight at 8</p></li>'
        '<li><b>Credit what you show.</b><p class="do">Gaza seaport, 7 October 2017. Not a still from Thirteen in Gaza.</p><p class="dont">A scene from Thirteen in Gaza</p></li>'
        '</ul>'))

    files = [('wordmark.svg', 'Wordmark, white stock'), ('wordmark-night.svg', 'Wordmark, black stock'), ('wordmark-on-stock.svg', 'Wordmark on a white sheet'),
             ('wordmark-on-black.svg', 'Wordmark on a black sheet'), ('v.svg', 'The V, white stock'), ('v-night.svg', 'The V, black stock'),
             ('avatar.svg', 'Avatar, white'), ('avatar-night.svg', 'Avatar, black')]
    chapters.append(chapter('files', 'Files',
        'Every mark is an SVG drawn from the font outlines. The kit holds the marks, the two typefaces with their licences, and the ink values as tokens.',
        '<div class="files"><a class="btn" href="assets/brand/vpalestine-identity.zip" download>Download the kit (zip)</a><ul>'
        + ''.join(f'<li><a href="assets/brand/{f}" download>{t}</a> <span>SVG</span></li>' for f, t in files) +
        '</ul><p class="copy note">Typefaces: Anybody by Etcetera Type Co and Besley by Owen Earl (Indestructible Type), both under the SIL Open Font License.</p></div>'))

    contents = ''.join(f'<li><a href="#{c}">{t}</a></li>' for c, t in (
        ('idea', 'Two screens and a key'), ('mark', 'The mark'), ('wordmark', 'Wordmark'), ('inks', 'Inks'), ('type', 'Type'),
        ('halftone', 'Halftone'), ('formats', 'Formats'), ('states', 'States'), ('motion', 'Motion'), ('voice', 'Voice'), ('files', 'Files')))
    cover = ('<section class="cover" id="cover" aria-labelledby="cover-h">'
             f'<div class="cv-mark">{B.wordmark("wm", "VPalestine")}</div>'
             '<div class="cv-sheets"><div class="cv-film ink ink-film p-film"><h1 id="cover-h" class="lines p-key" data-fit><span class="ln">Overprint</span></h1>'
             '<p class="copy p-key">The identity of VPalestine: Palestinian film and music, printed in two screens and a key.</p>'
             '<div class="furniture" aria-hidden="true"><svg class="reg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="11"/><path d="M20 0V40M0 20H40"/></svg>'
             '<span class="bar"><i class="c-film"></i><i class="c-film t"></i><i class="c-music"></i><i class="c-music t"></i><i class="c-over"></i><i class="c-key"></i><i class="c-key t"></i></span></div></div>'
             f'<nav class="cv-music p-music" aria-label="Contents"><h2 class="label">Contents</h2><ol>{contents}</ol>'
             '<a class="btn on-music" href="home.html">See the homepage</a></nav></div></section>')

    mast = ('<header class="mast"><a class="mark" href="./">' + B.wordmark() + '</a><div class="mid"><p class="dateline">Identity book · October 2026</p>'
            '<nav aria-label="Book"><ul><li><a href="#mark">Mark</a></li><li><a href="#inks">Inks</a></li><li><a href="#type">Type</a></li>'
            '<li><a href="#halftone">Halftone</a></li><li><a href="#motion">Motion</a></li><li><a href="home.html">Homepage</a></li></ul></nav></div>'
            '<button class="stock" type="button" aria-pressed="false"><span class="lbl">Black stock</span><span class="sw" aria-hidden="true"><i></i><i></i></span></button></header>')

    head = B.HEAD.format(V=V).replace(
        '<title>VPalestine — Palestinian film and music · Thursday 15 October 2026</title>', '<title>VPalestine — Identity book</title>').replace(
        '<meta name="description" content="Palestinian film and music, followed from premiere to audience: tonight Elia Suleiman opens Athens, tomorrow MC Abdul\'s first album.">',
        '<meta name="description" content="The VPalestine identity: two silkscreen inks for film and music, the overprint where they meet, type set to the measure, photographs as halftones.">').replace(
        f'<link rel="stylesheet" href="assets/css/vp.css?v={V}">', f'<link rel="stylesheet" href="assets/css/vp.css?v={V}">\n<link rel="stylesheet" href="assets/css/book.css?v={V}">')
    html = (head + '<body id="top">\n<!--\n' + B.CONTRACT + '\n-->\n<a class="skip" href="#main">Skip to the book</a>' + B.DEFS
            + '<div class="marks" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="squeegee" aria-hidden="true"></div>'
            + mast + '<main id="main" class="book">' + cover + ''.join(chapters) + '</main>'
            + '<footer class="imprint"><p class="legal">VPalestine identity book · design prototype by TakTek, October 2026 · photographs via Wikimedia Commons, credited where shown · '
            '<a href="home.html">Homepage</a> · <a href="assets/img/photo/CREDITS.md">All photo credits</a></p></footer>'
            + f'<script src="assets/js/vp.js?v={V}" defer></script><script src="assets/js/book.js?v={V}" defer></script>\n</body>\n</html>\n')
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
    print('index.html', len(html) // 1024, 'KB')


def kit():
    path = os.path.join(ROOT, 'assets', 'brand', 'vpalestine-identity.zip')
    tokens = {'stock': {'white': INK['stock'], 'black': INK['stock_d']},
              'film': {'white': INK['film'], 'black': INK['film_d']},
              'music': {'white': INK['music'], 'black': INK['music_d']},
              'overprint': {'white': INK['over'], 'black': INK['over_d'], 'note': 'film x music, multiplied on white stock'},
              'key': {'white': INK['key'], 'black': INK['key_d']},
              'type': {'titles': 'Anybody 850-900, width set to the measure (58-150)', 'reading': 'Besley 400'}}
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(os.path.join(ROOT, 'assets', 'brand'))):
            if f.endswith('.svg'):
                z.write(os.path.join(ROOT, 'assets', 'brand', f), 'marks/' + f)
        for f in sorted(os.listdir(os.path.join(ROOT, 'assets', 'fonts'))):
            z.write(os.path.join(ROOT, 'assets', 'fonts', f), 'fonts/' + f)
        z.writestr('inks.json', json.dumps(tokens, indent=2))
        z.writestr('README.txt', 'VPalestine identity kit\n\nmarks/  SVG wordmarks, the V and avatars for white and black stock\n'
                   'fonts/  Anybody and Besley (SIL Open Font License), web subsets\ninks.json  the four inks on both stocks\n\n'
                   'The identity book: index.html of the prototype.\n')
    print('kit', os.path.getsize(path) // 1024, 'KB')


if __name__ == '__main__':
    book()
    kit()
