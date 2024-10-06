from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
