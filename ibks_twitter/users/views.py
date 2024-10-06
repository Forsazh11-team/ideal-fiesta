from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def login(request):
    return render(request, "login.html", {})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление после успешной регистрации
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
