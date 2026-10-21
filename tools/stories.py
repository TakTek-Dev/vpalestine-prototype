"""The story pages: article (a report), work (one film's life), artist (one musician), festival (one festival's programme).

Built by tools/pages.py. Facts come from research/pages.json and research/news.json; nothing here is unsourced.
"""
import json, os, re, sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402
import edition as E  # noqa: E402
import pages as P  # noqa: E402

R = json.load(open(os.path.join(ROOT, 'research', 'pages.json'), encoding='utf-8'))
MON = B.MONTHS


def src_list(items):
    """Sources by name and link only: the research was re-checked after the edition date, so access dates are not printed."""
    seen, out = set(), []
    for s in items:
        name = s['name'].split(' (')[0]
        if s['url'] in seen or name in seen:
            continue
        seen.update((s['url'], name))
        out.append(f'<li><a href="{escape(s["url"])}">{escape(name)}</a></li>')
    return f'<section class="srcs" aria-labelledby="srcs-h"><h2 id="srcs-h" class="label">Sources</h2><ul>{"".join(out)}</ul></section>'


def when(iso, t=None):
    y, m, d = map(int, iso.split('-'))
    from datetime import date
    wd = 'Mon Tue Wed Thu Fri Sat Sun'.split()[date(y, m, d).weekday()]
    return f'{wd} {d} {MON[m - 1]}' + (f', {t}' if t else '')


def handbill(title, rows, foot=''):
    """The aside: a printed handbill of dates. rows: (date-label, time, venue, what-html, note)"""
    lis = ''.join(f'<li><p class="hb-d">{d}<small>{t}</small></p><div><p class="hb-w">{w}</p><p class="hb-v">{escape(v)}{(" · " + n) if n else ""}</p></div></li>'
                  for d, t, v, w, n in rows)
    return f'<aside class="handbill" aria-label="{escape(title)}"><h2 class="label">{escape(title)}</h2><ol>{lis}</ol>{foot}</aside>'


def related(items):
    """Three sheets to go on to, each with its photograph."""
    out = ''
    for href, ink, kicker_free_title, text, ph in items:
        pl = P.plate(ph, ink + ' th-big', lpi=70) if ph else ''
        out += (f'<article class="rel">{pl}<h3 class="hed"><a class="stretch" href="{href}">{escape(kicker_free_title)}</a></h3>'
                f'<p class="copy">{text}</p></article>')
    return f'<section class="sec related" aria-labelledby="rel-h"><div class="head"><h2 id="rel-h">Read on</h2><p>More from this edition.</p></div><div class="rels">{out}</div></section>'


# ---------------------------------------------------------------- article: Athens, Suleiman
ATHENS_PH = [
    {'slug': 'onassis', 'focus': (0.5, 0.5), 'alt': 'The main stage of Onassis Stegi, Athens', 'caption': 'The main stage of Onassis Stegi, Athens, 9 December 2018, where the run ends.'},
    {'slug': 'emst', 'focus': (0.5, 0.5), 'alt': 'EMST, the National Museum of Contemporary Art, Athens', 'caption': 'EMST, the National Museum of Contemporary Art, Athens, 5 November 2021.'},
]


def article():
    S = R['suleiman']
    A = R['athens_pff']
    L = E.LEAD
    feats = {f['title']: f for f in S['features']}
    order = ['Chronicle of a Disappearance', 'Divine Intervention', 'The Time That Remains', 'It Must Be Heaven']
    notes = {
        'Chronicle of a Disappearance': ('Venice 1996', 'Luigi De Laurentiis Award for a debut film'),
        'Divine Intervention': ('Cannes 2002, Competition', 'Jury Prize and FIPRESCI Prize'),
        'The Time That Remains': ('Cannes 2009, Competition', 'Jury Grand Prize, Asia Pacific Screen Awards, shared with About Elly'),
        'It Must Be Heaven': ('Cannes 2019, Competition', 'Special Mention and FIPRESCI Prize'),
    }
    ledger = ''
    for t in order:
        f = feats[t]
        sc = f['apff26_screening']
        fest, prize = notes[t]
        ledger += (f'<li><p class="yr">{f["year"]}</p><div><p class="lg-t"><em>{escape(t)}</em></p><p class="lg-b">{f["runtime_min"]}′ · {escape(fest)}</p></div>'
                   f'<p class="lg-p">{escape(prize)}</p><p class="lg-f">In Athens<span>{when(sc["date"], sc["time"])} · {escape(sc["venue"])}</span></p></li>')
    body = f'''
<p class="lede">The Athens Palestine Film Festival, now in its fifth year, opens at 20:00 tonight at the Trianon Cinema with Elia Suleiman’s <em>It Must Be Heaven</em> (2019), and Suleiman is listed to attend. The screening starts a retrospective the festival calls <em>A World in Silence</em>: all four of his features, each with Greek and English subtitles.</p>
<p><em>The Time That Remains</em> (2009) follows on Friday at 21:00, with a Q&amp;A with Suleiman afterwards. <em>Divine Intervention</em> (2002) plays on Sunday at 21:00, also at the Trianon. The run ends on 31 October at Onassis Stegi with <em>Chronicle of a Disappearance</em> (1996), his first feature.</p>
<h2>Four films, three decades</h2>
<ol class="ledger films">{ledger}</ol>
<h2>Who he is</h2>
<p>Suleiman was born in Nazareth in 1960. The festival’s biography says he lived in New York from 1981 to 1993 (other accounts give 1982), then moved to Jerusalem in 1994, where the European Commission entrusted him with setting up the Film and Media Department at Birzeit University. He sat on the Cannes jury in 2006 and is an artistic advisor to the Doha Film Institute. Among the honours the festival lists are the Prince Claus Award (2008), the European Achievement Award in World Cinema (2022) and the Heart of Sarajevo (2024).</p>
<div class="run-photos">{"".join(f'<figure>{P.plate(v, "ink-film", lpi=80)}<figcaption class="cap">{v["caption"]} {B.credit(v["slug"])}</figcaption></figure>' for v in ATHENS_PH if P.has(v["slug"]))}</div>
<h2>The rest of the festival</h2>
<p>APFF26 runs until 31 October at the Trianon, the National Museum of Contemporary Art (EMST) and Onassis Stegi, under the theme “Nothing comes from nothing”. It is presented by Dounias, the not-for-profit founded by its director, Carol Sansour.</p>
<p>Three short-film programmes, <em>Palescope 1</em> to <em>3</em>, play at the Trianon at 18:30 from Friday to Sunday. Alex Bakri’s <em>Habibi Hussein</em>, about Cinema Jenin’s last projectionist, screens on 23 October and <em>Who Killed Alex Odeh?</em> on 24 October. Two evenings, on 24 and 25 October, honour Mohammad Bakri, who died last December, with his family present.</p>
<p class="corr">No corrections to this story.</p>'''
    rows = [(when(x['date']), x['time'], x['venue'], f'<em>{escape(x["film"])}</em>', escape(x['notes']) if x.get('notes') else '')
            for x in S['apff26_retrospective']['screenings_in_order']]
    venues = ''.join(f'<li><b>{escape(v["name"].split(" (")[0])}</b>{escape(v["address"])}</li>' for v in A['venues'])
    aside = handbill('A World in Silence: the four screenings', rows,
                     f'<h2 class="label">Venues</h2><ul class="venues">{venues}</ul>'
                     '<p class="hb-n">Trianon tickets through more.com; Onassis Stegi through its own box office. Prices are not published on the festival site.</p>')
    head = (f'<header class="art-head ink ink-film p-film">{B.plate(L["photo"], lazy=False, lpi=118)}'
            f'<div class="ah-t p-key">{B.lines(L, "h1", href="#main")}'
            '<p class="stand">The first of four Suleiman features the Athens Palestine Film Festival shows by 31 October, with the director there for the opening.</p>'
            '<p class="byline">Film desk · <time datetime="2026-10-15">Thursday 15 October 2026</time></p>'
            f'{B.band([(k, escape(v)) for k, v in L["band"]])}{B.caption(L["photo"])}</div></header>')
    billing = ('<p class="billing" aria-label="Retrospective credits">Athens Palestine Film Festival presents <b>Elia Suleiman</b> '
               '<span>A World in Silence</span> four features · Trianon Cinema · Onassis Stegi · 15–31 October 2026 · Greek and English subtitles</p>')
    srcs = src_list(S['apff26_retrospective']['sources'] + A['sources'] + [s for f in S['features'] for s in f['sources']] + S['born_sources'])
    rel = related([
        ('festival.html', 'ink-film', 'Boston’s Palestine film festival turns twenty tomorrow', 'Ten days, four venues, from <em>Edward Said: Between Worlds</em> to <em>Palestine Comedy Club</em>.',
         E.CIRCUIT[0]['photo']),
        ('work.html', 'ink-film', 'Conversation With the Sea, from Venice to Doha', 'Muayad Alayan’s new film, stop by stop.', E.DOHA['photos'][1]),
        ('artist.html', 'ink-music', 'MC Abdul’s first album is out tomorrow', 'Nine tracks on EMPIRE, then Palestine Culture Day in Redwood City.', E.SLEEVE['photo']),
    ])
    main = (head + f'<div class="art-body"><article class="prose-col">{billing}{body}{srcs}</article>{aside}</div>' + rel)
    photos = [L['photo'], E.CIRCUIT[0]['photo'], E.DOHA['photos'][1], E.SLEEVE['photo']] + [v for v in ATHENS_PH if P.has(v['slug'])]
    B.page('article.html', 'Elia Suleiman: all four films, from tonight in Athens — VPalestine',
           'The Athens Palestine Film Festival opens with It Must Be Heaven and shows all four Elia Suleiman features by 31 October.', main, 'film.html', photos)


PAGES = {'article': article}


# ---------------------------------------------------------------- work: one film's life
def work():
    C = R['conversation_with_the_sea']
    M = C['muayad_alayan']
    lead = {'slug': 'el-basha', 'focus': (0.30, 0.42), 'zoom': 1.3,
            'alt': 'Kamel El Basha seated before a lit dressing-room mirror, his reflection behind him',
            'caption': 'Kamel El Basha, who plays Kamal, 23 October 2021.'}
    item = {'id': 'work', 'title': 'Conversation With the Sea', 'lines': ['Conversation', 'with the Sea']}
    head = (f'<header class="work-head ink ink-film p-film">{B.plate(lead, lazy=False, lpi=120)}'
            f'<div class="wh-t p-key">{B.lines(item, "h1", href="#main")}'
            '<p class="stand">In Jerusalem, a court orders a 60-year-old man to repay a social-security debt said to be owed by his son, who drowned in the Red Sea decades ago and whose death no record shows.</p>'
            '<p class="byline">A film by Muayad Alayan · <em>Hiwar ma’ albahr</em> · 2026</p>'
            + B.band([('Runtime', '112′'), ('Languages', 'Arabic, Hebrew, English'), ('Countries', 'Palestine, Netherlands, Saudi Arabia, Qatar'), ('Next', 'Doha, 19–27 Nov')])
            + f'{B.caption(lead)}</div></header>')
    # the run: every stop of the film's life, in ink density
    stops = [
        ('7 Sep', 'Venice', '83rd Venice International Film Festival', 'World premiere · Venice Spotlight', 'gone', 'Screened'),
        ('11–17 Sep', 'Toronto', '51st Toronto International Film Festival', 'North American premiere · Centrepiece', 'gone', 'Screened'),
        ('24 Sep – 3 Oct', 'Hamburg', 'Filmfest Hamburg', 'German premiere · Kaleidoscope (one report)', 'gone', 'Screened'),
        ('9–18 Oct', 'Warsaw', '42nd Warsaw International Film Festival', 'Eastern European premiere · International Competition', 'on', 'On now'),
        ('30 Oct', 'Toronto', 'Muslim International Film Festival', 'Opening night, with the Toronto Palestine Film Festival', 'on', 'Next'),
        ('19–27 Nov', 'Doha', 'Doha Film Festival', 'MENA premiere · International Feature Film Competition · screening date not yet published', 'due', 'Date to come'),
        ('27 Nov', 'London', 'London Palestine Film Festival', 'Closing film · Curzon Mayfair', 'on', 'Booked'),
    ]
    run = ''.join(f'<li class="stop {st}"><p class="st-d">{d}</p><div class="st-w"><p class="st-c">{escape(c)}</p><p class="st-f">{escape(f)}</p>'
                  f'<p class="st-n">{escape(n)}</p></div><p class="st-s">{B.vk("film", st)}{escape(lab)}</p></li>' for d, c, f, n, st, lab in stops)
    run_photos = [
        {'slug': 'lightbox', 'focus': (0.5, 0.5), 'alt': 'The TIFF Bell Lightbox building in Toronto', 'caption': 'TIFF Bell Lightbox, Toronto, 11 September 2010.'},
        {'slug': 'curzon-mayfair', 'focus': (0.5, 0.45), 'alt': 'The front of the Curzon cinema in Mayfair, London', 'caption': 'Curzon Mayfair, London, June 2023.'},
    ]
    strip = ''.join(f'<figure>{P.plate(p, "ink-film", lpi=80)}<figcaption class="cap">{p["caption"]} {B.credit(p["slug"])}</figcaption></figure>' for p in run_photos if P.has(p['slug']))
    cast = ' · '.join(escape(c['name']) for c in C['cast'] if 'note' not in c)
    crew = C['key_crew']
    billing = (f'<p class="billing big" aria-label="Credits">PalCine Productions presents in co-production with KeyFilm, Red Sea Fund and Metafora Production '
               f'<b>{cast}</b><span>Conversation With the Sea</span>'
               f'written by Muayad Alayan and Rami Alayan · cinematography {escape(crew["cinematography"])} · editing {escape(crew["editing"])} · '
               f'production design {escape(crew["production_design"])} · costume {escape(crew["costume"])} · music {escape(crew["music"])} · '
               f'produced by Muayad Alayan, Rami Alayan, Hanneke Niens, Faycal Hassairi · with the support of the Hubert Bals Fund, the Netherlands Film Fund, '
               f'the Doha Film Institute and Al Ma’mal Foundation for Contemporary Art · world sales MAD World '
               f'<b class="dir">directed by Muayad Alayan</b></p>')
    films = ''
    for w in M['earlier_works'] + [{'title': 'Conversation With the Sea', 'year': 2026, 'type': 'feature', 'festival': 'Venice 2026, Venice Spotlight', 'awards': []}]:
        aw = '; '.join(w['awards']).replace(' (APSA bio; festivals not named)', '').replace(' (Wikipedia)', '')
        films += (f'<li><p class="yr">{w["year"]}</p><div><p class="lg-t"><em>{escape(w["title"])}</em></p><p class="lg-b">{escape(w["type"])}</p></div>'
                  + (f'<p class="lg-p">{escape(aw)}</p>' if aw else '') + f'<p class="lg-f">{escape(w["festival"])}</p></li>')
    second = {'slug': 'rami-alayan', 'focus': (0.62, 0.38), 'zoom': 1.7, 'alt': 'Rami Alayan on stage at the Mostra de València',
              'caption': 'Rami Alayan, co-writer, presenting <em>A House in Jerusalem</em> at the Mostra de València, 21 October 2023.'}
    main = (head
            + '<div class="art-body"><article class="prose-col">'
            '<p class="lede">Kamal is sixty and lives in Jerusalem. An Israeli court orders him to repay a social-security debt said to be owed by his son Wael, who drowned in the Red Sea decades ago, '
            'though no official record of the death can be found. Following the only lead left, Kamal goes looking for what happened, and finds the relatives and friends who have long held a grudge against him.</p>'
            '<p>Muayad Alayan wrote the film with his brother Rami Alayan. He has said the opening incident comes from real events in his family, and that the rest is fiction drawn from life in Jerusalem, '
            'a love-and-hate letter to his home city. Kamel El Basha plays Kamal; Amer Hlehel plays the lawyer friend who helps him.</p>'
            f'{billing}'
            '<h2>The run</h2><p>From its premiere in Venice to the London Palestine Film Festival’s closing night: where the film has been and where it goes next.</p>'
            f'<ol class="run">{run}</ol>'
            f'<div class="run-photos">{strip}</div>'
            '<h2>Muayad Alayan</h2>'
            '<p>A Jerusalem-based director and producer, he co-founded PalCine Productions in Bethlehem with Rami Alayan and is a member of the European Film Academy. '
            'This is his fourth film with MAD World handling sales.</p>'
            f'{P.plate(second, "ink-film in-body", lpi=90)}{P.caption(second)}'
            f'<ol class="ledger films">{films}</ol>'
            '<p class="corr">No corrections to this page.</p>'
            f'{src_list(C["synopsis_sources"] + C["sources"] + M["sources"])}</article>'
            + handbill('Where to see it next', [
                ('Now', '9–18 Oct', 'Warsaw · International Competition', '42nd Warsaw International Film Festival', ''),
                (when('2026-10-30'), '', 'Toronto · The Creative School, Chrysalis Theatre', 'Muslim International Film Festival, opening night', 'with TPFF'),
                ('19–27 Nov', '', 'Doha · International Feature Film Competition', 'Doha Film Festival', 'date to come'),
                (when('2026-11-27'), '', 'London · Curzon Mayfair', 'London Palestine Film Festival, closing film', ''),
            ], '<p class="hb-n">Distribution and a release date have not been announced.</p>')
            + '</div>'
            + related([('festival.html', 'ink-film', 'Boston’s Palestine film festival turns twenty tomorrow', 'The full programme, day by day.', E.CIRCUIT[0]['photo']),
                       ('article.html', 'ink-film', 'Elia Suleiman: all four films, from tonight in Athens', 'The Athens Palestine Film Festival opens with <em>It Must Be Heaven</em>.', E.LEAD['photo']),
                       ('film.html#doha', 'ink-film', 'Four Palestinian films in Doha’s competition', 'Every film’s road to Doha, stop by stop.', E.DOHA['photos'][0])]))
    photos = [lead] + [p for p in run_photos if P.has(p['slug'])] + ([second] if P.has('rami-alayan') else []) + [E.CIRCUIT[0]['photo'], E.LEAD['photo'], E.DOHA['photos'][0]]
    B.page('work.html', 'Conversation With the Sea — VPalestine', 'Muayad Alayan’s Conversation With the Sea: the story, the credits and its festival run from Venice to London.',
           main, 'film.html', photos)


PAGES['work'] = work


# ---------------------------------------------------------------- artist: one musician
def artist():
    A = R['mc_abdul']
    D = A['debut_album']
    lead = {'slug': 'mc-abdul', 'focus': (0.48, 0.30), 'alt': 'MC Abdul on stage with an in-ear monitor, holding a microphone',
            'caption': 'MC Abdul at UNRWA USA’s Gaza 5K, Dallas, 28 September 2024.'}
    item = {'id': 'artist', 'title': 'MC Abdul', 'lines': ['MC Abdul']}
    head = (f'<header class="artist-head p-film"><div class="ah-sleeve ink ink-music">{B.plate(lead, lazy=False, lpi=96)}</div>'
            f'<div class="ah-t ink ink-music p-key">{B.lines(item, "h1", href="#main")}'
            '<p class="stand">His first album, <em>Day by Day, Shway Shway</em>, is out tomorrow: nine tracks, 26 minutes, executive-produced by Suhel Nafar. '
            'On Saturday he plays Palestine Culture Day in Redwood City.</p><p class="byline">Rapper · Gaza to the Bay Area · EMPIRE</p>'
            + B.band([('Born', 'Gaza, 2008'), ('Based', 'San Francisco Bay Area'), ('Label', 'EMPIRE'), ('Album', 'Fri 16 Oct')])
            + f'{B.caption(lead)}</div></header>')
    tracks = ''.join(f'<li><b>{t["no"]}</b><p class="tt"><em>{escape(t["title"])}</em>{("<small>" + escape(t["note"]) + "</small>") if t.get("note") and "KQED" in t["note"] else ""}</p>'
                     f'<p class="tl">{escape(t["length"])}</p></li>' for t in D['tracklist'])
    back = ('<section class="back" aria-labelledby="back-h"><div class="back-t"><h2 id="back-h" class="lines" data-fit><span class="ln">Day by Day</span><span class="ln">Shway Shway</span></h2>'
            '<p class="copy">The back of the sleeve, from the pre-release listing: nine tracks, three of them parts of <em>Is It Real?</em>, which opens, turns and closes the record. '
            '<em>Zanana</em> is named after the Gazan word for the buzz of drones, KQED reports. <em>Wait for Me</em>, the lead single, was co-written with Nai Barghouti.</p>'
            + B.band([('Release', 'Fri 16 Oct 2026'), ('Length', '26 min'), ('Executive producer', 'Suhel Nafar'), ('Label', 'EMPIRE')])
            + f'</div><ol class="tracks">{tracks}</ol></section>')
    singles = A['singles']
    sl = ''
    for s in singles:
        y, m, d = map(int, s['release_date'].split('-'))
        both = False  # every single here is a music release: the red is for film and music together only
        nai = 'Nai Barghouti' in s['credit']
        # one pull of each photograph: Nai Barghouti on her duet, MC Abdul once; the others print type only
        i = len(sl.split('<li')) - 1
        ph = {'slug': 'nai', 'focus': (0.5, 0.35), 'zoom': 1.2, 'alt': ''} if nai and P.has('nai') else ({'slug': 'mc-abdul', 'focus': (0.56, 0.20), 'zoom': 3.0, 'alt': ''} if i == 2 else None)
        sl += (f'<li class="sl1 ink-music{" type-only" if not ph else ""}"><div class="sq ink ink-music">{P.plate(ph, "", lpi=60) if ph else ""}'
               f'<p class="lines" data-fit><span class="ln">{escape(s["title"].split(" - ")[0])}</span></p></div>'
               f'<p class="by">{escape(s["credit"])}</p><p class="dd">{d} {MON[m - 1]} {y}{" · live, not on the album" if "Live" in s["title"] else ""}</p></li>')
    earlier = ''.join(f'<li><p class="yr">{(e.get("release_date") or str(e.get("year")))[:4]}</p><div><p class="lg-t"><em>{escape(e["title"])}</em></p><p class="lg-b">{escape(e["type"])}</p></div>'
                      f'<p class="lg-f">{escape(e.get("note", "")).replace(" (Wikipedia)", "")}</p></li>' for e in A['earlier_releases'])
    story = ('<p class="lede">He was eleven, the story usually goes, when a video of him rapping in English he had taught himself, at his school in Gaza, went around the world. '
             'EMPIRE, the San Francisco label, signed him in 2020; its founder began bringing him to the United States.</p>'
             '<p>His first single, <em>Shouting at the Wall</em>, is dated 30 June 2021 on Apple Music. His first concert was at the FIFA World Cup festivities in Qatar in 2022. '
             'In 2023, after about three years of waiting for permits and a visa, he flew to San Francisco with his father, meaning to stay a month, finish an album and play his first American show: '
             'Palestine Cultural Day in Foster City, on 9 September 2023, which he headlined with Elyanna.</p>'
             '<p>His mother and four younger siblings were still in Gaza. After 7 October, KQED reports, he did not know for five months whether they were alive; his record deal later let him bring them to the United States. '
             'He played Rolling Loud in 2024, billed as its youngest performer and the first Gaza-born artist on its stage.</p>'
             '<p>Tomorrow’s album is his first. He is eighteen.</p>')
    srcs = src_list(A['born_sources'] + A['how_known_sources'] + A['move_to_us']['sources'] if isinstance(A['move_to_us'].get('sources'), list) else A['born_sources'] + A['how_known_sources'])
    main = (head
            + '<div class="art-body"><article class="prose-col">' + story
            + '<h2>Singles from the album, 2026</h2>' + f'<ul class="singles">{sl}</ul>'
            + '<h2>Before the album</h2>' + f'<ol class="ledger films disc">{earlier}</ol>'
            + '<p class="corr">No corrections to this page.</p>' + srcs + '</article>'
            + handbill('Where to hear him', [(when('2026-10-16'), '', 'Everywhere · EMPIRE', '<em>Day by Day, Shway Shway</em>', 'the album'),
                                              (when('2026-10-17'), '', 'Redwood City, California', 'Palestine Culture Day', 'live')],
                       '<p class="hb-n">No other dates for October to December were published by 15 October.</p>')
            + '</div>' + back
            + related([('music.html', 'ink-music', 'Releases, stages and tours', 'Every Palestinian record and concert in this edition.', E.RECORD[1]['photo']),
                       ('calendar.html', 'ink-music', 'What’s on', 'Every film and music date ahead, by city.', E.RECORD[0]['photo']),
                       ('article.html', 'ink-film', 'Elia Suleiman: all four films, from tonight in Athens', 'The Athens Palestine Film Festival opens.', E.LEAD['photo'])]))
    B.page('artist.html', 'MC Abdul — VPalestine', 'MC Abdul, the Gaza-born rapper, and his first album Day by Day, Shway Shway, out 16 October 2026 on EMPIRE.',
           main, 'music.html', [lead, E.RECORD[1]['photo'], E.RECORD[0]['photo'], E.LEAD['photo']])


PAGES['artist'] = artist


# ---------------------------------------------------------------- festival: Boston, the full programme
FEST_PH = {
    'Museum of Fine Arts': {'slug': 'mfa', 'focus': (0.5, 0.5), 'alt': 'The Museum of Fine Arts, Boston, at night', 'caption': 'Museum of Fine Arts, Boston, Huntington Avenue entrance at night, 18 January 2019.'},
    'Coolidge Corner': {'slug': 'coolidge', 'focus': (0.45, 0.30), 'gamma': 1.7, 'alt': 'The Coolidge Corner Theatre marquee at night', 'caption': 'The Coolidge Corner Theatre marquee, Brookline, 15 June 2024.'},
    'Brattle': {'slug': 'brattle', 'focus': (0.5, 0.5), 'alt': 'The Brattle Theatre, Cambridge', 'caption': 'The Brattle Theatre, Cambridge, 19 July 2008.'},
}
FILM_PH = {
    'Edward Said: Between Worlds': {'slug': 'said', 'focus': (0.5, 0.34), 'zoom': 1.3, 'gamma': 0.6, 'alt': 'Edward Said in Seville in 2002', 'caption': 'Edward Said in Seville, 2002.'},
    'Who Killed Alex Odeh?': {'slug': 'odeh-directors', 'focus': (0.5, 0.36), 'alt': 'Jason Osder and William Lafi Youmans holding an award', 'caption': 'Jason Osder and William Lafi Youmans at the Sundance awards, 30 January 2026.'},
    'Chronicles from the Siege': {'slug': 'alkhatib', 'focus': (0.5, 0.3), 'alt': 'Abdallah Al-Khatib at the Berlinale', 'caption': 'Abdallah Al-Khatib at the Berlinale, 3 February 2026.'},
    'Habibi Hussein': {'slug': 'cinema-jenin', 'focus': (0.5, 0.5), 'alt': 'The front of Cinema Jenin', 'caption': 'Cinema Jenin, 11 December 2008, the cinema the film is about.'},
    'With Hasan in Gaza': {'slug': 'aljafari', 'focus': (0.5, 0.3), 'alt': 'Kamal Aljafari on the red carpet at Locarno', 'caption': 'Kamal Aljafari at the Locarno Film Festival, 2025.'},
    "Yesterday the Eye Didn't Sleep": {'slug': 'mayasi', 'focus': (0.5, 0.3), 'alt': 'Rakan Mayasi', 'caption': 'Rakan Mayasi, 22 August 2026.'},
    'Traces of Home': {'slug': 'brattle', 'focus': (0.5, 0.5), 'alt': 'The Brattle Theatre, Cambridge', 'caption': 'The Brattle Theatre, Cambridge, 19 July 2008.'},
    'Palestine Comedy Club': {'slug': 'coolidge', 'focus': (0.45, 0.30), 'gamma': 1.7, 'alt': 'The Coolidge Corner Theatre marquee', 'caption': 'The Coolidge Corner Theatre marquee, Brookline, 15 June 2024.'},
}


def festival():
    F = R['boston_pff']
    sc = F['screenings']
    tickets = {}
    for t in F['ticket_prices']:
        for k in ('Coolidge', 'MassArt', 'MFA', 'Brattle', 'afterpart'):
            if k in t['what']:
                tickets[k] = t
    def price(venue, title):
        if 'afterparty' in title.lower():
            return 'Free, no ticket'
        if 'MassArt' in venue or 'Howard Thurman' in venue or 'UMass' in venue:
            return 'Free, register'
        if 'Coolidge' in venue:
            return '$18'
        return 'Price not listed'
    lead_ph = FEST_PH['Coolidge Corner']
    item = {'id': 'festival', 'title': 'Boston Palestine Film Festival, 20th edition', 'lines': ['Boston', 'Palestine Film', 'Festival']}
    head = (f'<header class="fest-head ink ink-film p-film"><div class="fh-t p-key">'
            f'{B.lines(item, "h1", href="#main")}'
            '<p class="stand">Ten days, seven venues, from the sold-out opening of <em>Edward Said: Between Worlds</em> at the Museum of Fine Arts tomorrow to <em>Palestine Comedy Club</em> at the Coolidge Corner Theatre on the 25th.</p>'
            '<p class="byline">20th edition · since 2007 · 16–25 October 2026</p>'
            + B.band([('Opens', 'Fri 16 Oct, 19:00, MFA'), ('Closes', 'Sun 25 Oct, 16:30, Coolidge'), ('Tickets', '$18 at the Coolidge; MassArt, BU and UMass free')])
            + f'</div>{B.plate(lead_ph, lazy=False, lpi=90)}<div class="fh-cap p-key">{B.caption(lead_ph)}</div></header>')
    # the programme, day by day: a column per day like a festival brochure
    days = {}
    for s in sc:
        days.setdefault(s['date'], []).append(s)
    cols = ''
    for iso in sorted(days):
        items = ''
        for s in days[iso]:
            ph = FILM_PH.get(s['title'].replace(' (second screening)', ''))
            is_event = s.get('type') == 'Special event'
            sold = 'SOLD OUT' in (s.get('notes') or '')
            pl = P.plate(ph, 'ink-film th-big', lpi=48) if ph and not is_event else ''
            meta = ' · '.join(x for x in (s.get('director'), f'{s["runtime_min"]}′' if s.get('runtime_min') else '', s.get('type') if not s.get('director') else '') if x)
            note = (s.get('notes') or '').replace(' SOLD OUT (listed as such on 15 Oct).', '').replace('SOLD OUT (listed as such on 15 Oct).', '')
            note = re.sub(r' \((MFA|Mirage|TPFF|APFF26|Wikipedia|Tirana IFF)\)', '', note)
            films = ''
            if s.get('films'):
                films = '<ul class="shorts">' + ''.join(f'<li><em>{escape(f["title"])}</em> {escape(f["director"])}, {f["runtime_min"]}′</li>' for f in s['films']) + '</ul>'
            items += (f'<li class="slot{" ev" if is_event else ""}{" sold" if sold else ""}{"" if pl else " no-th"}">{pl}<p class="sl-t">{escape(s["time"])}{("–" + escape(s["end_time"])) if s.get("end_time") else ""}'
                      f'<span>{escape(s["venue"].replace("Museum of Fine Arts, Boston", "MFA Boston"))}</span></p>'
                      f'<h3 class="sl-h"><em>{escape(s["title"])}</em></h3><p class="sl-m">{escape(meta)}</p>{films}'
                      f'<p class="sl-n">{escape(note)}</p>'
                      f'<p class="sl-p{" sold" if sold else (" due" if price(s["venue"], s["title"]) == "Price not listed" else "")}"><span>Tickets</span>{"Sold out" if sold else escape(price(s["venue"], s["title"]))}</p></li>')
        few = ' class="few"' if len(days[iso]) <= 2 else ''
        cols += f'<section class="pday" aria-label="{when(iso)}"><h2>{when(iso).split(" ")[0]} <b>{int(iso[8:])}</b></h2><ol{few}>{items}</ol></section>'
    venues = ''
    for v in F['venues']:
        key = next((k for k in FEST_PH if k in v['name']), None)
        ph = FEST_PH.get(key) if key else None
        pl = P.plate(ph, 'ink-film', lpi=60) if ph else ''
        venues += (f'<li{"" if pl else " class=text-only"}>{pl}<p class="vn">{escape(v["name"].split(", Isenberg")[0])}</p><p class="va">{escape(v["address"]).replace(" (the festival site prints &#x27;Brookline MA&#x27;)", "")}</p>'
                   f'{("<p class=vu>" + escape(v["use"]) + "</p>") if v.get("use") else ""}</li>')
    main = (head
            + f'<section class="sec first" aria-labelledby="prog-h"><div class="head"><h2 id="prog-h">The programme</h2><p>Every screening and event, in Boston time. '
            f'A sold-out screening keeps its slot in outline.</p></div><div class="prog">{cols}</div></section>'
            + f'<section class="sec" aria-labelledby="ven-h"><div class="head"><h2 id="ven-h">Seven venues</h2><p>From Huntington Avenue to Amherst.</p></div><ul class="venue-grid">{venues}</ul></section>'
            + '<section class="sec" aria-labelledby="tix-h"><div class="head"><h2 id="tix-h">Tickets</h2><p>As the festival and its ticketing pages list them on 15 October.</p></div>'
            '<dl class="band tix"><div><dt>Coolidge Corner Theatre</dt><dd>$18 general admission</dd></div><div><dt>MassArt, BU, UMass Amherst</dt><dd>Free, registration required</dd></div>'
            '<div><dt>Opening and closing parties</dt><dd>Free, no ticket</dd></div><div><dt>MFA and Brattle</dt><dd>Price not published</dd></div></dl></section>'
            + '<div class="art-body"><div class="prose-col">' + src_list(F['sources']) + '</div></div>'
            + related([('article.html', 'ink-film', 'Elia Suleiman: all four films, from tonight in Athens', 'The other festival opening this week.', E.LEAD['photo']),
                       ('work.html', 'ink-film', 'Conversation With the Sea, from Venice to Doha', 'One film’s life, stop by stop.', E.DOHA['photos'][1]),
                       ('calendar.html', 'ink-music', 'What’s on', 'Every film and music date ahead.', E.SLEEVE['photo'])]))
    photos = [lead_ph] + [p for p in list(FILM_PH.values()) + list(FEST_PH.values()) if P.has(p['slug'])] + [E.LEAD['photo'], E.DOHA['photos'][1], E.SLEEVE['photo']]
    B.page('festival.html', 'Boston Palestine Film Festival 2026 — VPalestine',
           'The 20th Boston Palestine Film Festival, 16–25 October 2026: every screening, venue and ticket price.', main, 'festival.html', photos)


PAGES['festival'] = festival
