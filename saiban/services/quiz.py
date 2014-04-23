import random

from saiban.models import(
    Kanji,
    KanjiGroup,
    Profile,
    KanjiStatus
)

# Working with kanji and groups

def get_random_kanji_group(level=1):
    """Get random kanji group by level"""
    # NB: could be slow (yet, lazy querysets should be fast!)
    try:
        return random.choice(KanjiGroup.objects.filter(level=level))
    except IndexError:
        return None

def get_scheduled_kanji(user):
    """Get next scheduled kanji group or random one"""
    level = user.profile.get().group_level

    # TODO: ponder how to not always get the same scheduled kanji (after update)
    # TODO: either get scheduled OR new! (if there are unseen kanji left in the level)
    try:
        next_kanji = KanjiStatus.objects.filter(
            user=user, group_level=level
        ).order_by('next_practice')[0:1].get()

    # No kanji scheduled at all!
    except KanjiStatus.DoesNotExist:
        # Get rangom group for this level
        random_group = get_random_kanji_group(level)
        if random_group is None:
            return None

        # Select random kanji to study
        kanji = random.choice(random_group.kanji.all())

        # Associate new status with it
        status = KanjiStatus()
        status.user = user
        status.level = level
        status.kanji = kanji
        status.seen += 1
        status.save()

        return kanji

    # Otherwise, simply returned scheduled kanji
    return next_kanji.kanji

def delay_kanji(kanji_id):
    # TODO: get kanji by id
    # TODO: get kanji status (if any)
    # TODO: delay
    pass
