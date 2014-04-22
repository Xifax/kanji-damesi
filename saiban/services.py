import random

from django.contrib.auth.models import User

from models import(
    Kanji,
    KanjiGroup,
    Profile
)


# Working with kanji and groups

def get_random_kanji_group(level=1):
    """Get random kanji group by level"""
    # NB: could be slow (yet, lazy querysets should be fast!)
    return random.choice(KanjiGroup.objects.filter(level=level))

def get_scheduled_kanji_group(user):
    """Get next scheduled kanji group or random one"""
    pass

# User management

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

