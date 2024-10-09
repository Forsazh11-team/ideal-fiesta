from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template import context
from django.views.generic import ListView
from users.models import Follow
from blog.models import Tweet
from django.http import JsonResponse  



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
        try:
            author = request.user
            content = request.POST.get('content')  # Используем get для безопасного доступа
            
            # Проверяем, что содержимое не пустое
            if content:
                tweet = Tweet.objects.create(author=author, content=content)
                tweet.save()

                # Формируем данные для ответа
                response_data = {
                    'id': tweet.id,
                    'author_username': tweet.author.username,
                    'date_posted': tweet.date_posted.strftime('%Y-%m-%d %H:%M:%S'),  # Форматируем дату
                    'content': tweet.content
                }

                # Проверяем, является ли запрос AJAX
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse(response_data)  # Возвращаем JSON с данными нового твита
                else:
                    return redirect('/home')  # Для обычного запроса перенаправляем
            else:
                # Возвращаем ошибку, если контент пустой
                return JsonResponse({'error': 'Content cannot be empty'}, status=400)

        except Exception as e:
            return JsonResponse({'error': 'An internal error occurred.'}, status=500)

    return redirect('/home')  # Укажите свой шаблон


def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)  # Убедитесь, что используете tweet_id здесь
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Проверка, является ли запрос AJAX
        data = {
            'author': tweet.author.username,
            'content': tweet.content,
            'date_posted': tweet.date_posted.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse(data)
