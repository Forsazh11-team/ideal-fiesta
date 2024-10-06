from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
def home(request):
    return render(request, "home.html", {})

def login(request):
    return render(request, "login.html", {})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return redirect('register')
        #     username = form.cleaned_data.get('username')
        #     messages.success(request, f'Создан аккаунт {username}!')
        #     return redirect('login')
    else:
        return render(request, 'register.html', {})
