from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import PhosphoProtein


def home(request):
    return render(request, 'home.html', {})

def login_user(request):
    pass

def logout_user(request):
    pass

def protein_list(request):
    proteins = PhosphoProtein.objects.all()
    return render(request, 'protein_list.html', {'proteins': proteins})
