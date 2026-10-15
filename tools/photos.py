"""Commons photos -> grayscale WebP plates for the halftone screens.

python -I tools/photos.py   (reads research/photos.json, writes assets/img/photo/*.webp + CREDITS.md)

Every photo on the site is printed as a halftone over an ink, so the source plate is grayscale:
levels are set per photo (1st..99th percentile) so the screen has a full range of dot sizes.
Thumbnails are requested at Commons' standard widths only (non-standard widths are throttled).
Without JavaScript the same plate shows multiplied over its ink: a duotone, still in the world.
"""
import io, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img', 'photo')
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'VPalestine-prototype/1.0 (TakTek design prototype; en.developer2 at gmail)'}
STANDARD = [500, 960, 1280, 1920]

# slug -> (Commons file, longest edge we need)
USE = {
    'suleiman': ('File:Počasno Srce Sarajeva Elia Suleiman.jpg', 1920),
    'mc-abdul': ('File:MC Abdul 2.jpg', 1280),
    'coolidge': ('File:Coolidge Corner Theatre Marquee.jpg', 1280),
    'gaza-port': ('File:5M0A8322-01.jpg', 1280),
    'el-basha': ('File:Kamel elbasha.jpg', 1280),
    'yaqubi': ('File:Mohanad Yaqubi at the 79th Locarno Film Festival 01.jpg', 1280),
    'alkhatib': (None, 1280),  # resolved by prefix below (long file name)
    'odeh-directors': ('File:Sundance awards 2026 - Who Killed Alex Odeh - Jason Osder and William Lafi Youmans.jpg', 1280),
    'saint-levant': ('File:Saint Levant en Madrid (2025) 01.jpg', 960),
    'faraj': (None, 1280),
    'rasha-nahas': ('File:Womex24 rasha nahas by jacob crawfurd.jpg', 1280),
    'jubran': ('File:Kamilya Jubran with Oud in Cologne (8397).jpg', 1280),
    'damascus-gate': ('File:Damascus Gate IMG 3146.jpg', 1280),
    'alhambra-jaffa': (None, 1920),
    'cinema-jenin': ('File:Cinema front 1.jpg', 500),
    'bakri': ('File:Mohammad Bakri.jpg', 1280),
}
PREFIX = {'alkhatib': 'File:Abdallah Alkhatib at Berlin', 'faraj': 'File:Faraj suleiman artist womex19', 'alhambra-jaffa': 'File:Jaffa. Alhambra Cinema'}


def api(title, width):
    q = urllib.parse.urlencode({'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata',
                                'iiurlwidth': width, 'format': 'json', 'formatversion': 2})
    req = urllib.request.Request('https://commons.wikimedia.org/w/api.php?' + q, headers=UA)
    for attempt in range(6):
        try:
            return json.load(urllib.request.urlopen(req, timeout=40))['query']['pages'][0]
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(10 + attempt * 10)
    raise SystemExit('Commons API keeps throttling: ' + title)


def fetch(url):
    for attempt in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception as e:
            print('  retry', attempt + 1, e)
            time.sleep(3 + attempt * 4)
    raise SystemExit('could not fetch ' + url)


def main():
    research = {p['file']: p for p in json.load(open(os.path.join(ROOT, 'research', 'photos.json'), encoding='utf-8'))}
    credits, meta = [], {}
    only = set(sys.argv[1:])
    for slug, (title, need) in USE.items():
        if title is None:
            title = next(f for f in research if f.startswith(PREFIX[slug]))
        r = research[title]
        out = os.path.join(OUT, slug + '.webp')
        page = api(title, 1280)
        ii = page['imageinfo'][0]
        w0, h0 = ii['width'], ii['height']
        width = next((s for s in STANDARD if s >= need), STANDARD[-1])
        if max(w0, h0) <= width or w0 <= width:
            url = ii['url']
        else:
            url = api(title, width)['imageinfo'][0]['thumburl']
        if not (only and slug not in only) and not os.path.exists(out):
            img = Image.open(io.BytesIO(fetch(url)))
            img = ImageOps.exif_transpose(img).convert('L')
            img = ImageOps.autocontrast(img, cutoff=1)
            img.save(out, 'WEBP', quality=80, method=6)
            print(slug, img.size, os.path.getsize(out) // 1024, 'KB')
            time.sleep(4)
        im = Image.open(out)
        meta[slug] = {'w': im.size[0], 'h': im.size[1], 'file': title, 'author': r['author'], 'license': r['license'],
                      'license_url': r.get('license_url', ''), 'page': r['page_url'], 'date': r.get('date', ''),
                      'place': r.get('place', ''), 'description': r.get('description', '')}
        credits.append(f"- `{slug}.webp` — [{title[5:]}]({r['page_url']}) · {r['author']} · {r['license']} · "
                       f"{r.get('date', '')} · grayscale, levels set, printed as a halftone on the site")
    json.dump(meta, open(os.path.join(ROOT, 'tools', 'out', 'photos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, 'CREDITS.md'), 'w', encoding='utf-8').write(
        '# Photo credits\n\nAll photographs from Wikimedia Commons, used under the licences below. None is a film still or poster; '
        'each is captioned on the site with its real date and place.\n\n' + '\n'.join(credits) + '\n')


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'tools', 'out'), exist_ok=True)
    main()
