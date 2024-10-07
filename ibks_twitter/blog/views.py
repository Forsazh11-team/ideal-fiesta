from django.shortcuts import render

def home(request):
    return render(request, 'main_page.html', {})

def user_account(request):
    pass