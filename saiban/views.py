from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import(
    logout as logout_user,
    authenticate,
    login as login_user
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import logging

# General views
def index(request):
    return render(request, 'index.html')

def profile(request):
    if not request.user.is_authenticated():
        raise Http404

    return render(request, 'profile.html', {'user': request.user})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if not form.is_valid():
            return render(
                    request,
                    'index.html',
                    {'error_message': 'Sorry, could not login'}
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
                    {'error_message': 'Sorry, could not login'}
            )

    # Otherwise, redirect to index
    return redirect('index')

def logout(request):
    logout_user(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if not form.is_valid():
            return render(
                    request,
                    'index.html',
                    {'error_message': form.errors.values()}
            )

    # If valid form -> create user
    User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
    )

    # Go to profile
    return redirect('profile')

def saiban(request):
    pass
