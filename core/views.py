from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome " + username)
            return redirect("home.html")
        else:
            messages.error(request, "We encountered an error and could not log you in, please try again...")
            return redirect("home.html")
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect("home.html")

def register_user(request):
    return render(request, 'register.html', {})