from django.contrib import admin
from blog.models import Tweet, Comment, Like, Hashtag

admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Hashtag)