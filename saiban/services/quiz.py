import random

from saiban.models import(
    Kanji,
    KanjiGroup,
    Example,
    Profile,
    KanjiStatus
)
from saiban.services.srs import rate_by_time

########
# Quiz #
########


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
    try:
        status = KanjiStatus.objects.filter(kanji=kanji, user=user).get()
        status.delay()
        status.save()
    except KanjiStatus.DoesNotExist:
        pass


def rate_answer(kanji, is_correct, user, answering_time=0):
    kanji = Kanji.objects.get(front=kanji)
    status = kanji.status.filter(user=user).get()

    rating = 0 if not is_correct else rate_by_time(answering_time)
    status.set_next_practice(rating)
    status.save()

    # Update profile
    update_profile(user, is_correct, rating)


def get_examples(keyword, limit=2):
    # TODO: if none found, try to use reading_contains
    return Example.objects.filter(front__contains=keyword)[:limit]

#####################
# Profile and stats #
#####################


def gain_exp(profile, rating=1):
    # Update exp
    profile.experience += (
        profile.group_level     # exp based on group level
        + profile.streak        # streak bonus
        + profile.vanity_level  # bonus for user level
        + rating                # bonus for quick answer
    ) * Profile.EXP
    # Gain a level, if accumulated enough exp (level x 10)
    new_level_exp = (profile.vanity_level + 1) * Profile.MULTIPLIER
    if profile.experience >= new_level_exp:
        profile.vanity_level += 1
        # Redistribute experience
        profile.experience = profile.experience - new_level_exp

    profile.save()


def update_profile(user, correct_answer, rating=1):
    profile = user.profile.get()

    # Update answering streak & exp
    if correct_answer:
        profile.streak += 1
        gain_exp(profile, rating)
    else:
        profile.streak = 0
        profile.save()

    # TODO: check for possible achievements to award!

    return profile
