"""The four screens and two stocks. One source for brand.py, social renders and the identity book.

White stock (day): transparent inks overprint by multiply, so film x music = the overprint red.
Black stock (night): opaque inks over a white underbase; the overprint is printed as its own screen.
"""

INK = {
    'stock': '#FAFAF6',     # white poster stock: the only white, never a card
    'film': '#FFC20E',      # film screen: projector yellow
    'music': '#D8137F',     # music screen: fuchsia
    'over': '#D80F0C',      # film x music, multiplied: belongs to both
    'key': '#16131A',       # key plate: type and halftone shadows
    # black stock
    'stock_d': '#121014',
    'film_d': '#FFC823',
    'music_d': '#FF3497',
    'over_d': '#FF3B26',
    'key_d': '#F2EFE8',     # the underbase white carries the type at night
}


def multiply(a, b):
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x * y / 255):02X}' for x, y in zip(pa, pb))


if __name__ == '__main__':
    print('film x music =', multiply(INK['film'], INK['music']), '(stored', INK['over'] + ')')
