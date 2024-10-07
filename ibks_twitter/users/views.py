from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.checks import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from gitdb.utils.encoding import force_text

from .token import EmailVerificationTokenGenerator, email_verification_token

from .forms import UserRegisterForm

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