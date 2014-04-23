import random

from saiban.models import(
    Kanji,
    KanjiGroup,
    Profile
)

# Working with kanji and groups

def get_random_kanji_group(level=1):
    """Get random kanji group by level"""
    # TODO: allow to select multiple levels
    # NB: could be slow (yet, lazy querysets should be fast!)
    # return KanjiGroup.objects.filter(level=level).order_by('?')[:1]
    return random.choice(KanjiGroup.objects.filter(level=level))

def get_scheduled_kanji_group(user):
    """Get next scheduled kanji group or random one"""
    # TODO: try to get scheduled
    # TODO: if none, get random
    pass


