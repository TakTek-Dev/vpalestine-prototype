"""Self-hosted, feature-complete WOFF2 subsets of the two brand faces.

python -I tools/fonts.py   (from the project root; sources in research/font-src, gitignored)

Anybody (Etcetera Type Co, OFL) prints the posters: titles, the where-and-when band, dates, navigation.
Its width axis (50-150) is how a title is set to its sheet, the way poster type was chosen to fill the measure.
Besley (Indestructible Type, OFL), a Clarendon, prints the reading: decks, story text, captions.
Every OpenType layout feature is kept (case, tabular figures, fractions, slashed zero, oldstyle figures).
"""
import os
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'research', 'font-src')
OUT = os.path.join(ROOT, 'assets', 'fonts')
os.makedirs(OUT, exist_ok=True)

# Basic Latin + Latin-1 + the Latin Extended-A letters names and transliteration use
# (ā ī ū ḥ ṣ ḍ ṭ ẓ ʿ ʾ, plus Turkish/Polish/French accents in festival and people names),
# typographic punctuation, arrows, prime marks for running times, multiplication sign for collaborations.
UNICODES = (
    list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) +
    [0x1E0C, 0x1E0D, 0x1E24, 0x1E25, 0x1E62, 0x1E63, 0x1E6C, 0x1E6D, 0x1E92, 0x1E93, 0x02BE, 0x02BF, 0x02BC,
     0x2009, 0x200A, 0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026,
     0x2032, 0x2033, 0x2039, 0x203A, 0x2044, 0x20AC, 0x2116, 0x2190, 0x2191, 0x2192, 0x2193, 0x2212, 0x2248,
     0x2260, 0x2264, 0x2265, 0x00D7, 0x00B0, 0x00B7, 0x2153, 0x2154, 0x00BC, 0x00BD, 0x00BE]
)

JOBS = [
    ('Anybody_wdth-wght.ttf', 'anybody-var.woff2'),
    ('Anybody-Italic_wdth-wght.ttf', 'anybody-italic-var.woff2'),
    ('Besley_wght.ttf', 'besley-var.woff2'),
    ('Besley-Italic_wght.ttf', 'besley-italic-var.woff2'),
]

for src, out in JOBS:
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['*']
    opts.name_IDs = ['*']
    opts.name_languages = ['*']
    opts.notdef_outline = True
    opts.glyph_names = False
    opts.hinting = False
    opts.desubroutinize = True
    font = subset.load_font(os.path.join(SRC, src), opts)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=UNICODES)
    sub.subset(font)
    path = os.path.join(OUT, out)
    subset.save_font(font, path, opts)
    print(out, os.path.getsize(path) // 1024, 'KB')
