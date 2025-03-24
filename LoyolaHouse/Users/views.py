from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('loyola:dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('loyola:dashboard')
        else:
            messages.error(request, "Wrong Username and Password. Try Again...")
            return redirect('users:login')

    return render(request, 'users/login.html')

