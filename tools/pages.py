"""The inner pages, printed with the homepage's press (tools/build.py helpers, assets/css/pages.css).

python -I tools/pages.py            all pages
python -I tools/pages.py film music only those
Pages: film, music, calendar (What's on), search, about, 404, plus article, work, artist, festival (tools/stories.py).
Never hand-edit the generated .html files.
"""
import json, os, re, sys
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402
import edition as E  # noqa: E402
from listings import EVENTS  # noqa: E402

NEWS = B.NEWS
PHOTOS = B.PHOTOS
MON = B.MONTHS
DAYS = 'Mon Tue Wed Thu Fri Sat Sun'.split()
TODAY = date(2026, 10, 15)

# where each researched story lives in the prototype
HOME_OF = {
    'athens-pff-2026-opens': 'article.html', 'suleiman-athens-retrospective': 'article.html',
    'mc-abdul-debut-album': 'artist.html',
    'boston-pff-2026': 'festival.html', 'edward-said-between-worlds': 'festival.html',
    'conversation-with-the-sea': 'work.html', 'doha-ff-2026-competition': 'work.html',
}


def link_of(nid):
    return HOME_OF.get(nid) or f'{"music" if NEWS[nid]["desk"] == "music" else "film"}.html#{nid}'


def has(slug):
    return slug in PHOTOS


def plate(p, cls='', lazy=True, lpi=None):
    return B.plate(p, cls, lazy, lpi) if p and has(p['slug']) else ''


def caption(p, override=None):
    return B.caption(p, override) if p and has(p['slug']) else ''


def d_label(iso, end=None, long=False):
    if not iso:
        return 'Date to come'
    y, m, d = map(int, iso.split('-'))
    dt = date(y, m, d)
    s = f'{DAYS[dt.weekday()]} {d} {MON[m - 1]}' if long else f'{d} {MON[m - 1]}'
    if end:
        y2, m2, d2 = map(int, end.split('-'))
        s = f'{d}–{d2} {MON[m - 1]}' if m2 == m else f'{d} {MON[m - 1]} – {d2} {MON[m2 - 1]}'
    if y != 2026:
        s += f' {y}'
    return s


def head(title, text, ink='ink-film', extra='', h='h1', lines=None, plate_html='', band=None, cls=''):
    """A page's own poster: the section printed as a one-sheet across the top."""
    item = {'id': 'top', 'title': title, 'lines': lines or [title]}
    b = B.band(band) if band else ''
    return (f'<header class="ph ink {ink} p-film {cls}">'
            f'<div class="ph-t p-key">{B.lines(item, h, href="#main")}</div>'
            f'<div class="ph-d p-key"><p class="deck">{text}</p>{b}{extra}</div>{plate_html}</header>')


def sec(sid, title, lede, body, cls=''):
    return (f'<section class="sec {cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="head"><h2 id="{sid}-h">{title}</h2>'
            f'<p>{lede}</p></div>{body}</section>')


# ---------------------------------------------------------------- stories index (the desk's archive)
# every story gets the honest photograph we have for it: its people, its work's makers or its venue
STORY_PH = {
    'elgouna-2026-opens': ('elgouna', 'The marina at El Gouna, Egypt, 15 March 2009.'),
    'athens-pff-2026-opens': ('suleiman', 'Elia Suleiman at the Sarajevo Film Festival, 2024.'),
    'jerusalem-festival-closes': ('damascus-gate', 'Damascus Gate, Jerusalem’s Old City, 8 November 2022.'),
    'mc-abdul-debut-album': ('mc-abdul', 'MC Abdul in Dallas, 28 September 2024.'),
    'boston-pff-2026': ('coolidge', 'The Coolidge Corner Theatre marquee, Brookline, 15 June 2024.'),
    'lff-2026-palestinian-titles': ('bfi', 'BFI Southbank, London, 10 December 2021.'),
    'rome-ff-yesterday-eye': ('mayasi', 'Rakan Mayasi, 22 August 2026.'),
    'doha-ff-2026-competition': ('el-basha', 'Kamel El Basha, 23 October 2021.'),
    'thirteen-in-gaza-netpac': ('gaza-port', 'Gaza seaport, 7 October 2017. Not a still from the film.'),
    'conversation-with-the-sea': ('rami-alayan', 'Rami Alayan, co-writer, at the Mostra de València, 21 October 2023.'),
    'who-is-still-alive-swiss-oscar': ('barbican-cinema', 'The Barbican Centre foyer, London, 23 February 2012.'),
    'lpff-2026': ('curzon-mayfair', 'Curzon Mayfair, London, June 2023.'),
    'bakri-tributes': ('bakri', 'Mohammad Bakri, 16 March 2010.'),
    'who-killed-alex-odeh-release': ('quad', 'The Quad Cinema, New York, 8 March 2014.'),
    'habibi-hussein-jenin': ('cinema-jenin', 'Cinema Jenin, 11 December 2008.'),
    'revolutionaries-never-die-locarno': ('yaqubi', 'Mohanad Yaqubi at Locarno, 10 August 2026.'),
    'chronicles-from-the-siege': ('alkhatib', 'Abdallah Al-Khatib at the Berlinale, 3 February 2026.'),
    'edward-said-between-worlds': ('said', 'Edward Said in Seville, 2002.'),
    'tpff-2026': ('jacir', 'Annemarie Jacir, whose Palestine 36 opened the festival, at TIFF 2025.'),
    'suleiman-athens-retrospective': ('onassis', 'The main stage of Onassis Stegi, Athens, 9 December 2018.'),
    'gaza-shorts-lpff': ('riverside', 'Riverside Studios, London, 2 July 2019.'),
    'pfi-durban-showcase': ('eltahri', 'Jihan El-Tahri at Locarno, 6 August 2025.'),
    'saint-levant-tour-postponed': ('saint-levant-live', 'Saint Levant at Melbourne Town Hall, 4 June 2026.'),
    'rasha-nahas-manaqish': ('rasha-nahas', 'Rasha Nahas at WOMEX, 27 October 2024.'),
    'faraj-suleiman-solo': ('faraj', 'Faraj Suleiman at WOMEX, 27 October 2019.'),
    'nai-barghouti-hong-kong': ('nai', 'Nai Barghouti, 18 October 2019.'),
    'al-festival-berlin-jubran-daboor': ('festsaal', 'Festsaal Kreuzberg, Berlin, 16 September 2023.'),
    'national-best-arabic-songs': ('saint-levant', 'Saint Levant in Madrid, 22 July 2025.'),
    'concrete-land': ('bertha', 'The Brunswick Centre, Bloomsbury, home of Bertha DocHouse, 11 September 2016.'),
}


def story_photo(nid):
    slug, cap = STORY_PH.get(nid, (None, None))
    if slug and has(slug):
        return {'slug': slug, 'focus': (0.5, 0.4), 'alt': re.split(r'[,.] ', cap)[0], 'caption': cap}
    return None


def story_rows(desk):
    rows = sorted((x for x in NEWS.values() if x['desk'] == desk), key=lambda x: x['date'], reverse=True)
    out = []
    for x in rows:
        y, m, d = map(int, x['date'].split('-'))
        state = 'due' if x.get('confidence') == 'medium' else 'on'
        ph = story_photo(x['id'])
        th = plate(ph, f'{"ink-music" if desk == "music" else "ink-film"} th-story', lpi=40) if ph else ''
        out.append(f'<li class="story{" has-th" if th else ""}" id="{x["id"]}">{B.vk(desk, state, B.DESK_NAME[desk])}'
                   f'<p class="dt"><b>{d}</b><small>{MON[m - 1]}</small></p>{th}'
                   f'<div><h3 class="hed"><a href="{link_of(x["id"]) if HOME_OF.get(x["id"]) else "#" + x["id"]}">{escape(x["title_facts"])}</a></h3>'
                   f'<p class="copy">{escape(x["summary"])}</p>{B.caption(ph) if ph else ""}{B.sources([x["id"]])}</div></li>')
    return '<ol class="stories">' + ''.join(out) + '</ol>'


# ---------------------------------------------------------------- film
PRIZES = [
    ('Thirteen in Gaza', 'Hosam Abu Dan', 'NETPAC Award', 'Toronto International Film Festival, 51st', 'Sep 2026', 'thirteen-in-gaza-netpac', 'gaza-port'),
    ('Revolutionaries Never Die', 'Mohanad Yaqubi', 'Special Jury Prize CINE+OCS, Cineasti del Presente', 'Locarno Film Festival, 79th', 'Aug 2026', 'revolutionaries-never-die-locarno', 'yaqubi'),
    ('Chronicles from the Siege', 'Abdallah Al-Khatib', 'GWFF Best First Feature Award', 'Berlinale, 76th', 'Feb 2026', 'chronicles-from-the-siege', 'alkhatib'),
    ('Who Killed Alex Odeh?', 'Jason Osder, William Lafi Youmans', 'Special Jury Award for Journalistic Excellence', 'Sundance Film Festival', 'Jan 2026', 'who-killed-alex-odeh-release', 'odeh-directors'),
    ('Who Is Still Alive', 'Nicolas Wadimoff', 'Prix de Soleure', 'Solothurn Film Festival', '', 'who-is-still-alive-swiss-oscar', 'wadimoff'),
]
PRIZE_PHOTOS = {
    'gaza-port': {'slug': 'gaza-port', 'focus': (0.5, 0.55), 'alt': 'Gaza seaport at dusk', 'caption': 'Gaza seaport, 7 October 2017. Not a still from the film.'},
    'yaqubi': {'slug': 'yaqubi', 'focus': (0.59, 0.222), 'zoom': 5.5, 'alt': 'Mohanad Yaqubi', 'caption': 'Mohanad Yaqubi at Locarno, 10 August 2026.'},
    'alkhatib': {'slug': 'alkhatib', 'focus': (0.5, 0.3), 'alt': 'Abdallah Al-Khatib', 'caption': 'Abdallah Al-Khatib at the Berlinale, 3 February 2026.'},
    'odeh-directors': {'slug': 'odeh-directors', 'focus': (0.5, 0.36), 'alt': 'Jason Osder and William Lafi Youmans with their award', 'caption': 'Jason Osder and William Lafi Youmans at the Sundance awards, 30 January 2026.'},
    'wadimoff': {'slug': 'wadimoff', 'focus': (0.5, 0.3), 'alt': 'Nicolas Wadimoff', 'caption': 'Nicolas Wadimoff.'},
}


def ledger():
    rows = ''
    for title, by, prize, fest, when, nid, ph in PRIZES:
        p = PRIZE_PHOTOS.get(ph)
        th = plate(p, 'ink-film th', lpi=34) if p else ''
        rows += (f'<li>{th or "<span class=th-none aria-hidden=true></span>"}<div class="lg-w"><p class="lg-t"><em>{escape(title)}</em></p><p class="lg-b">{escape(by)}</p></div>'
                 f'<p class="lg-p">{escape(prize)}</p><p class="lg-f">{escape(fest)}<span>{escape(when)}</span></p></li>')
    return f'<ol class="ledger">{rows}</ol>' + B.sources([x[5] for x in PRIZES], cap=6)


def tour(events, thumbs=True):
    """The tour-poster date list, grouped by month, every row a real event with a link."""
    rows, month = [], None
    for ev in events:
        key = ev['start'][:7] if ev['start'] else 'tba'
        if key != month:
            month = key
            if key == 'tba':
                label = 'Not yet dated'
            else:
                y, m = map(int, key.split('-'))
                label = f'{["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][m - 1]} {y}'
            rows.append(f'<li class="year" role="presentation">{label}</li>')
        ink = {'film': 'ink-film', 'music': 'ink-music', 'both': 'ink-over'}[ev['desk']]
        if ev['start']:
            y, m, d = map(int, ev['start'].split('-'))
            n = str(d) + (f'–{int(ev["end"][8:])}' if ev.get('end') and ev['end'][5:7] == ev['start'][5:7] else '')
            mo = MON[m - 1]
        else:
            n, mo = 'TBA', ''
        th = ''
        if thumbs and ev.get('photo') and has(ev['photo']['slug']):
            th = plate(ev['photo'], f'{ink} th', lpi=26)
        place = ev['city'] + (' · ' + ev['venue'] if ev['venue'] and ev['venue'] != ev['city'] else '')
        time_ = f' · {ev["time"]} local' if ev.get('time') else ''
        rows.append(f'<li class="row {ink}{" due" if ev["state"] == "due" else ""}{" has-th" if th else ""}" data-desk="{ev["desk"]}" data-city="{escape(ev["city"])}" '
                    f'data-state="{ev["state"]}"><p class="dt"><b{" class=rng" if "–" in n else ""}>{n}</b><small>{mo}</small></p>{th}'
                    f'<div class="wh"><p class="what"><a href="{ev["link"]}">{ev["what"]}</a></p><p class="where">{escape(place)}{time_}{" · expected" if ev["state"] == "due" else ""}</p></div>'
                    f'{B.vk(ev["desk"], ev["state"], B.DESK_NAME[ev["desk"]] + ", " + B.STATE_NAME[ev["state"]])}</li>')
    # two printed columns, split by count; a month that breaks across them repeats its heading
    if len(rows) < 8:
        return '<div class="tour-cols one"><ol class="tour">' + ''.join(rows) + '</ol></div>'
    half = (len(rows) + 1) // 2
    if rows[half].startswith('<li class="year"'):
        half += 1
    left, right = rows[:half], rows[half:]
    if right and not right[0].startswith('<li class="year"'):
        head = next(r for r in reversed(left) if r.startswith('<li class="year"'))
        right = [head.replace('role="presentation">', 'role="presentation" aria-hidden="true">')] + right
    return ('<div class="tour-cols"><ol class="tour">' + ''.join(left) + '</ol><ol class="tour">' + ''.join(right) + '</ol></div>')


def upcoming(desk=None):
    evs = [e for e in EVENTS if (desk is None or e['desk'] == desk)]
    dated = sorted((e for e in evs if e['start']), key=lambda e: e['start'])
    return [e for e in dated if e['start'] >= '2026-10-15'] + [e for e in evs if not e['start']]


def film():
    L = E.LEAD
    lead = (f'<article class="lead-sheet ink ink-film" id="lead">{plate(L["photo"], lpi=110)}<div class="txt">'
            f'{B.lines(L, "h2", href="article.html")}<p class="copy">{L["deck"]}</p>{B.band([(k, escape(v)) for k, v in L["band"]])}'
            f'{caption(L["photo"])}</div></article>')
    circuit = ''.join(B.sheet(x) for x in E.CIRCUIT)
    for a, b in (('href="#boston"', 'href="festival.html"'), ('href="#el-gouna"', 'href="#el-gouna-run"')):
        circuit = circuit.replace(a, b)
    main = (head('Film', 'Where Palestinian films are this week and after: premieres, festival runs, prizes and releases, '
                 'each with its date, its place and its source.', 'ink-film',
                 band=[('On screens this week', '7 festivals'), ('In competition next', 'Doha, 19–27 Nov'), ('Next release', 'Who Killed Alex Odeh?, 30 Oct')])
            + f'<section class="sec first" aria-label="The lead">{lead}</section>'
            + sec('festivals', 'Festivals this week', 'Festival by festival, the Palestinian films playing between now and Sunday.', f'<div class="wall">{circuit}</div>')
            + B.doha().replace('href="#doha"', 'href="work.html"')
            + sec('prizes', 'Prizes this year', 'What Palestinian films have won in 2026, as each festival announced it.', ledger())
            + sec('el-gouna-run', 'In cinemas', '<em>Who Killed Alex Odeh?</em> opens in US cinemas on 30 October with Watermelon Pictures.',
                  tour([e for e in upcoming('film') if 'Alex Odeh' in e['what'] and e['kind'] in ('release', 'screening')]))
            + oscars()
            + sec('dates', 'Film dates ahead', 'Every film date we know of, in local time. A tinted date is expected.', tour(upcoming('film')))
            + B.reissue()
            + sec('stories', 'All film stories', 'Everything the film desk has reported for this edition, newest first.', story_rows('film')))
    photos = [L['photo']] + [x['photo'] for x in E.CIRCUIT if x.get('photo')] + E.DOHA['photos'] + [PRIZE_PHOTOS[x[6]] for x in PRIZES if x[6] in PRIZE_PHOTOS and has(x[6])] \
        + [E.REISSUE['photo']] + E.REISSUE['small'] + [e['photo'] for e in EVENTS if e.get('photo')] \
        + [story_photo(x['id']) for x in NEWS.values() if x['desk'] == 'film' and story_photo(x['id'])]
    B.page('film.html', 'Film — VPalestine', 'Palestinian films this week: festivals, prizes, releases and every date ahead.', main, 'film.html', photos)


def oscars():
    n = NEWS['citizen-osama-oscar']
    w = NEWS['who-is-still-alive-swiss-oscar']
    stops = [('Submitted', '30 Sep'), ('Shortlist of 15', '15 Dec'), ('Nominations', '21 Jan 2027'), ('Ceremony', '14 Mar 2027')]
    road = ''.join(f'<li><b>{escape(a)}</b><small>{escape(b)}</small></li>' for a, b in stops)
    return (f'<section class="sec" id="oscars" aria-labelledby="oscars-h"><div class="head"><h2 id="oscars-h">The Oscar road</h2>'
            '<p>Best International Feature, 99th Academy Awards.</p></div><div class="oscar">'
            f'<article class="sheet ink ink-film st-due"><h3 class="lines" data-fit><span class="ln">Citizen Osama</span></h3>'
            f'<p class="copy">{escape(n["summary"])}</p><ol class="road">{road}</ol>{B.sources(["citizen-osama-oscar"])}</article>'
            f'<article class="sheet ink ink-stock"><h3 class="lines" data-fit><span class="ln">Who Is</span><span class="ln">Still Alive</span></h3>'
            f'<p class="copy">{escape(w["summary"])}</p>{B.sources(["who-is-still-alive-swiss-oscar"])}</article></div></section>')


# ---------------------------------------------------------------- music
RELEASES = [
    dict(t='Day by Day, Shway Shway', by='MC Abdul', what='Debut album, nine tracks', when='Out Fri 16 Oct', label='EMPIRE', state='due', slug='mc-abdul', focus=(0.48, 0.30), link='artist.html', src='mc-abdul-debut-album'),
    dict(t='Afandi', by='Saint Levant', what='Second album, his first entirely in Arabic', when='Out 21 Aug', label='', state='on', slug='saint-levant-live', focus=(0.5, 0.4), link='#saint-levant', src='saint-levant-tour-postponed'),
    dict(t='Manaqish', by='Rasha Nahas', what='Single; the album produced by Meshell Ndegeocello has no date yet', when='Out 25 Sep', label='', state='on', slug='rasha-nahas', focus=(0.40, 0.55), zoom=1.5, link='#rasha-nahas', src='rasha-nahas-manaqish'),
    dict(t='Nano', by='Tul8te and Saint Levant', what='No. 1 on Spotify in Egypt, in The National’s songs of the year so far', when='Out 1 Jun', label='', state='on', slug='tul8te', focus=(0.5, 0.3), link='#chart', src='national-best-arabic-songs'),
    dict(t='Nassaba', by='Siilawy', what='In The National’s songs of the year so far', when='Out 17 Apr', label='', state='on', slug='siilawy', focus=(0.5, 0.3), link='#chart', src='national-best-arabic-songs'),
    dict(t='Dawaween', by='Shbash with Rknddn', what='In The National’s songs of the year so far', when='Out 13 Feb', label='', state='on', slug='shbash', focus=(0.5, 0.3), link='#chart', src='national-best-arabic-songs'),
]


def sleeves():
    out = ''
    for r in RELEASES:
        p = {'slug': r['slug'], 'focus': r['focus'], 'alt': r['by'], 'caption': ''}
        if r.get('zoom'):
            p['zoom'] = r['zoom']
        pl = plate(p, 'ink-music', lpi=54) if has(r['slug']) else f'<div class="plate ink-music no-photo" aria-hidden="true"><span>{escape(r["by"])}</span></div>'
        st = {'due': ' st-due', 'on': '', 'gone': ' st-gone'}[r['state']]
        out += (f'<li class="sl{st}">{pl}<h3><a href="{r["link"]}"><em>{escape(r["t"])}</em></a></h3><p class="by">{escape(r["by"])}</p>'
                f'<p class="wh">{escape(r["what"])}</p><p class="dd">{escape(r["when"])}{(" · " + escape(r["label"])) if r["label"] else ""}{" · expected" if r["state"] == "due" else ""}</p></li>')
    return (f'<ul class="sleeves">{out}</ul><p class="cap note">Sleeves are set in VPalestine’s type over a photograph of the artist; '
            'they are not the releases’ own artwork.</p>' + B.sources([r['src'] for r in RELEASES], cap=5))


def music():
    S = E.SLEEVE
    lead = (f'<article class="lead-sheet ink ink-music" id="lead">{plate(S["photo"], lpi=90)}<div class="txt">'
            f'{B.lines(S, "h2", href="artist.html")}<p class="hed">{escape(S["title"])}</p><p class="copy">{S["text"]}</p>'
            f'{B.band([(k, escape(v)) for k, v in S["band"]])}{caption(S["photo"])}</div></article>')
    chart_items = [('Nano', 'Tul8te and Saint Levant', '1 June', 'No. 1 on Spotify in Egypt; in the top 10 through the summer'),
                   ('Nassaba', 'Siilawy, Jordanian-Palestinian singer', '17 April', ''),
                   ('Dawaween', 'Shbash, Jordanian rapper, with Palestinian artist Rknddn', '13 February', '')]
    chart = ''.join(f'<li><b>{i + 1}</b><div><p class="lg-t"><em>{escape(t)}</em></p><p class="lg-b">{escape(a)}</p></div><p class="lg-f">{escape(d)}<span>{escape(n)}</span></p></li>'
                    for i, (t, a, d, n) in enumerate(chart_items))
    record = B.record()
    main = (head('Music', 'Palestinian records, singles, tours and concerts: what came out, what is coming, and where to hear it, '
                 'in the local time of every stage.', 'ink-music',
                 band=[('Out tomorrow', 'MC Abdul, Day by Day, Shway Shway'), ('Last night tonight', 'Jerusalem Festival'), ('Next show', 'MC Abdul, Sat 17 Oct')])
            + f'<section class="sec first" aria-label="The lead">{lead}</section>'
            + sec('releases', 'Releases', 'Albums and singles of 2026, newest first.', sleeves())
            + record.replace('<section class="sec" id="record"', '<section class="sec" id="stages"').replace('id="record-h">Records and stages', 'id="record-h">Stages and tours')
            + sec('chart', 'Songs of the year so far', 'Palestinian artists in The National’s list of the best Arabic songs of 2026, published 5 October.',
                  f'<ol class="ledger chart">{chart}</ol>' + B.sources(['national-best-arabic-songs']))
            + sec('dates', 'Music dates ahead', 'Concerts and releases we know of, in local time. A tinted date is expected.', tour(upcoming('music')))
            + sec('stories', 'All music stories', 'Everything the music desk has reported for this edition, newest first.', story_rows('music')))
    photos = [S['photo']] + [x['photo'] for x in E.RECORD if x.get('photo')] \
        + [{'slug': r['slug'], 'caption': f'{r["by"]}.'} for r in RELEASES if has(r['slug'])] + [e['photo'] for e in EVENTS if e.get('photo')] \
        + [story_photo(x['id']) for x in NEWS.values() if x['desk'] == 'music' and story_photo(x['id'])]
    B.page('music.html', 'Music — VPalestine', 'Palestinian records, tours and concerts: releases of 2026 and every date ahead.', main, 'music.html', photos)


# ---------------------------------------------------------------- what's on
def calendar():
    evs = upcoming()
    cities = sorted({e['city'] for e in evs if e['city'] != 'Everywhere'})
    n_on = sum(1 for e in evs if e['state'] == 'on')
    filters = ('<form class="filters" aria-label="Filter the dates" onsubmit="return false">'
               '<fieldset><legend class="label">Desk</legend><div class="chips">'
               f'<button type="button" class="chip" data-desk="all" aria-pressed="true">All</button>'
               f'<button type="button" class="chip" data-desk="film" aria-pressed="false">{B.vk("film")} Film</button>'
               f'<button type="button" class="chip" data-desk="music" aria-pressed="false">{B.vk("music")} Music</button></div></fieldset>'
               '<label class="sel"><span class="label">City</span><select id="city"><option value="">Every city</option>'
               + ''.join(f'<option>{escape(c)}</option>' for c in cities) + '</select></label>'
               f'<label class="tog"><input type="checkbox" id="due" checked> <span>{B.vk("film", "due")} Include expected dates</span></label>'
               '<p class="count" id="count" aria-live="polite"></p></form>')
    ics = '<a class="btn ghost" href="assets/vpalestine-dates.ics" download>Add the confirmed dates to your calendar</a>'
    main = (head('What’s on', 'Every Palestinian film and music date we know of, from tonight to March, in the local time of the venue. '
                 'Filter by desk or city; expected dates print as a tint until they are confirmed.', 'ink-over', cls='two',
                 lines=['What’s on'], band=[('Dates', f'{len(evs)}'), ('Confirmed', f'{n_on}'), ('Cities', f'{len(cities)}')], extra=ics)
            + f'<section class="sec first cal" aria-label="Dates">{filters}{tour(evs)}<p class="empty" id="empty" hidden>No dates match. Clear a filter to see more.</p>'
            f'<div class="pad">{B.sources(sorted({e["src"] for e in evs}), cap=0, fold=True)}</div></section>')
    photos = [e['photo'] for e in evs if e.get('photo')]
    B.page('calendar.html', 'What’s on — VPalestine', 'Every Palestinian film and music date ahead, in local time, by desk and city.', main, 'calendar.html', photos, js=('pages.js',))
    write_ics(evs)


def write_ics(evs):
    """One calendar file with every confirmed, dated event (all-day entries; local times go in the description)."""
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//VPalestine//What is on//EN', 'CALSCALE:GREGORIAN', 'X-WR-CALNAME:VPalestine dates']
    for i, e in enumerate(evs):
        if not e['start'] or e['state'] != 'on':
            continue
        s = e['start'].replace('-', '')
        end = (e.get('end') or e['start'])
        y, m, d = map(int, end.split('-'))
        nxt = date.fromordinal(date(y, m, d).toordinal() + 1).strftime('%Y%m%d')
        what = re.sub(r'<[^>]+>', '', e['what'])
        desc = (f'{e["venue"]}, {e["city"]}' + (f' · {e["time"]} local time' if e['time'] else '')).replace(',', '\\,')
        lines += ['BEGIN:VEVENT', f'UID:vp-{s}-{i}@vpalestine.prototype', 'DTSTAMP:20261015T000000Z', f'DTSTART;VALUE=DATE:{s}', f'DTEND;VALUE=DATE:{nxt}',
                  'SUMMARY:' + what.replace(',', '\\,').replace(';', '\\;'), 'LOCATION:' + f'{e["venue"]}, {e["city"]}'.replace(',', '\\,').replace(';', '\\;'),
                  'DESCRIPTION:' + desc, 'END:VEVENT']
    lines.append('END:VCALENDAR')
    open(os.path.join(ROOT, 'assets', 'vpalestine-dates.ics'), 'w', encoding='utf-8', newline='\r\n').write('\n'.join(lines) + '\n')


# ---------------------------------------------------------------- search
def search():
    idx = []
    for x in NEWS.values():
        idx.append({'id': x['id'], 'desk': x['desk'], 'date': x['date'], 'title': x['title_facts'], 'text': x['summary'],
                    'tags': ' '.join(x.get('people', []) + [w['title'] for w in x.get('works', [])] + x.get('places', [])),
                    'href': link_of(x['id']), 'state': 'due' if x.get('confidence') == 'medium' else 'on',
                    'img': (STORY_PH[x['id']][0] if x['id'] in STORY_PH and has(STORY_PH[x['id']][0]) else '')})
    os.makedirs(os.path.join(ROOT, 'assets', 'data'), exist_ok=True)
    json.dump(sorted(idx, key=lambda r: r['date'], reverse=True), open(os.path.join(ROOT, 'assets', 'data', 'search.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tries = ['Gaza', 'Suleiman', 'Boston', 'MC Abdul', 'Doha', 'London', 'Oscar', 'Jerusalem']
    main = ('<section class="srch" aria-labelledby="s-h"><form class="sfield" role="search" action="search.html" method="get">'
            '<h1 id="s-h" class="vh">Search VPalestine</h1>'
            '<label class="vh" for="q">Search films, records, people and places</label>'
            '<input id="q" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="A film, an artist, a city">'
            '<button class="btn" type="submit">Search</button></form>'
            '<p class="tries"><span class="label">Try</span>' + ''.join(f'<a href="search.html?q={escape(t)}">{escape(t)}</a>' for t in tries) + '</p>'
            f'<div class="facets" role="group" aria-label="Desk"><button type="button" class="chip" data-desk="all" aria-pressed="true">All <span></span></button>'
            f'<button type="button" class="chip" data-desk="film" aria-pressed="false">{B.vk("film")} Film <span></span></button>'
            f'<button type="button" class="chip" data-desk="music" aria-pressed="false">{B.vk("music")} Music <span></span></button></div>'
            '<p class="count" id="count" aria-live="polite"></p><ol class="results" id="results"></ol>'
            '<div class="noresult" id="none" hidden><p class="lines big" data-fit><span class="ln">Nothing printed</span></p>'
            '<p class="copy">No story matches that yet. Try a film title, an artist, a festival or a city, or browse <a href="calendar.html">What’s on</a>.</p></div>'
            '<noscript><p class="copy">Search needs JavaScript. Every story is listed on the <a href="film.html#stories">Film</a> and <a href="music.html#stories">Music</a> pages.</p></noscript></section>')
    B.page('search.html', 'Search — VPalestine', 'Search Palestinian films, records, people and places on VPalestine.', main, 'search.html', [], js=('pages.js',))


# ---------------------------------------------------------------- about
def about():
    form = ('<form class="sendform" id="send-form" action="#" method="post" novalidate>'
            '<fieldset><legend class="label">What is it</legend><div class="chips">'
            '<label class="chip"><input type="radio" name="kind" value="screening" checked> Screening</label>'
            '<label class="chip"><input type="radio" name="kind" value="concert"> Concert</label>'
            '<label class="chip"><input type="radio" name="kind" value="release"> Release</label>'
            '<label class="chip"><input type="radio" name="kind" value="festival"> Festival</label></div></fieldset>'
            '<label><span class="label">Title of the film, record or event</span><input name="title" required autocomplete="off"></label>'
            '<div class="two"><label><span class="label">Date</span><input name="date" type="date" required></label>'
            '<label><span class="label">Local time</span><input name="time" type="time"></label></div>'
            '<div class="two"><label><span class="label">Venue</span><input name="venue" autocomplete="off"></label>'
            '<label><span class="label">City</span><input name="city" required autocomplete="address-level2"></label></div>'
            '<label><span class="label">A public link that confirms it</span><input name="link" type="url" placeholder="https://" required></label>'
            '<label><span class="label">Your email, so we can check with you</span><input name="email" type="email" autocomplete="email" required></label>'
            '<button class="btn" type="submit">Send it</button><p class="note" role="status">[FORM BACKEND] Placeholder: nothing is sent from this prototype.</p></form>')
    rules = [('The work leads.', 'A film or a record, and the people who made it, come before the event around it.'),
             ('Film and music share one page.', 'Two desks, one grammar: neither is a sub-section of the other, and where they meet the page prints both.'),
             ('Every date names its source.', 'Each story carries the pages it was checked against, with their dates.'),
             ('Expected stays expected.', 'A release without a date or a result still to come prints as a tint until it is confirmed.'),
             ('Local time, with the place.', 'Times are the venue’s own; a reader in another city converts, not us.'),
             ('Palestinian work at full dignity.', 'No war imagery as decoration and no pity framing; the work is the story.')]
    main = (head('About VPalestine', 'Palestinian film and music in English, followed from premiere to audience: what premiered, what won, '
                 'what is screening or out, and who is playing where.', 'ink-over', cls='two', lines=['About', 'VPalestine'])
            + sec('how', 'How we work', 'Six rules every page is printed by.',
                  '<ol class="rules big">' + ''.join(f'<li><b>{escape(a)}</b> {escape(b)}</li>' for a, b in rules) + '</ol>')
            + sec('corrections', 'Corrections', 'When we get something wrong, the story says so.',
                  '<div class="prose"><p class="copy">Corrections are printed at the foot of the story they correct, with the date of the change and what was wrong. '
                  'A changed date or venue is marked on the listing itself: the old date keeps its outline, the new one prints in ink.</p>'
                  '<p class="copy">Write to <b>[CORRECTIONS EMAIL]</b> with the story’s address and what needs fixing.</p></div>')
            + sec('send', 'Send us a screening', 'A film screening, a concert, a release or a festival with Palestinian work in it. We list it once we can confirm it.', form)
            + sec('contact', 'Contact', 'Editors, press and partnerships.',
                  '<dl class="band contact"><div><dt>Editors</dt><dd>[EDITORS EMAIL]</dd></div><div><dt>Press</dt><dd>[PRESS EMAIL]</dd></div>'
                  '<div><dt>Social</dt><dd>[SOCIAL HANDLES]</dd></div><div><dt>Masthead</dt><dd>[STAFF AND PUBLISHER DETAILS]</dd></div></dl>'
                  '<p class="copy note">The identity of this site is documented in the <a href="index.html">identity book</a>.</p>'))
    B.page('about.html', 'About — VPalestine', 'What VPalestine covers, how it checks what it prints, corrections, and how to send us a screening.', main, 'about.html', [], js=('pages.js',))


# ---------------------------------------------------------------- 404
def notfound():
    v = B.MARKS['v']
    mis = (f'<svg class="mis" viewBox="-400 -120 1867 1590" aria-hidden="true">'
           f'<path class="f" transform="translate(-260 40)" d="{v["film"]}"/><path class="m" transform="translate(240 -60)" d="{v["music"]}"/></svg>')
    main = (f'<section class="misprint" aria-labelledby="nf-h"><div class="mis-art">{mis}</div><div class="mis-t">'
            '<h1 id="nf-h" class="lines" data-fit><span class="ln">This sheet</span><span class="ln">didn’t print</span></h1>'
            '<p class="copy">The two screens never met on this page: the address may have changed, or it has a typo. '
            'Everything else is still on the press.</p>'
            '<form class="sfield small" role="search" action="search.html" method="get"><label class="vh" for="q404">Search VPalestine</label>'
            '<input id="q404" name="q" type="search" placeholder="Search a film, an artist, a city"><button class="btn" type="submit">Search</button></form>'
            '<p class="links"><a class="btn" href="home.html">Today’s edition</a> <a class="btn ghost" href="calendar.html">What’s on</a></p></div></section>')
    B.page('404.html', 'Not found — VPalestine', 'This page did not print.', main, None, [])
    # GitHub Pages serves 404.html at any depth: resolve every relative address from the site root
    p = os.path.join(ROOT, '404.html')
    s = open(p, encoding='utf-8').read()
    base = ("<script>document.write('<base href=\"'+(location.hostname.endsWith('github.io')?'/vpalestine-prototype/':'/')+'\">')</script>\n")
    s = s.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + base, 1)
    open(p, 'w', encoding='utf-8').write(s)


PAGES = {'film': film, 'music': music, 'calendar': calendar, 'search': search, 'about': about, '404': notfound}

if __name__ == '__main__':
    want = sys.argv[1:] or list(PAGES)
    for k in want:
        if k in PAGES:
            PAGES[k]()
    try:
        import stories  # noqa: E402  (article, work, artist, festival)
        for k in want if sys.argv[1:] else stories.PAGES:
            if k in stories.PAGES:
                stories.PAGES[k]()
    except ImportError:
        pass
