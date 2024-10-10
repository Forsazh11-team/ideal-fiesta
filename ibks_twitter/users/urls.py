from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("login/otp", views.opt, name="otp"),
    path('captcha/', include('captcha.urls')),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='reset_password'),
    path('reset_password/done',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
         success_url=reverse_lazy("password_reset_complete")),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('confirmation/<str:status>/', views.confirmation_view, name='confirmation'),
    #path('profile/<uidb64>', views.update_profile, name = 'update_profile')
]