"""
Spaced repetition settings and algorithms
"""

RATINGS = (
    (0, 'What is this thingy?'),
    (1, 'Barely know it'),
    (2, 'Needs some work'),
    (3, 'I remember it'),
    (4, 'Perfect!')
)


# Time in milliseconds
def rate_by_time(time):
    """Rate answer by time"""
    if time in range(0, 3999):
        return 4
    elif time in range(4000, 9999):
        return 3
    elif time in range(10000, 19999):
        return 2
    elif time in range(20000, 39999):
        return 1
    else:
        return 0


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

    i, ef = interval(repition - 1, rating, easy_factor)
    i *= easy_factor
    return i, ef
