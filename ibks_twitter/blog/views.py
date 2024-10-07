from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template import context
from django.views.generic import ListView
from users.models import Follow
from blog.models import Tweet


class Home_list_view(ListView):
    model = Tweet
    template_name = 'main_page.html'

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        users = []
        for i in data['object_list']:
            users.append(i.follow_user)

        try:
            tweets = Tweet.objects.filter(author__in=users).order_by('-date_posted')
            print(tweets)
            data['flag_posts'] = True
            data['tweets'] = tweets
        except:
            data['flag_posts'] = False

        data['user'] = self.request.user
        data['object_list'] = data['object_list'][:6]
        print(data['flag_posts'])
        return data


class Profile_list_view(ListView):
    model = Tweet
    template_name = 'profile_page.html'

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        try:
            tweets = Tweet.objects.filter(author=user).order_by('-date_posted')
            print(tweets)
            data['flag_posts'] = True
            data['tweets'] = tweets
        except:
            print("No...")
            data['flag_posts'] = False
        data['user'] = user
        data['auth_user'] = self.request.user
        return data


def tweet_view(request):
    if request.method == 'POST':
        author = request.user
        content = request.POST['content']
        tweet = Tweet.objects.create(author=author, content=content)
        tweet.save()
        return redirect('/home')
