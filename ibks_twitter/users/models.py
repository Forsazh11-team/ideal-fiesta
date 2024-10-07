from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user.png/', upload_to='img')
    location = models.CharField(max_length=30, default="")
    about = models.CharField(max_length=150, default="")
    def __str__(self):
        return f'{self.user.username} Profile'
    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def set_location(self, location):
        self.location = location
    def set_about(self, about):
        self.about = about
    def set_image(self, image):
        pass


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)