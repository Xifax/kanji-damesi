from django.shortcuts import render, redirect
from django.contrib.auth import(
    logout as logout_user,
    authenticate,
    login as login_user
)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from saiban.services.user import (
    new_user_with_profile,
    get_anonymous_user,
    get_motto,
    get_stats
)

                               ################
                               # Landing page #
                               ################


def index(request):
    """Show Saiban home page with login/register"""
    if request.user.is_authenticated():
        redirect('profile')

    return render(request, 'index.html')


                               #################
                               # Profile pages #
                               #################

def profile(request):
    """Display main profile page"""
    if not request.user.is_authenticated():
        redirect('index')

    return render(
        request,
        'profile.html',
        {
            'user': request.user,
            'motto': get_motto(),
            'stats': get_stats(request.user)
        }
    )


def achievements(request):
    """Display user achievements"""
    return render(request, 'profile/achievements.html')


def history(request):
    """Display user study history"""
    return render(request, 'profile/history.html')


def stats(request):
    """Display user kanji stats"""
    return render(request, 'profile/stats.html')

                               #################
                               # Authorization #
                               #################


def register(request):
    """Register new user and associate profile"""
    if request.user.is_authenticated():
        return redirect('profile')

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if not form.is_valid():
            return render(
                request,
                'index.html',
                {'error_message': 'Could not create user', 'register': True}
                # {'error_message': form.errors.values()}
            )
        else:
            # If valid form -> create user
            user, profile = new_user_with_profile(form)

            # Login registered user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login_user(request, user)

            # Go to profile
            return redirect('profile')

    # Otherwise, display register page
    return render(request, 'index.html', {'register': True})


def login(request):
    """Try to login existing user"""
    if request.user.is_authenticated():
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if not form.is_valid():
            return render(
                request,
                'index.html',
                {'error_message': 'Sorry, could not login', 'login': True}
                # {'error_message':
                #' '.join([e.as_text() for e in form.errors.values()])}
            )

        # If form is valid, try to authenticate user
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            # Log in and  redirect to profile
            login_user(request, user)
            return redirect('profile')
        else:
            return render(
                request,
                'index.html',
                {'error_message': 'Sorry, could not login', 'login': True}
            )

    # Otherwise, display login page
    return render(request, 'index.html', {'login': True})


def logout(request):
    """Try to logout existing user"""
    if request.user.is_authenticated():
        logout_user(request)
        return redirect('index')


                                ##############
                                # Kanji quiz #
                                ##############

def quiz(request):
    """Show quiz page"""
    return render(request, 'quiz.html')


def try_quiz(request):
    """Try kanji quiz as anonymous user"""
    # Auth as anonymous user
    if request.user.is_authenticated():
        logout_user(request)

    # Get or create anonymous user
    user = get_anonymous_user(request)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login_user(request, user)

    return render(request, 'quiz.html')
