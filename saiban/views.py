from django.shortcuts import render
from django.http import HttpResponse

# General views
def index(request):
    return render(request, 'index.html')

def profile(request):
    pass

def login(request):
    pass

def register(request):
    pass

def saiban(request):
    pass
