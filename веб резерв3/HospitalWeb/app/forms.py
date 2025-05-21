# app/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import Blog, Comment

class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        min_length=2,
        max_length=50,
    )
    email = forms.EmailField(
        label="Email",
        min_length=5,
    )
    rating = forms.ChoiceField(
        label="Оцените сайт",
        choices=[
            ('5', 'Отлично'),
            ('4', 'Хорошо'),
            ('3', 'Удовлетворительно'),
            ('2', 'Плохо'),
            ('1', 'Ужасно'),
        ],
        widget=forms.RadioSelect,
        initial='5',
    )
    favorite_section = forms.ChoiceField(
        label="Любимый раздел",
        choices=[
            ('home', 'Главная'),
            ('about', 'О нас'),
            ('services', 'Услуги'),
            ('contacts', 'Контакты'),
        ],
    )
    subscribe = forms.BooleanField(
        label="Хотите получать новости?",
        required=False,
    )
    comments = forms.CharField(
        label="Ваш комментарий",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False,
        max_length=500,
    )
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'summary', 'content']
        widgets = {
            'summary': forms.Textarea(attrs={'rows':3}),
            'content': forms.Textarea(attrs={'rows':8}),
        }
# --- ФОРМА ДЛЯ КОММЕНТАРИЕВ ---
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'class': 'form-control',
                'placeholder': 'Ваш комментарий...'
            }),
        }