from saiban.models import(
    Kanji,
    KanjiGroup,
    Profile
)

from django.contrib.auth.models import User

# Working with kanji and groups

def get_random_kanji_group(level=1):
    """Get random kanji group by level"""
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

