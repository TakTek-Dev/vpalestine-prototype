"""Every dated event the edition knows about, as of Thursday 15 October 2026 (sources: research/news.json ids).

start/end: ISO dates (end only for runs); time: local time when the source gives one; city/venue as listed.
desk: film | music | both; state: on (confirmed) | due (expected, or details not yet published) | gone (passed or moved).
kind: screening | festival | release | concert | award | tribute
link: the page that carries the work or event in this prototype.
"""

EVENTS = [
    # Thursday 15
    dict(start='2026-10-15', time='20:00', city='Jerusalem', venue='Yabous Cultural Centre', what='Jerusalem Festival final night: Irth and Iliya dabke troupes', desk='music', state='on', kind='festival', link='music.html#jerusalem', src='jerusalem-festival-closes'),
    dict(start='2026-10-15', end='2026-10-23', time='', city='El Gouna', venue='El Gouna Film Festival', what='El Gouna Film Festival opens; <em>Who Killed Alex Odeh?</em> in the line-up', desk='film', state='on', kind='festival', link='film.html#el-gouna', src='elgouna-2026-opens'),
    dict(start='2026-10-15', time='20:00', city='Athens', venue='Trianon Cinema', what='<em>It Must Be Heaven</em> opens the Athens Palestine Film Festival', desk='film', state='on', kind='screening', link='article.html', src='athens-pff-2026-opens'),
    # Friday 16
    dict(start='2026-10-16', time='', city='Boston', venue='Museum of Fine Arts', what='<em>Edward Said: Between Worlds</em> opens the 20th Boston Palestine Film Festival (sold out)', desk='film', state='on', kind='screening', link='festival.html', src='boston-pff-2026'),
    dict(start='2026-10-16', time='21:00', city='Athens', venue='Trianon Cinema', what='Elia Suleiman, <em>The Time That Remains</em>, followed by a Q&amp;A with Suleiman', desk='film', state='on', kind='screening', link='article.html', src='suleiman-athens-retrospective'),
    dict(start='2026-10-16', time='', city='Everywhere', venue='EMPIRE', what='MC Abdul, <em>Day by Day, Shway Shway</em>, debut album', desk='music', state='due', kind='release', link='artist.html', src='mc-abdul-debut-album'),
    # weekend
    dict(start='2026-10-17', time='', city='Redwood City', venue='Palestine Culture Day', what='MC Abdul live', desk='music', state='on', kind='concert', link='artist.html', src='mc-abdul-debut-album'),
    dict(start='2026-10-17', time='18:30', city='Athens', venue='Trianon Cinema', what='<em>Palescope 2: The Way Home</em>, six shorts', desk='film', state='on', kind='screening', link='article.html', src='athens-pff-2026-opens'),
    dict(start='2026-10-24', time='21:00', city='Athens', venue='Trianon Cinema', what='Saverio Costanzo’s <em>Private</em>, a night for Mohammad Bakri with his family present', desk='film', state='on', kind='tribute', link='film.html#reissue', src='bakri-tributes'),
    dict(start='2026-10-18', time='', city='Boston', venue='Museum of Fine Arts', what='<em>Who Killed Alex Odeh?</em>', desk='film', state='on', kind='screening', link='festival.html', src='boston-pff-2026'),
    dict(start='2026-10-18', time='21:00', city='Athens', venue='Trianon Cinema', what='Elia Suleiman, <em>Divine Intervention</em>', desk='film', state='on', kind='screening', link='article.html', src='suleiman-athens-retrospective'),
    dict(start='2026-10-18', time='', city='London', venue='BFI London Film Festival', what='London Film Festival awards; <em>Concrete Land</em> in the Documentary Competition', desk='film', state='due', kind='award', link='film.html#lff', src='lff-2026-palestinian-titles'),
    dict(start='2026-10-19', time='', city='Brookline', venue='Coolidge Corner Theatre', what='Kamal Aljafari, <em>With Hasan in Gaza</em>', desk='film', state='on', kind='screening', link='festival.html', src='boston-pff-2026'),
    dict(start='2026-10-20', time='', city='Cambridge', venue='Brattle Theatre', what='<em>Traces of Home</em>', desk='film', state='on', kind='screening', link='festival.html', src='boston-pff-2026'),
    dict(start='2026-10-22', end='2026-10-25', time='', city='Washington', venue='Angelika Pop-Up, Union Market', what='DC Palestinian Film and Arts Festival, 15th year; titles not yet published', desk='film', state='due', kind='festival', link='film.html#dc', src='dc-pfaf-2026'),
    dict(start='2026-10-23', time='', city='Boston', venue='Museum of Fine Arts', what='<em>Chronicles from the Siege</em>', desk='film', state='on', kind='screening', link='festival.html', src='chronicles-from-the-siege'),
    dict(start='2026-10-23', time='19:00', city='Athens', venue='Trianon Cinema', what='<em>Habibi Hussein</em>, about Cinema Jenin’s last projectionist', desk='film', state='on', kind='screening', link='film.html#reissue', src='habibi-hussein-jenin'),
    dict(start='2026-10-24', time='', city='Brookline', venue='Coolidge Corner Theatre', what='<em>Habibi Hussein</em> and <em>Yesterday the Eye Didn’t Sleep</em>', desk='film', state='on', kind='screening', link='festival.html', src='boston-pff-2026'),
    dict(start='2026-10-24', time='19:00', city='Athens', venue='Trianon Cinema', what='<em>Who Killed Alex Odeh?</em>', desk='film', state='on', kind='screening', link='film.html#el-gouna', src='athens-pff-2026-opens'),
    dict(start='2026-10-24', time='', city='Edmonton', venue='Horowitz Theatre', what='Faraj Suleiman, <em>Faraj, Piano and Mic</em>, his first fully solo show', desk='music', state='on', kind='concert', link='music.html#faraj', src='faraj-suleiman-solo'),
    dict(start='2026-10-25', time='', city='Brookline', venue='Coolidge Corner Theatre', what='<em>Palestine Comedy Club</em> closes the Boston Palestine Film Festival', desk='film', state='on', kind='screening', link='festival.html', src='boston-pff-2026'),
    dict(start='2026-10-25', time='20:00', city='Athens', venue='Trianon Cinema', what='<em>Mohammad Bakri: A Cultural Legacy</em>, with Rashid Masharawi’s <em>Haifa</em>', desk='film', state='on', kind='tribute', link='film.html#reissue', src='bakri-tributes'),
    dict(start='2026-10-25', time='19:30', city='Hong Kong', venue='Shaw Auditorium, HKUST', what='Nai Barghouti, <em>Music of Palestine</em>', desk='music', state='on', kind='concert', link='music.html#nai', src='nai-barghouti-hong-kong'),
    dict(start='2026-10-29', end='2026-10-30', time='20:00', city='Athens', venue='Onassis Stegi', what='Larissa Sansour and Søren Lind, <em>A Sunken Tale of Losses Delayed</em>', desk='film', state='on', kind='screening', link='article.html', src='athens-pff-2026-opens'),
    dict(start='2026-10-29', end='2026-10-31', time='', city='Valladolid', venue='Seminci, Meeting Point', what='<em>Yesterday the Eye Didn’t Sleep</em>', desk='film', state='on', kind='screening', link='film.html#rome', src='rome-ff-yesterday-eye'),
    dict(start='2026-10-30', time='', city='New York', venue='Quad Cinema; also Laemmle Glendale and Uprising Theater, Chicago', what='<em>Who Killed Alex Odeh?</em> opens in US cinemas', desk='film', state='on', kind='release', link='film.html#el-gouna', src='who-killed-alex-odeh-release'),
    dict(start='2026-10-31', time='20:00', city='Athens', venue='Onassis Stegi', what='Elia Suleiman, <em>Chronicle of a Disappearance</em> closes the run', desk='film', state='on', kind='screening', link='article.html', src='suleiman-athens-retrospective'),
    # November
    dict(start='2026-11-05', end='2026-11-10', time='', city='Santa Ana', venue='The Frida Cinema', what='<em>Who Killed Alex Odeh?</em>, in the city where the bombing happened', desk='film', state='on', kind='release', link='film.html#el-gouna', src='who-killed-alex-odeh-release'),
    dict(start='2026-11-11', end='2026-11-20', time='', city='Cairo', venue='Cairo International Film Festival, 47th', what='Cairo International Film Festival; Palestinian titles not yet named', desk='film', state='due', kind='festival', link='film.html', src='cairo-iff-2026'),
    dict(start='2026-11-13', time='', city='London', venue='Barbican', what='<em>Who Is Still Alive</em> opens the London Palestine Film Festival', desk='film', state='on', kind='screening', link='film.html#oscars', src='who-is-still-alive-swiss-oscar'),
    dict(start='2026-11-14', time='', city='London', venue='ICA', what='<em>Who Killed Alex Odeh?</em>, UK premiere', desk='film', state='on', kind='screening', link='film.html#el-gouna', src='lpff-2026'),
    dict(start='2026-11-14', time='', city='Berlin', venue='Festsaal Kreuzberg', what='Rasha Nahas', desk='music', state='on', kind='concert', link='music.html#rasha-nahas', src='rasha-nahas-manaqish'),
    dict(start='2026-11-15', time='', city='London', venue='Ciné Lumière', what='<em>Edward Said: Between Worlds</em>, with Maiken Baird', desk='film', state='on', kind='screening', link='festival.html', src='edward-said-between-worlds'),
    dict(start='2026-11-16', time='', city='London', venue='Barbican', what='<em>From Ground Zero+</em>: five shorts from Gaza', desk='film', state='on', kind='screening', link='film.html', src='gaza-shorts-lpff'),
    dict(start='2026-11-18', time='', city='London', venue='Barbican', what='<em>Habibi Hussein</em>, with a ScreenTalk', desk='film', state='on', kind='screening', link='film.html#reissue', src='habibi-hussein-jenin'),
    dict(start='2026-11-19', time='', city='London', venue='Rio Cinema', what='<em>A Life in Cinema: A Tribute to Mohammad Bakri</em>, with Saleh Bakri', desk='film', state='on', kind='tribute', link='film.html#reissue', src='bakri-tributes'),
    dict(start='2026-11-19', end='2026-11-27', time='', city='Doha', venue='Doha Film Festival', what='Doha Film Festival: four Palestinian films in competition', desk='film', state='on', kind='festival', link='work.html', src='doha-ff-2026-competition'),
    dict(start='2026-11-26', time='', city='London', venue='Bertha DocHouse', what='<em>Concrete Land</em>', desk='film', state='on', kind='screening', link='film.html#lff', src='concrete-land'),
    dict(start='2026-11-27', time='', city='London', venue='Curzon Mayfair', what='<em>Conversation With the Sea</em> closes the London Palestine Film Festival', desk='film', state='on', kind='screening', link='work.html', src='conversation-with-the-sea'),
    # December and after
    dict(start='2026-12-15', time='', city='Los Angeles', venue='Academy of Motion Picture Arts and Sciences', what='Oscar shortlist: <em>Citizen Osama</em> for Palestine, <em>Who Is Still Alive</em> for Switzerland', desk='film', state='due', kind='award', link='film.html#oscars', src='citizen-osama-oscar'),
    dict(start='2026-12-19', time='', city='Dubai', venue='Dopa World', what='Saint Levant', desk='music', state='on', kind='concert', link='music.html#saint-levant', src='saint-levant-tour-postponed'),
    dict(start='2027-01-21', time='', city='Los Angeles', venue='Academy of Motion Picture Arts and Sciences', what='Oscar nominations', desk='film', state='due', kind='award', link='film.html#oscars', src='citizen-osama-oscar'),
    dict(start='2027-01-23', time='', city='London', venue='Barbican', what='Faraj Suleiman leads a 20-piece ensemble in a Ziad Rahbani tribute', desk='music', state='on', kind='concert', link='music.html#faraj', src='faraj-suleiman-solo'),
    dict(start='2027-03-14', time='', city='Los Angeles', venue='99th Academy Awards', what='Oscar ceremony', desk='film', state='due', kind='award', link='film.html#oscars', src='citizen-osama-oscar'),
    dict(start='2027-03-19', time='', city='Ottawa', venue='Afandi World Tour, North America', what='Saint Levant’s North American leg opens; Boston on 27 March is the first US date', desk='music', state='on', kind='concert', link='music.html#saint-levant', src='saint-levant-tour-postponed'),
    # undated
    dict(start='', time='', city='New York', venue='Venue not announced', what='Together for Palestine, New York benefit concert', desk='music', state='due', kind='concert', link='music.html', src='together-for-palestine-ny'),
    dict(start='', time='', city='Everywhere', venue='Produced by Meshell Ndegeocello', what='Rasha Nahas, third album', desk='music', state='due', kind='release', link='music.html#rasha-nahas', src='rasha-nahas-manaqish'),
]


# a photograph for each event where we have an honest one: the person, the work's maker, or the venue
PH = [
    ('opens in US cinemas', 'quad'), ('UK premiere', 'ica2'), ('Bertha DocHouse', 'bertha'), ('Ciné Lumière', 'said'),
    ('Who Is Still Alive', 'barbican-cinema'), ('in the city where the bombing happened', 'frida'),
    ('Jerusalem Festival', 'damascus-gate'), ('It Must Be Heaven', 'suleiman'),
    ('Edward Said', 'said'), ('The Time That Remains', 'suleiman'), ('Divine Intervention', 'suleiman'),
    ('Chronicle of a Disappearance', 'suleiman'), ('Day by Day', 'mc-abdul'), ('MC Abdul live', 'mc-abdul'),
    ('Who Killed Alex Odeh?', 'odeh-directors'), ('With Hasan in Gaza', 'aljafari'), ('Traces of Home', 'brattle'),
    ('Chronicles from the Siege', 'alkhatib'), ('Habibi Hussein', 'cinema-jenin'), ('Faraj Suleiman', 'faraj'),
    ('Palestine Comedy Club', 'coolidge'), ('A Life in Cinema', 'saleh-bakri'), ('Bakri', 'bakri'), ('Saint Levant', 'saint-levant-live'),
    ('Rasha Nahas', 'rasha-nahas'), ('Conversation With the Sea', 'curzon-mayfair'), ('Nai Barghouti', 'nai'),
    ('A Sunken Tale', 'onassis'), ('Seminci', 'calderon'), ('Yesterday the Eye', 'mayasi'), ('Cairo International', 'cairo-opera'),
    ('Doha Film Festival', 'doha'), ('London Film Festival awards', 'bfi'), ('Concrete Land', 'bfi'), ('DC Palestinian', 'union-market'),
    ('Together for Palestine', 'wembley'), ('Palescope', 'trianon'), ('From Ground Zero', 'barbican-cinema'),
]
ALT = {
    'quad': 'The Quad Cinema on West 13th Street, New York', 'wadimoff': 'Nicolas Wadimoff', 'frida': 'The Frida Cinema, Santa Ana',
    'damascus-gate': 'Damascus Gate, Jerusalem', 'elgouna': 'The marina at El Gouna, Egypt', 'suleiman': 'Elia Suleiman',
    'said': 'Edward Said in Seville, 2002', 'ica2': 'The ICA on the Mall, London', 'bertha': 'The Brunswick Centre, Bloomsbury, home of Bertha DocHouse',
    'onassis': 'The main stage of Onassis Stegi, Athens', 'saint-levant-live': 'Saint Levant performing at Melbourne Town Hall', 'mc-abdul': 'MC Abdul on stage', 'odeh-directors': 'Jason Osder and William Lafi Youmans',
    'aljafari': 'Kamal Aljafari', 'brattle': 'The Brattle Theatre, Cambridge', 'alkhatib': 'Abdallah Al-Khatib', 'cinema-jenin': 'Cinema Jenin',
    'faraj': 'Faraj Suleiman at the piano', 'coolidge': 'The Coolidge Corner Theatre marquee', 'saleh-bakri': 'Saleh Bakri', 'bakri': 'Mohammad Bakri',
    'saint-levant': 'Saint Levant singing', 'rasha-nahas': 'Rasha Nahas with a guitar', 'curzon-mayfair': 'Curzon Mayfair, London',
    'nai': 'Nai Barghouti', 'sansour': 'Larissa Sansour', 'calderon': 'Teatro Calderón, Valladolid', 'mayasi': 'Rakan Mayasi',
    'cairo-opera': 'The Cairo Opera House', 'doha': 'Doha', 'bfi': 'BFI Southbank, London', 'union-market': 'Union Market, Washington',
    'wembley': 'OVO Arena Wembley, London', 'trianon': 'The Trianon cinema, Athens', 'barbican-cinema': 'The Barbican Centre, London',
}
# the homepage's Coming attractions: festivals, releases, concerts, awards, tributes, and these screenings
HOME_SCREENINGS = ('Habibi Hussein</em>, about', 'Seminci', 'Who Is Still Alive', 'closes the London', 'A Life in Cinema', 'opens in US cinemas')

VENUE_CROP = {'quad': ((0.5, 0.35), 2.2), 'brattle': ((0.5, 0.45), 2.0), 'coolidge': ((0.45, 0.3), 2.0), 'curzon-mayfair': ((0.5, 0.4), 2.0),
              'cinema-jenin': ((0.5, 0.5), 1.6), 'damascus-gate': ((0.52, 0.4), 2.0), 'onassis': ((0.5, 0.5), 2.0), 'bfi': ((0.55, 0.5), 2.0),
              'ica2': ((0.5, 0.45), 2.0), 'bertha': ((0.5, 0.5), 2.0), 'barbican-cinema': ((0.5, 0.5), 2.0), 'riverside': ((0.5, 0.45), 2.0)}
PEOPLE = {'suleiman', 'mc-abdul', 'odeh-directors', 'aljafari', 'alkhatib', 'faraj', 'saleh-bakri', 'bakri', 'saint-levant-live', 'rasha-nahas', 'nai', 'mayasi', 'said', 'wadimoff', 'sansour'}

for _e in EVENTS:
    for key, slug in PH:
        if key in _e['what'] or key in _e['venue']:
            person = slug in PEOPLE
            _e['photo'] = {'slug': slug, 'focus': (0.5, 0.3) if person else (0.5, 0.5), 'alt': ALT.get(slug, ''), 'caption': ALT.get(slug, '') + '.'}
            if person:
                _e['photo']['zoom'] = 1.6
            elif slug in VENUE_CROP:
                _e['photo']['focus'], _e['photo']['zoom'] = VENUE_CROP[slug]
            break
    _e['home'] = _e['kind'] != 'screening' or any(k in _e['what'] or k in _e['venue'] for k in HOME_SCREENINGS)
