from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import PhosphoProtein
from django.contrib import messages
from .forms import SignUpForm
from .models import Profile

def home(request):
    return render(request, 'home.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            messages.success(request, "You are logged in.")
            return redirect('home')
        else:
            messages.error(request, "Ups, something went wrong. Please try again.")
            return render(request, "login.html", {})
    else:
        return render(request, "login.html", {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() 
            institution_name = form.cleaned_data['institution_name']
            country = form.cleaned_data['country']
            profile = Profile.objects.create(user=user, institution_name=institution_name, country=country)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
    else:
        form = SignUpForm() 
        return render(request, "register.html", {'form': form})
    
    return render(request, "register.html", {'form': form})

def protein_list(request):
    proteins = PhosphoProtein.objects.all()
    return render(request, 'protein_list.html', {'proteins': proteins})
