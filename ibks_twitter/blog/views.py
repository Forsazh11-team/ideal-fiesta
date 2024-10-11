from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from users.models import Follow
from blog.models import Tweet, Like, Hashtag
from django.http import JsonResponse, request
import json
from blog.forms import TweetForm


class Settings_view(ListView):
    template_name = 'settings_page.html'
    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class Home_list_view(ListView):
    model = Tweet
    template_name = 'main_page.html'
    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        users = []
        users.append(self.request.user)
        for i in data['object_list']:
            users.append(i.follow_user)
        try:
            tweets = Tweet.objects.filter(author__in=users).order_by('-date_posted')
            data['flag_posts'] = True
            data['tweets'] = tweets
            liked_tweet_ids = Like.objects.filter(user=self.request.user).values_list('tweet_id', flat=True)
            data['liked_tweet_ids'] = list(liked_tweet_ids)
        except:
            data['flag_posts'] = False

        data['user'] = self.request.user
        data['object_list'] = data['object_list'][:6]
        data['form'] = TweetForm()
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
            liked_tweet_ids = Like.objects.filter(user=self.request.user).values_list('tweet_id', flat=True)
            data['liked_tweet_ids'] = list(liked_tweet_ids)
            data['flag_posts'] = True
            data['tweets'] = tweets
        except:
            print("No...")
            data['flag_posts'] = False
        data['user'] = user
        data['auth_user'] = self.request.user
        data['flag_track'] = True
        if(data['user'] == data['auth_user'] or data['object_list'].filter(user=data['auth_user']).exists()):
            data['flag_track'] = False
        return data


def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            print("FORM VALID")
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            hashtags_list = form.cleaned_data['hashtags']
            for tag in hashtags_list:
                hashtag, created = Hashtag.objects.get_or_create(text=tag)
                tweet.hashtags.add(hashtag)
            response_data = {
                'id': tweet.id,
                'author_username': tweet.author.username,
                'date_posted': tweet.date_posted.strftime('%Y-%m-%d %H:%M:%S'),  # Форматируем дату
                'content': tweet.content,
                'hashtag': tweet.hashtags
            }
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            else:
                return redirect('/home')

        else:
            return JsonResponse({'error': 'not valid form'}, status=400)
    else:
        form = TweetForm(request.POST)
    return redirect('/home')


def tweet_detail(request, tweet_id):
    if request.method == 'GET':
        tweet = get_object_or_404(Tweet, id=tweet_id)  # Убедитесь, что используете tweet_id здесь
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Проверка, является ли запрос AJAX
            data = {
                'author': tweet.author.username,
                'content': tweet.content,
                'date_posted': tweet.date_posted.strftime('%Y-%m-%d %H:%M:%S'),
                'img': tweet.author.profile.image.url,
            }
            return JsonResponse(data)
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass


@require_POST
def like_tweet(request, tweet_id):
    data = json.loads(request.body)
    liked = data.get('liked')
    tweet = Tweet.objects.get(id=tweet_id)
    if liked:
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if created:
            tweet.likes += 1
            tweet.save()
            return JsonResponse({'liked': True})
        else:
            return JsonResponse({'liked': True})
    else:
        if Like.objects.filter(user=request.user, tweet=tweet).exists():
            Like.objects.filter(user=request.user, tweet=tweet).delete()
            tweet.likes -= 1
            tweet.save()
        return JsonResponse({'liked': False})


class Search_view(ListView):
    model = Tweet
    template_name = 'search_result_page.html'

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        users = []
        users.append(self.request.user)
        for i in data['object_list']:
            users.append(i.follow_user)
        try:
            query = self.request.GET.get('tag')
            hashtag = Hashtag.objects.get(text=query)
            print(hashtag)
            tweets = hashtag.tweets.all().order_by('-date_posted')
            print(tweets)
            data['flag_posts'] = True
            data['tweets'] = tweets
            liked_tweet_ids = Like.objects.filter(user=self.request.user).values_list('tweet_id', flat=True)
            data['liked_tweet_ids'] = list(liked_tweet_ids)
        except:
            data['flag_posts'] = False
        data['user'] = self.request.user
        data['object_list'] = data['object_list'][:6]
        return data
