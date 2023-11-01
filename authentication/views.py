from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from authentication.forms import SignupForm


def index(request):
    return render(request, 'index.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            request.session['invalid_login'] = "Invalid Password or username, try again"
            return redirect('login')
    else:
        form = AuthenticationForm
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
