from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from gitdb.utils.encoding import force_text
from .models import OTP
from .token import email_verification_token
from .forms import UserRegisterForm
import pyotp
from random import randint

def confirmation_view(request, status):
    messages = {
        'success': 'Подтверждение успешно. Можете <a href="/login">войти</a> в свой аккаунт.',
        'invalid': 'Ссылка невалидна.',
        'email_sent': 'На указанную почту выслано письмо для подтверждения.'
    }
    
    message = messages.get(status, 'Некорректный статус.')
    return render(request, 'confirm.html', {'message': message})


def login(request):
    return render(request, "login.html", {})

def login_view(request):
    error_message = ""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = User.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=password)
        if user is not None:
            key = pyotp.random_base32()
            totp = pyotp.HOTP(key)
            time = randint(0, 100000)
            otp_obj, created = OTP.objects.get_or_create(user=user, email=email)
            otp_obj.otp_secret = key
            otp_obj.save()
            current_site = get_current_site(request)
            mail_subject = 'A one-time password has been sent to your email'
            message = render_to_string('otp_body.html', {
                'user': user,
                'domain': current_site.domain,
                'otp' : totp.at(time),
            })
            email_send = EmailMessage(
                mail_subject, message, to=[email]
            )
            email_send.send()
            request.session['email'] = email
            request.session['time'] = time
            request.session['password'] = password
            return redirect('otp')
        else:
            error_message = "Invalid login or password"

    return render(request, "login.html", {'error_message': error_message})


def opt(request):
    err_mes = ""
    if request.method == 'POST':
        email = request.session.get('email')
        time = request.session.get('time')
        password = request.session.get('time')
        code = request.POST['Code']
        otp_obj = OTP.objects.filter(email=email).first()
        if otp_obj:
            otp = pyotp.HOTP(otp_obj.otp_secret)
            if otp.verify(code, time):
                otp_obj.is_verified = True
                otp_obj.save()
                print("verify code")
                user = otp_obj.user
                if user:
                    login(request, user)
                    return HttpResponse('Success.')
                else:
                    return redirect('/login')
            else:
                print("not verify code")
                return redirect('/login')
        else:
            return redirect('/login')

    return render(request, "otp.html", {})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('mail_body.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return confirmation_view(request, 'email_sent')
        else:
            print(form)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return confirmation_view(request, 'success')
    else:
        return confirmation_view(request, 'invalid')