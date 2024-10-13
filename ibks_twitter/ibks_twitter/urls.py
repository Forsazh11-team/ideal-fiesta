"""
URL configuration for ibks_twitter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from django.conf.urls.static import static
from blog.views import Home_list_view, Profile_list_view, tweet_detail,Settings_view, Search_view, Comment_view

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('users.urls')),
    path("home/", Home_list_view.as_view()),
    path("tweet/", blog_views.create_tweet),
    path("profile/<username>", Profile_list_view.as_view()),
    path('tweet/<int:tweet_id>/', tweet_detail, name='tweet_detail'),  # Для AJAX запроса
    path('settings/', Settings_view.as_view()),
    path('like/<int:tweet_id>/', blog_views.like_tweet, name='like_tweet'),
    path('search/', Search_view.as_view(), name='search_by_hashtag'),
    path('comment/', Comment_view.as_view(), name='create_cooment')


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)