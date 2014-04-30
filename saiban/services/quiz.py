import random

from saiban.models import(
    Kanji,
    KanjiGroup,
    # Profile,
    KanjiStatus
)

# Working with kanji and groups


def get_random_kanji_group(level=1):
    """Get random kanji group by level"""
    # NB: could be slow (yet, lazy querysets should be fast!)
    try:
        # TODO: profile and optimize!
        return random.choice(KanjiGroup.objects.filter(level=level))
    except IndexError:
        return None


def get_new_random_kanji(user):
    """Get random kanji to study"""
    # TODO: do not include those already in study list?
    level = user.profile.get().group_level

    # Get rangom group for this level
    random_group = get_random_kanji_group(level)
    if random_group is None:
        return None

    # Select random kanji to study
    kanji = random.choice(random_group.kanji.all())

    # Get existing status
    try:
        status = KanjiStatus.objects.filter(user=user, kanji=kanji).get()
    # Or associate new status with it
    except KanjiStatus.DoesNotExist:
        status = KanjiStatus()
        status.user = user
        status.level = level
        status.kanji = kanji

    status.seen += 1
    status.save()

    return kanji


def get_scheduled_kanji(user):
    """Get next scheduled kanji group or random one"""
    # TODO: if could not get profile for user -> create new one
    level = user.profile.get().group_level

    # Either get scheduled or get new/random kanji to study
    should_get_random = random.choice([True, False])
    if should_get_random:
        return get_new_random_kanji(user)

    # If only one, two or three statuses, get random
    if KanjiStatus.objects.filter(user=user, group_level=level).count() < 3:
        return get_new_random_kanji(user)

    # At last, try to get scheduled
    try:
        next_kanji = KanjiStatus.objects.filter(
            user=user, group_level=level
        ).order_by('next_practice')[0:1].get()

    # No kanji scheduled at all!
    except KanjiStatus.DoesNotExist:
        return get_new_random_kanji(user)

    # Otherwise, simply returned scheduled kanji
    return next_kanji.kanji


def delay_kanji(kanji, user):
    # Get kanji by its front
    kanji = Kanji.objects.get(front=kanji)

    # Get kanji status (if any)
    status = kanji.status.filter(user=user).get()
    if status:
        status.delay()
        kanji.status.save()


def rate_answer(kanji, is_correct, user):
    kanji = Kanji.objects.get(front=kanji)
    status = kanji.status.filter(user=user).get()

    # TODO: base rating also upon time it took user to answer
    rating = 0 if not is_correct else 4
    status.set_next_practice(rating)
    status.save()
