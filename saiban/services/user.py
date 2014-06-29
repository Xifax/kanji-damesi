import random

from django.contrib.auth.models import User

from saiban.models import Profile, KanjiStatus

###################
# User management #
###################


def new_profile(user):
    """Associate new profile with existing user"""
    profile = Profile()
    profile.user = user
    profile.save()

    return profile


def new_user_with_profile(form):
    """Create new user with associated profile using form data"""
    user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1']
    )

    return user, new_profile(user)


def get_anonymous_user(request):
    """Get or create anonymous user"""
    try:
        user = User.objects.get(username='Anonymous')
    except User.DoesNotExist:
        user = User(username="Anonymous")
        user.save()
        profile = Profile()
        profile.user = user
        profile.save()

    return user


def get_motto():
    """Get some random motto"""
    return random.choice([
        "Just look at the time, it's kanji time!",
        "How about a tiny-weeny kanji study, eh?",
        "I love me some fresh kanji early in the morning.",
        "You're doing quite well! Probably.",
        "You know, kanji won't study themselves.",
        "Once upon a time, there was a kanji novice...",
        "Every kanji has it's day.",
        "Good pace! Only a couple of thousands kanji left.",
    ])


def get_stats(user):
    """Get some user stats"""
    days = random.randint(1, 7)
    stats = {
        'kanji_studied': 0,
        'new_kanji_studied': 0,
        'errors_made': 0,
        'percentage': 0,
        'days': days,
    }
    return stats

######################
# Profile management #
######################

DESCRIPTIONS = {
    1: 'I can study',
    2: 'Bring it on',
    3: 'Hurt me plenty',
    4: 'Hardcore',
}


def get_user_level(user):
    """Get level for specified user"""
    level = user.profile.get().group_level
    return {
        'level': level,
        'description': DESCRIPTIONS.get(level, '')
    }


def change_user_level(user, level):
    """Change level for specified user"""
    profile = user.profile.get()
    profile.group_level = level
    profile.save()

    return {
        'level': level,
        'description': DESCRIPTIONS.get(level, '')
    }


def get_study_list(user):
    """Get study list for specific user"""
    return KanjiStatus.objects.filter(user=user)
