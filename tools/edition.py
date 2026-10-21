"""The edition of Thursday 15 October 2026, rebuilt from research/news.json (sources resolved at build time).

desk:  film | music | both     -> which screen prints it (yellow, fuchsia, the overprint)
state: on | due | gone          -> ink density: solid, halftone tint, outline
Work titles are wrapped in <em>. Poster lines ("lines") are how a title is broken on its sheet;
each line is set to the sheet's measure by the width axis (assets/js/vp.js, fitLines).
"""

DATE = '2026-10-15'
DATELINE = 'Thursday 15 October 2026'

LEAD = {
    'id': 'suleiman-athens', 'desk': 'film', 'state': 'on',
    'title': 'Elia Suleiman: all four films, from tonight in Athens',
    'lines': ['Elia Suleiman,', 'all four films,', 'from tonight'],
    'deck': 'The Athens Palestine Film Festival opens at the Trianon at 20:00 with <em>It Must Be Heaven</em> (2019). '
            '<em>The Time That Remains</em> follows on Friday and <em>Divine Intervention</em> on Sunday; '
            '<em>Chronicle of a Disappearance</em> (1996) closes the run at Onassis Stegi on 31 October.',
    'band': [('Opens', 'Thu 15 Oct, 20:00 Athens time'), ('Where', 'Trianon Cinema, Athens'), ('Runs', '15–31 Oct · Trianon, EMST, Onassis Stegi')],
    'photo': {'slug': 'suleiman', 'focus': (0.64, 0.29), 'zoom': 2.6,
              'alt': 'Elia Suleiman, in a hat and dark suit, holding a framed award on a stage beside its presenter',
              'caption': 'Elia Suleiman receives the Honorary Heart of Sarajevo at the Sarajevo Film Festival, 2024.'},
    'src': ['athens-pff-2026-opens', 'suleiman-athens-retrospective'],
}

SLEEVE = {
    'id': 'mc-abdul', 'desk': 'music', 'state': 'due',
    'title': 'MC Abdul’s first album is out tomorrow',
    'lines': ['Day by Day,', 'Shway Shway'],
    'text': 'Nine tracks on EMPIRE, executive-produced by Suhel Nafar. The Gaza-born rapper, 18 and now in the Bay Area, '
            'plays Palestine Culture Day in Redwood City on Saturday.',
    'band': [('Out', 'Fri 16 Oct'), ('Label', 'EMPIRE')],
    'photo': {'slug': 'mc-abdul', 'focus': (0.48, 0.30),
              'alt': 'MC Abdul on stage with an in-ear monitor, holding a microphone',
              'caption': 'MC Abdul at UNRWA USA’s Gaza 5K, Dallas, 28 September 2024.'},
    'src': ['mc-abdul-debut-album'],
}

# This week, in local time. day, time, place, what (HTML), desk, state, note
BILL = [
    ('Thu 15', '20:00', 'Jerusalem', 'Jerusalem Festival final night: a dabke double bill', 'music', 'on', 'Yabous Cultural Centre'),
    ('Thu 15', 'opening', 'El Gouna', 'El Gouna Film Festival opens; <em>Who Killed Alex Odeh?</em> is in the line-up', 'film', 'on', 'to 23 Oct'),
    ('Thu 15', '20:00', 'Athens', '<em>It Must Be Heaven</em> opens the Athens Palestine Film Festival', 'film', 'on', 'Trianon'),
    ('Fri 16', 'opening', 'Boston', '<em>Edward Said: Between Worlds</em> opens the 20th Boston Palestine Film Festival', 'film', 'on', 'MFA · sold out'),
    ('Fri 16', 'release', 'everywhere', 'MC Abdul, <em>Day by Day, Shway Shway</em>', 'music', 'due', 'EMPIRE'),
    ('Sat 17', 'live', 'Redwood City', 'MC Abdul at Palestine Culture Day', 'music', 'on', 'California'),
    ('Sun 18', '', 'Boston', '<em>Who Killed Alex Odeh?</em>', 'film', 'on', 'MFA'),
    ('Sun 18', 'awards', 'London', 'London Film Festival winners; <em>Concrete Land</em> is in the Documentary Competition', 'film', 'due', 'result due'),
]

# Where the films are playing this week
CIRCUIT = [
    {'id': 'boston', 'desk': 'film', 'state': 'on', 'fmt': 'half',
     'title': 'Boston’s Palestine film festival turns twenty tomorrow',
     'lines': ['Boston', 'turns twenty'],
     'text': 'The 20th edition opens at the Museum of Fine Arts with Maiken Baird’s <em>Edward Said: Between Worlds</em>, '
             'already sold out, and closes on 25 October at the Coolidge Corner Theatre with <em>Palestine Comedy Club</em>.',
     'list': [('18 Oct', '<em>Who Killed Alex Odeh?</em>', 'MFA'),
              ('19 Oct', 'Kamal Aljafari, <em>With Hasan in Gaza</em>', 'Coolidge'),
              ('20 Oct', '<em>Traces of Home</em>', 'Brattle'),
              ('23 Oct', '<em>Chronicles from the Siege</em>', 'MFA'),
              ('24 Oct', '<em>Habibi Hussein</em>, <em>Yesterday the Eye Didn’t Sleep</em>', 'Coolidge'),
              ('25 Oct', '<em>Palestine Comedy Club</em>, closing night', 'Coolidge')],
     'band': [('Runs', '16–25 Oct'), ('Venues', 'MFA · Coolidge Corner · Brattle · UMass Amherst'), ('Tickets', '$18')],
     'photo': {'slug': 'coolidge', 'focus': (0.45, 0.30), 'gamma': 1.7,
               'alt': 'The lit vertical sign and marquee of the Coolidge Corner Theatre at night',
               'caption': 'The Coolidge Corner Theatre marquee, Brookline, 15 June 2024.'},
     'src': ['boston-pff-2026', 'edward-said-between-worlds']},
    {'id': 'el-gouna', 'desk': 'film', 'state': 'on', 'fmt': 'window',
     'title': 'El Gouna opens today, with the Alex Odeh case in its line-up',
     'lines': ['El Gouna', 'opens today'],
     'text': 'The ninth El Gouna Film Festival opens with Marc Fitoussi’s <em>All About Corinne</em> and runs to 23 October. '
             'The tenth title it announced was <em>Who Killed Alex Odeh?</em>, Jason Osder and William Lafi Youmans’s '
             're-investigation of the 1985 bombing in Santa Ana that killed the Palestinian-American activist. '
             'Watermelon Pictures opens it in US cinemas on 30 October.',
     'band': [('Runs', '15–23 Oct'), ('Where', 'El Gouna, Egypt')],
     'photo': {'slug': 'odeh-directors', 'focus': (0.5, 0.36),
               'alt': 'Jason Osder and William Lafi Youmans holding an award in front of a Sundance backdrop',
               'caption': 'Jason Osder and William Lafi Youmans at the Sundance awards, 30 January 2026.'},
     'src': ['elgouna-2026-opens', 'who-killed-alex-odeh-release']},
    {'id': 'lff', 'desk': 'film', 'state': 'due', 'fmt': 'lobby',
     'title': 'Sunday, London names its documentary winner. Concrete Land is in the running.',
     'lines': ['London,', 'Sunday'],
     'text': 'Asmahan Bkerat’s debut follows the Al-Najjar family as an eviction notice, new construction and hostile neighbours '
             'push them and their animals off their land in Jordan. It is in the BFI London Film Festival’s Documentary Competition; '
             'Abdallah Al-Khatib’s <em>Chronicles from the Siege</em> plays in the Dare strand.',
     'band': [('Awards', 'Sun 18 Oct'), ('Festival', '70th BFI London Film Festival')],
     'photo': {'slug': 'ica', 'focus': (0.5, 0.45), 'alt': 'The entrance of the Institute of Contemporary Arts on the Mall, London',
               'caption': 'The ICA on the Mall, London, 14 January 2006, where the festival showed <em>Revolutionaries Never Die</em> on 12 October.'},
     'src': ['lff-2026-palestinian-titles', 'concrete-land']},
    {'id': 'siege', 'desk': 'film', 'state': 'on', 'fmt': 'lobby',
     'title': 'Chronicles from the Siege, from Berlin to Boston',
     'lines': ['Yarmouk'],
     'text': 'Abdallah Al-Khatib’s Berlinale best-first-feature winner draws on his years in Yarmouk camp. '
             'After closing Toronto’s festival and playing London, it screens at the MFA on 23 October.',
     'band': [('Boston', 'Fri 23 Oct, MFA')],
     'photo': {'slug': 'alkhatib', 'focus': (0.5, 0.3),
               'alt': 'Abdallah Al-Khatib, curly-haired, in a black-and-white keffiyeh, at the Berlinale',
               'caption': 'Abdallah Al-Khatib at the Berlinale, 3 February 2026.'},
     'src': ['chronicles-from-the-siege']},
    {'id': 'rome', 'desk': 'film', 'state': 'on', 'fmt': 'lobby',
     'title': 'Yesterday the Eye Didn’t Sleep competes in Rome',
     'lines': ['Rome'],
     'text': 'Rakan Mayasi’s debut, first shown in Cannes’ Un Certain Regard, is one of 18 films in Rome’s Progressive Cinema '
             'competition. Then Valladolid’s Seminci, 29 to 31 October.',
     'band': [('Rome', '13–25 Oct'), ('Runtime', '101′')],
     'photo': {'slug': 'mayasi', 'focus': (0.5, 0.3), 'alt': 'Rakan Mayasi', 'caption': 'Rakan Mayasi, 22 August 2026.'},
     'src': ['rome-ff-yesterday-eye']},
    {'id': 'dc', 'desk': 'film', 'state': 'due', 'fmt': 'strip',
     'title': 'Washington’s festival turns fifteen next week',
     'lines': ['Washington'],
     'text': 'The volunteer-run DC Palestinian Film and Arts Festival screens 22 to 25 October at the Angelika Pop-Up at Union Market. '
             'Its titles are not yet published.',
     'band': [('Runs', '22–25 Oct'), ('Titles', 'to come')],
     'src': ['dc-pfaf-2026']},
]

DOHA = {
    'id': 'doha', 'desk': 'film', 'state': 'on',
    'title': 'Four Palestinian films in Doha’s competition',
    'lines': ['Four films,', 'one competition'],
    'text': 'The Doha Film Festival named its 15-film international competition on 8 October; eleven are Doha Film Institute grantees. '
            'Arab News confirms two Palestinian titles. Trade listings add two more, printed here in tint until the festival’s own page lists them.',
    'films': [
        {'title': 'Thirteen in Gaza', 'by': 'Hosam Abu Dan', 'rt': '77′', 'state': 'on',
         'road': [('Toronto', 'NETPAC Award'), ('Buffalo', '12 Oct'), ('Doha', 'MENA premiere')]},
        {'title': 'Conversation With the Sea', 'by': 'Muayad Alayan', 'rt': '112′', 'state': 'on',
         'road': [('Venice', '7 Sep'), ('Toronto', 'Centerpiece'), ('Doha', 'MENA premiere'), ('London', '27 Nov, closing film')]},
        {'title': 'Revolutionaries Never Die', 'by': 'Mohanad Yaqubi', 'rt': '80′', 'state': 'due',
         'road': [('Locarno', 'Special Jury Prize'), ('London', 'ICA, 12 Oct'), ('Doha', 'per trade listings')]},
        {'title': 'Sama', 'by': 'Rabab Khamis', 'rt': '', 'state': 'due',
         'road': [('Doha', 'world premiere, per trade listings')]},
    ],
    'band': [('Doha', '19–27 Nov'), ('Best narrative', 'US$75,000'), ('Best documentary', 'US$50,000')],
    'photos': [
        {'slug': 'gaza-port', 'focus': (0.5, 0.55),
         'alt': 'Gaza’s seaport at dusk, boats below a cloudy sky and the harbour memorial in silhouette',
         'caption': 'Gaza seaport, 7 October 2017. Not a still from <em>Thirteen in Gaza</em>.'},
        {'slug': 'el-basha', 'focus': (0.30, 0.42), 'zoom': 1.5,
         'alt': 'Kamel El Basha seated before a lit dressing-room mirror',
         'caption': 'Kamel El Basha, who stars in <em>Conversation With the Sea</em>, 23 October 2021.'},
        {'slug': 'yaqubi', 'focus': (0.59, 0.222), 'zoom': 5.5,
         'alt': 'Mohanad Yaqubi in a patterned scarf on the Locarno red carpet',
         'caption': 'Mohanad Yaqubi at Locarno, 10 August 2026.'},
    ],
    'src': ['doha-ff-2026-competition', 'thirteen-in-gaza-netpac', 'conversation-with-the-sea', 'revolutionaries-never-die-locarno'],
}

# film x music: printed in the overprint
BRIDGE = {
    'id': 'unsung', 'desk': 'both', 'state': 'due',
    'title': 'A film about Gaza’s first rock band, in development',
    'lines': ['Gaza’s first', 'rock band'],
    'text': 'The Palestine Film Institute took four works in progress to the Durban FilmMart. One, <em>Echoes of the Unsung</em>, '
            'follows Gaza’s first rock band as it tries to record an album. Filmmaker Jihan El-Tahri told TimesLIVE that 22 short films '
            'were made in Gaza on mobile phones during the war.',
    'band': [('Project', 'Echoes of the Unsung'), ('Showcase', 'Palestine Film Hub, Durban FilmMart')],
    'photo': {'slug': 'eltahri', 'focus': (0.5, 0.32), 'alt': 'Jihan El-Tahri on the red carpet at Locarno',
              'caption': 'Jihan El-Tahri, who spoke for the showcase, at the Locarno Film Festival, 6 August 2025.'},
    'src': ['pfi-durban-showcase'],
}

RECORD = [
    {'id': 'jerusalem', 'desk': 'music', 'state': 'on', 'fmt': 'gig',
     'title': 'The Jerusalem Festival’s last scheduled day',
     'lines': ['Jerusalem,', 'last night'],
     'text': 'Back on 16 August after a pause since 2023, the festival opened with the Jerusalem Arabic Music Ensemble’s tribute to '
             'Ziad Rahbani and ran two months of concerts, talks and exhibitions across East Jerusalem. Yabous chairman Suheil Khoury '
             'said it returned to give people hope. Tonight’s final night at Yabous is a dabke double bill: the Irth troupe’s <em>Irth Baqin</em> and the Iliya Palestine Youth troupe’s <em>Searching for Zarif</em>.',
     'band': [('Final night', 'Thu 15 Oct, 20:00'), ('Where', 'Yabous Cultural Centre, Al-Zahra Street'), ('Edition', '30th')],
     'photo': {'slug': 'damascus-gate', 'focus': (0.52, 0.36), 'zoom': 1.25,
               'alt': 'Damascus Gate in Jerusalem’s Old City, its stone walls and steps in daylight',
               'caption': 'Damascus Gate, Jerusalem’s Old City, 8 November 2022.'},
     'src': ['jerusalem-festival-closes']},
    {'id': 'saint-levant', 'desk': 'music', 'state': 'gone', 'fmt': 'sleeve',
     'title': 'Saint Levant’s Afandi, and a tour moved to spring',
     'lines': ['Afandi'],
     'text': 'His second album, his first entirely in Arabic, came out on 21 August. The North American leg of the tour, which had him '
             'at The Wiltern in Los Angeles this week, moved to spring 2027 after his US visa went to further checks: Ottawa on 19 March, '
             'Boston on 27 March. His song with Tul8te, <em>Nano</em>, topped Spotify in Egypt.',
     'band': [('Album', 'out 21 Aug'), ('North America', 'from 19 Mar 2027')],
     'photo': {'slug': 'saint-levant-live', 'focus': (0.5, 0.4),
               'alt': 'Saint Levant performing on stage at Melbourne Town Hall',
               'caption': 'Saint Levant at Melbourne Town Hall, RISING festival, 4 June 2026.'},
     'src': ['saint-levant-tour-postponed', 'national-best-arabic-songs']},
    {'id': 'rasha-nahas', 'desk': 'music', 'state': 'due', 'fmt': 'sleeve',
     'title': 'Rasha Nahas: the single is out, the album isn’t yet',
     'lines': ['Manaqish'],
     'text': 'The Haifa-born, Berlin-based songwriter released <em>Manaqish</em> on 25 September. Her third album, produced by '
             'Meshell Ndegeocello and billed for October, has no date yet. She plays Festsaal Kreuzberg, Berlin, on 14 November.',
     'band': [('Single', 'out 25 Sep'), ('Album', 'date to come')],
     'photo': {'slug': 'rasha-nahas', 'focus': (0.40, 0.55), 'zoom': 1.5,
               'alt': 'Rasha Nahas playing an electric guitar on a lit stage',
               'caption': 'Rasha Nahas at WOMEX, 27 October 2024.'},
     'credit': 'Jacob Crawfurd / WOMEX, CC BY 2.0',
     'src': ['rasha-nahas-manaqish']},
    {'id': 'faraj', 'desk': 'music', 'state': 'on', 'fmt': 'gig',
     'title': 'Faraj Suleiman alone: one piano, one microphone',
     'lines': ['Piano', 'and Mic'],
     'text': 'His first fully solo show, in Arabic, with songs from <em>Better than Berlin</em>, <em>Second Verse</em> and <em>Maryam</em>. '
             'In January he leads a 20-piece ensemble in a Ziad Rahbani tribute at the Barbican.',
     'band': [('Edmonton', 'Sat 24 Oct, Horowitz Theatre'), ('London', '23 Jan 2027, Barbican')],
     'photo': {'slug': 'faraj', 'focus': (0.62, 0.40), 'zoom': 1.35,
               'alt': 'Faraj Suleiman at a grand piano, leaning into the keys',
               'caption': 'Faraj Suleiman at WOMEX, 27 October 2019.'},
     'credit': 'Jacob Crawfurd / WOMEX, CC BY 2.0',
     'src': ['faraj-suleiman-solo']},
    {'id': 'nai', 'desk': 'music', 'state': 'on', 'fmt': 'gig',
     'title': 'Nai Barghouti plays Music of Palestine in Hong Kong',
     'lines': ['Hong Kong'],
     'text': 'The singer and flautist closes HKUST’s Cosmopolis Festival with original songs and arrangements of classic Arabic repertoire, '
             'jazz and Western classical music. She sings on MC Abdul’s <em>Wait for Me</em>.',
     'band': [('Sun 25 Oct', '19:30, Shaw Auditorium')],
     'photo': {'slug': 'nai', 'focus': (0.5, 0.35), 'alt': 'Nai Barghouti speaking in an interview', 'caption': 'Nai Barghouti interviewed by Ahotsa Info, 18 October 2019.'},
     'src': ['nai-barghouti-hong-kong']},
    {'id': 'al-festival', 'desk': 'music', 'state': 'gone', 'fmt': 'gig',
     'title': 'Kamilya Jubran and Daboor played Berlin’s AL.Festival',
     'lines': ['Berlin'],
     'text': 'AL.Festival ran 2 to 10 October at Festsaal Kreuzberg, with the oud player and composer Kamilya Jubran, '
             'the rapper Daboor of BLTNM, and a showcase from the Syrian Cassette Archives.',
     'band': [('Ran', '2–10 Oct')],
     'photo': {'slug': 'jubran', 'focus': (0.55, 0.40),
               'alt': 'Kamilya Jubran smiling, holding an oud, in concert',
               'caption': 'Kamilya Jubran in Cologne, 14 October 2009.'},
     'src': ['al-festival-berlin-jubran-daboor']},
]

# Coming attractions. date (big), month, what (HTML), where, desk, state
COMING = [
    ('17', 'Oct', 'MC Abdul live, Palestine Culture Day', 'Redwood City, California', 'music', 'on'),
    ('18', 'Oct', 'London Film Festival awards; <em>Concrete Land</em> in competition', 'London', 'film', 'due'),
    ('22–25', 'Oct', 'DC Palestinian Film and Arts Festival, 15th year', 'Angelika Pop-Up, Union Market, Washington', 'film', 'due'),
    ('23', 'Oct', '<em>Habibi Hussein</em>, about Cinema Jenin’s last projectionist', 'Trianon, Athens', 'film', 'on'),
    ('24', 'Oct', 'Faraj Suleiman, <em>Piano and Mic</em>', 'Horowitz Theatre, Edmonton', 'music', 'on'),
    ('25', 'Oct', '<em>Mohammad Bakri: A Cultural Legacy</em>', 'Trianon, Athens', 'film', 'on'),
    ('25', 'Oct', 'Nai Barghouti, <em>Music of Palestine</em>', 'HKUST, Hong Kong', 'music', 'on'),
    ('29–31', 'Oct', '<em>Yesterday the Eye Didn’t Sleep</em> at Seminci', 'Valladolid', 'film', 'on'),
    ('30', 'Oct', '<em>Who Killed Alex Odeh?</em> opens in US cinemas', 'Quad, New York · Laemmle Glendale · Uprising, Chicago', 'film', 'on'),
    ('11–20', 'Nov', 'Cairo International Film Festival, 47th; Palestinian titles not yet named', 'Cairo', 'film', 'due'),
    ('13–27', 'Nov', 'London Palestine Film Festival, from <em>Who Is Still Alive</em> to <em>Conversation With the Sea</em>', 'Barbican to Curzon Mayfair', 'film', 'on'),
    ('14', 'Nov', 'Rasha Nahas', 'Festsaal Kreuzberg, Berlin', 'music', 'on'),
    ('19–27', 'Nov', 'Doha Film Festival', 'Doha', 'film', 'on'),
    ('15', 'Dec', 'Oscar shortlist: <em>Citizen Osama</em> for Palestine, <em>Who Is Still Alive</em> for Switzerland', 'International feature', 'film', 'due'),
    ('19', 'Dec', 'Saint Levant', 'Dopa World, Dubai', 'music', 'on'),
    ('23', 'Jan', 'Faraj Suleiman’s Ziad Rahbani tribute, 20-piece ensemble', 'Barbican, London', 'music', 'on'),
    ('19', 'Mar', 'Saint Levant’s North American leg opens', 'Ottawa', 'music', 'on'),
    ('TBA', '', 'Together for Palestine, New York', 'date, venue and line-up not announced', 'music', 'due'),
]
COMING_SRC = ['mc-abdul-debut-album', 'dc-pfaf-2026', 'habibi-hussein-jenin', 'bakri-tributes', 'faraj-suleiman-solo',
              'nai-barghouti-hong-kong', 'rome-ff-yesterday-eye', 'who-killed-alex-odeh-release', 'cairo-iff-2026', 'lpff-2026',
              'rasha-nahas-manaqish', 'doha-ff-2026-competition', 'citizen-osama-oscar', 'who-is-still-alive-swiss-oscar',
              'saint-levant-tour-postponed', 'together-for-palestine-ny']

REISSUE = {
    'id': 'reissue', 'desk': 'film', 'state': 'on',
    'title': 'Before the screens went dark',
    'text': [
        'In 1937 the Alhambra in Jaffa was one of the Arab cinemas of Palestine’s coast. Alex Bakri’s <em>Habibi Hussein</em>, now on the '
        'festival circuit, comes at that loss from the projection box: he shot it in 2008–2010 while working on the NGO-backed reopening of '
        'Cinema Jenin, and turns to Hussein Darbi, who started there at twelve beside his uncle and was later sidelined by the project. '
        'The cinema was demolished seven years after it reopened, The New Arab reported.',
        'Mohammad Bakri, of <em>Jenin, Jenin</em>, died on 24 December 2025, aged 72. Athens marks him on 25 October; London screens '
        '<em>A Life in Cinema</em> on 19 and 20 November, each followed by a conversation with his son, Saleh Bakri.',
    ],
    'band': [('Habibi Hussein', 'Athens 23 Oct · Boston 24 Oct · London 18 Nov'), ('Bakri tribute', 'Athens 25 Oct · London 19–20 Nov')],
    'photo': {'slug': 'alhambra-jaffa', 'focus': (0.5, 0.45),
              'alt': 'The Alhambra cinema in Jaffa in 1937: an Art Deco facade with a statue in a circular niche, Arabic lettering above the entrance and people at the door',
              'caption': 'The Alhambra, Jaffa, 1937. Matson Collection, Library of Congress.'},
    'small': [
        {'slug': 'cinema-jenin', 'focus': (0.5, 0.5), 'alt': 'The front of Cinema Jenin, a two-storey concrete building, with cars parked outside',
         'caption': 'Cinema Jenin, 11 December 2008.'},
        {'slug': 'bakri', 'focus': (0.5, 0.25), 'alt': 'Mohammad Bakri, arms folded, in a dark jacket',
         'caption': 'Mohammad Bakri, 16 March 2010.'},
    ],
    'src': ['habibi-hussein-jenin', 'bakri-tributes'],
}
