"""
Spaced repetition settings and algorithms
"""

RATINGS = (
        (0, 'Blanked'),
        (1, 'Barely Know It'),
        (2, 'Needs Work'),
        (3, 'Remembered'),
        (4, 'Solid')
)

def interval(repition, rating, easy_factor=2.5):
    """
    Calculate SRS repetition interval
    see: http://www.supermemo.com/english/ol/sm2.htm
    Rating may vary from 0 (wtf is this) to 4 (known by heart)
    """
    ef = easy_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
    ef = ef if ef >= 1.3 else 1.3

    if rating < 3:
        return 1, ef
    if repition == 1:
        return 1, ef
    if repition == 2:
        return 6, ef

    i, ef = interval(repition-1, rating, easy_factor)
    i *= easy_factor
    return i, ef

