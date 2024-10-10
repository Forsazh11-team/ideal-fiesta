from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Hashtag(models.Model):
    text = models.CharField(max_length=100, unique=True)  # Текст хэштега, уникальный
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания хэштега

    def __str__(self):
        return self.text


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    hashtags = models.ManyToManyField(Hashtag, related_name='tweets')
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

