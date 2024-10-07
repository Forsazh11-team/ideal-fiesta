from django.db import models
from django.contrib.auth.models import User
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
