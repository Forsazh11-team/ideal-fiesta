from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    hashtags = forms.CharField(max_length=100, required=False,widget=forms.Textarea(attrs={
                'rows': 1,  # Количество строк
                'placeholder': 'Введите теги через запятую',  # Текст-заполнитель
                'oninput': 'autoResize(this)'
            }))
    content = forms.CharField(max_length=300, required=True, widget=forms.Textarea(attrs={
                'rows': 2,  # Количество строк
                'placeholder': 'Поделитесь чем-нибудь!',  # Текст-заполнитель
                'oninput': 'autoResize(this)'
        }))


    class Meta:
        model = Tweet
        fields = ['content', 'hashtags']

    def clean_hashtags(self):
        hashtags_data = self.cleaned_data['hashtags']
        hashtags_list = [tag.strip() for tag in hashtags_data.split(',') if tag.strip()]
        return hashtags_list
