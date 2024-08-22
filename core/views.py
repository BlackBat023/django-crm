from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .register import SignUpForm, AddClientForm
from .models import Clients

def home(request):
    clients = Clients.objects.all()

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
        return render(request, 'home.html', {"clients": clients})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect("home.html")

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form is not None:
            form.save()
            # Authenticate and login user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            login(request, user)
            messages.success(request, "Your registration was successfull!")
            return redirect('home.html')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

def client_details(request, pk):
    if request.user.is_authenticated:
        # Lookup cutomer record
        client_record = Clients.objects.get(id=pk)
        return render(request, "client_details.html", {"client_record": client_record})
    else:
        messages.error(request, "You must be logged in to view this page...")
        return redirect("home.html")
        
def delete_details(request, pk):
    if request.user.is_authenticated:
        # Find record to delete
        delete_it = Clients.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record has been deleted...")
        return redirect("home.html")
    else:
        messages.error(request, "You must cbe logged in to delete records...")
        return redirect("home.html")

def add_client(request):
    form = AddClientForm(request.POST or None)

    if request.user.is_authenticated:
        if form.is_valid():
            add_client = form.save()
            messages.success(request, "Client has been added...")
            return redirect("home.html")
        else:
            return render(request, "add_client.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to view this page...")
        return redirect("home.html")

def edit_details(request, pk):
    if request.user.is_authenticated:
        # Find client record
        client_record = Clients.objects.get(id=pk)
        form = AddClientForm(request.POST or None, instance=client_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Client details successfully updated...")
            return redirect('home.html')
        return render(request, 'edit_details.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to view this page...")
        return redirect("home.html")
    